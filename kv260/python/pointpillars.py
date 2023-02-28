"""
Copyright 2022-2023 Woven Planet Holdings.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from timeit import default_timer as timer
from typing import List, Sequence

import ctypes
import numpy as np
import torch
import vart
import xir
from mmdet3d.ops.voxel import voxelization
from numpy.ctypeslib import load_library, ndpointer
from torch.nn import functional as F


@dataclass
class TensorBundle:
    """ Handle these 2 as a pair to avoid human errors. """
    ndarray: np.ndarray
    xtensor: xir.Tensor


class VartContext:
    def __init__(self, xmodel: str):
        # create the runner.
        self.graph = xir.Graph.deserialize(xmodel)
        subgraphs = self.get_child_subgraph_dpu(self.graph)
        assert len(subgraphs) == 1  # only one DPU kernel
        self.runner = vart.Runner.create_runner(subgraphs[0], "run")

        # Allocate TensorBundle objects.
        self.inputs: Sequence[TensorBundle] = []
        for x in self.runner.get_input_tensors():
            a = np.zeros(tuple(x.dims), dtype=np.int8, order="C")
            self.inputs.append(TensorBundle(a, x))
        self.outputs: Sequence[TensorBundle] = []
        for x in self.runner.get_output_tensors():
            a = np.zeros(tuple(x.dims), dtype=np.int8, order="C")
            self.outputs.append(TensorBundle(a, x))


    @staticmethod
    def get_child_subgraph_dpu(graph: "Graph") -> List["Subgraph"]:
        """
        From: https://github.com/Xilinx/Vitis-AI/blob/v2.5/src/Vitis-AI-Runtime/VART/vart/dpu-runner/samples/resnet50_mt_py/resnet50.py
        """
        assert graph is not None, "'graph' should not be None."
        root_subgraph = graph.get_root_subgraph()
        assert (root_subgraph is not None), "Failed to get root subgraph of input Graph object."
        if root_subgraph.is_leaf:
            return []
        child_subgraphs = root_subgraph.toposort_child_subgraph()
        assert child_subgraphs is not None and len(child_subgraphs) > 0
        return [
            cs for cs in child_subgraphs
            if cs.has_attr("device") and cs.get_attr("device").upper() == "DPU"
        ]


    def run(self) -> None:
        input_arrays = [t.ndarray for t in self.inputs]
        output_arrays = [t.ndarray for t in self.outputs]
        job_id = self.runner.execute_async(input_arrays, output_arrays)
        self.runner.wait(job_id)


    def reset(self) -> None:
        for bundle in self.inputs + self.outputs:
            bundle.ndarray.fill(0)


    def save_outputs(self, output_dir: Path) -> None:
        for bundle in self.outputs:
            output_scale = 2**(-bundle.xtensor.get_attr("fix_point"))
            array = (bundle.ndarray * output_scale).astype(np.float32)
            np.save(output_dir / f"{bundle.xtensor.name}.npy", array)


class PreProcessor:
    def __init__(self, dataset: str):
        """
        PreProcess like Voxelization + HardVFE.

        Args:
            dataset (str): "nuscenes" or  "contest".
        """
        if dataset == "nuscenes":
            self.voxel_size = [0.25, 0.25, 8]
            self.point_cloud_range = [-50.0, -50.0, -5.0, 50.0, 50.0, 3.0]
            lbounds = [-50, -50, -5, 0, 0]
            ubounds = [50, 50, 3, 255, 0.55]
        elif dataset == "contest":
            self.voxel_size = [0.2, 0.2, 8]
            self.point_cloud_range = [-51.2, -51.2, -5.0, 51.2, 51.2, 3.0]
            lbounds = [-50, -50, -5, 0, 0]
            ubounds = [50, 50, 3, 255, 0.50]
        else:
            raise NotImplementedError(f"Only nuscenes are contest are supported: {dataset}")
        self.mids = 0.5 * (torch.tensor(lbounds) + torch.tensor(ubounds)).view(1, 1, -1)
        self.scales = 1. / (0.5 * (torch.tensor(ubounds) - torch.tensor(lbounds)).view(1, 1, -1))


    # From /opt/open-mmlab/mmdetection3d/mmdet3d/models/voxel_encoders/utils_quant.py
    @staticmethod
    def get_paddings_indicator(actual_num, max_num, axis=0):
        """Create boolean mask by actually number of a padded tensor.

        Args:
            actual_num (torch.Tensor): Actual number of points in each voxel.
            max_num (int): Max number of points in each voxel

        Returns:
            torch.Tensor: Mask indicates which points are valid inside a voxel.
        """
        actual_num = torch.unsqueeze(actual_num, axis + 1)
        # tiled_actual_num: [N, M, 1]
        max_num_shape = [1] * len(actual_num.shape)
        max_num_shape[axis + 1] = -1
        max_num = torch.arange(
            max_num, dtype=torch.int, device=actual_num.device).view(max_num_shape)
        # tiled_actual_num: [[3,3,3,3,3], [4,4,4,4,4], [2,2,2,2,2]]
        # tiled_max_num: [[0,1,2,3,4], [0,1,2,3,4], [0,1,2,3,4]]
        paddings_indicator = actual_num.int() > max_num
        # paddings_indicator shape: [batch_size, max_num]
        return paddings_indicator


    def run(self, points: torch.Tensor, stacked_pillars: TensorBundle) -> torch.Tensor:
        # NOTE: In Vitis AI, BCHW -> BHWC conversion happens automatically during xmodel compilation.
        input_shape = tuple(stacked_pillars.xtensor.dims)
        max_voxel_num = input_shape[1]
        max_point_num = input_shape[2]
        # in_channel_num = input_shape[3]

        # From /opt/open-mmlab/mmdetection3d/mmdet3d/models/detectors/mvx_two_stage_quant.py:257
        t = voxelization(points, self.voxel_size, self.point_cloud_range, max_point_num, max_voxel_num)
        voxels = t[0] # voxels.shape == (actual_voxel_num, max_point_num, in_channel_num)
        coor = t[1] # coor.shape == (actual_voxel_num, len("zyx"))
        actual_point_nums = t[2] # actual_point_nums.shape == (actual_voxel_num,)

        # From /opt/open-mmlab/mmdetection3d/mmdet3d/models/voxel_encoders/voxel_encoder_quant.py:341
        voxel_feats = voxels - self.mids
        voxel_feats = voxel_feats * self.scales
        mask = self.get_paddings_indicator(actual_point_nums, max_point_num, axis=0)
        voxel_feats *= mask.unsqueeze(-1).type_as(voxel_feats)
        features = voxel_feats.contiguous().unsqueeze(0)

        # From /opt/open-mmlab/mmdetection3d/mmdet3d/apis/quant_test.py:65
        input_scale = 2**(stacked_pillars.xtensor.get_attr("fix_point"))
        ndarray = features.numpy() * input_scale
        actual_voxel_num = features.shape[1]
        stacked_pillars.ndarray[:, :actual_voxel_num, :, :] = ndarray.astype(np.int8)
        return coor


def middleprocess(learned_features: TensorBundle, coor: torch.Tensor, pseudo_image: TensorBundle):
    """
    From /opt/open-mmlab/mmdetection3d/mmdet3d/models/middle_encoders/pillar_scatter_quant.py:75
    """
    # NOTE: In Vitis AI, BCHW -> BHWC conversion happens automatically during xmodel compilation.
    height = pseudo_image.xtensor.dims[1]
    width = pseudo_image.xtensor.dims[2]
    in_channel_num = pseudo_image.xtensor.dims[3]
    canvas = torch.zeros(width * height, in_channel_num)

    # Calculate the indices to scatter the learned_features.
    indices = coor[:, 1] * width + coor[:, 2]
    indices = indices.type(torch.long)

    # Dequantize.
    output_scale = 2**(-learned_features.xtensor.get_attr("fix_point"))
    ndarray = np.squeeze(learned_features.ndarray) * output_scale

    # Scatter learned_features into canvas.
    # coor.shape[0] == actual_voxel_num
    voxel_features = torch.from_numpy(ndarray.astype(np.float32))
    canvas[indices,:] = voxel_features[:coor.shape[0], :]
    canvas = canvas.view(1, height, width, in_channel_num)

    # Quantize again.
    input_scale = 2**(pseudo_image.xtensor.get_attr("fix_point"))
    pseudo_image.ndarray[:,:,:,:] = canvas.numpy() * input_scale


class PostProcessor:
    def __init__(self, outputs: Sequence[TensorBundle], riscv_interface: Path):
        """
        PostProcess like CenterHead.

        Args:
            outputs (Sequence[TensorBundle]): TensorBundle objects from the second VartContext.
            riscv_interface (Path): .so file which performs the postprocess.
        """
        self.ndarrays = [] # Arrays to pass to C/C++.
        self.accessors = [] # Accessors to absorb the order difference b/w .xmodel and C/C++.

        # Set up self.ndarrays and self.accessors.
        mapping_table = [(1, "heatmap"),
                         (2, "height"),
                         (0, "dim"),
                         (4, "rot"),
                         (5, "vel"),
                         (3, "reg")]
        for module_idx in range(2):
            for relative_accessor, head_name in mapping_table:
                accessor = relative_accessor + len(mapping_table) * module_idx
                self.accessors.append(accessor)
                bundle = outputs[accessor]
                s = list(bundle.ndarray.shape)
                bchw = np.empty(s[0:1] + s[3:] + s[1:3], dtype=np.float32)
                self.ndarrays.append(bchw)

                # Confirm the tensor order is not changed in .xmodel.
                assert f"ModuleList_{module_idx}" in bundle.xtensor.name
                assert head_name in bundle.xtensor.name
        assert len(outputs) == len(self.ndarrays)
        self.__setup_ctypes(riscv_interface)


    def __setup_ctypes(self, riscv_interface: Path):
        self.riscv = np.ctypeslib.load_library(riscv_interface.name, str(riscv_interface.parent))
        flags = ['C_CONTIGUOUS']
        args = [ndpointer(dtype=a.dtype, ndim=a.ndim, flags=flags) for a in self.ndarrays]
        self.riscv.postprocess.argtypes = args
        self.riscv.postprocess.restype = ctypes.c_int


    def run(self, outputs: Sequence[TensorBundle]):
        # Dequant the output tensors then run the postprocess.
        for idx, accessor in enumerate(self.accessors):
            bundle = outputs[accessor]
            output_scale = 2**(-bundle.xtensor.get_attr("fix_point"))
            bhwc = (bundle.ndarray * output_scale).astype(np.float32)
            self.ndarrays[idx][:,:,:,:] = np.transpose(bhwc, (0, 3, 1, 2))
        self.riscv.postprocess(*self.ndarrays)


def predict(args: Namespace) -> None:
    # Set up VartContext and TensorBundle.
    first_context = VartContext(args.xmodels[0])
    second_context = VartContext(args.xmodels[1])
    preprocessor = PreProcessor(args.dataset)
    postprocessor = PostProcessor(second_context.outputs, args.riscv_interface)
    stacked_pillars = first_context.inputs[0]
    learned_features = first_context.outputs[0]
    pseudo_image = second_context.inputs[0]

    # Repeat the inference.
    with torch.inference_mode():
        for i in range(args.repeat):
            logging.info("%d: inference started", i)
            times = [None] * 6
            times[0]= timer()
            coor_tensor = preprocessor.run(args.points, stacked_pillars)
            times[1]= timer()
            first_context.run()
            times[2]= timer()
            middleprocess(learned_features, coor_tensor, pseudo_image)
            times[3]= timer()
            second_context.run()
            times[4]= timer()
            postprocessor.run(second_context.outputs)
            times[5]= timer()
            logging.info(f"{i}: overall_time(sec) = {times[-1] - times[0]}")
            for j in range(len(times)-1):
                logging.info(f" * times[{j+1}] - times[{j}] = {times[j+1] - times[j]}")
            if i != args.repeat - 1:
                first_context.reset()
                second_context.reset()

    # Save the output tensoers.
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir /= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir.mkdir(exist_ok=True)
        second_context.save_outputs(output_dir)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--log-level", type=logging.getLevelName, default="INFO", help="Log level")
    parser.add_argument("--repeat", type=int, default=1, help="Times to repeat the inference")
    parser.add_argument("--dataset", choices=["nuscenes", "contest"], default="contest", help="Configure the preprocess depending on the dataset.")
    parser.add_argument("--xmodels", nargs=2, help="2 .xmodel files of PointPillars")
    parser.add_argument("--riscv-interface", type=Path, default="../build/lib/libRiscvInterface.so", help=".so file of the postprocess")
    parser.add_argument("--output-dir", help="Directory to store the output files")
    parser.add_argument("points", type=torch.load, help="Pickle of LiDARPoints")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, format="%(asctime)s | %(levelname)8s | %(message)s")
    predict(args)


if __name__ == "__main__":
    main()
