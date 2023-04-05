# usage.md

## Table of Contents

* [Introduction](#introduction)  
  (This section)
* [Run PointPillars on KV260](#run-pointpillars-on-kv260)  
  (For those who just expect to run our inference application on KV260)
* [Train/Quantize PointPillars on x86-64 + NVIDIA GPUs](#trainquantize-pointpillars-on-x86-64--nvidia-gpus)  
  (For those who are interested in our training artifacts in [data/models](../data/models))
* [Set up DPU/VexRiscv for KV260](#set-up-dpuvexriscv-for-kv260)  
  (For those who are interested in how we configured KV260's PL)
* [Set up PetaLinux userland for inference application](#set-up-petalinux-userland-for-inference-application)  
  (For those who expect to set up PetaLinux userland to run our inference application)


## Run PointPillars on KV260

Burn your SD card with our [snapshot.img](https://1drv.ms/u/s!AlYlwqtjkSOsgQkHPEtQd3fUHnmO?e=I5fba7)
using the `dd` command then execute the following commands:

```Shell
$ sudo xmutil unloadapp # in sd.img, the password is "petalinux".
$ sudo xmutil loadapp riscv_dpu_test
$ REPO_ROOT=ai-edge-contest-pointpillars.git
$ cd $REPO_ROOT
$ cd kv260/python
$ sudo -E python pointpillars.py \
    --xmodels $REPO_ROOT/data/models/CenterPoint/0.xmodel $REPO_ROOT/data/models/CenterPoint/1.xmodel \
    $REPO_ROOT/data/inputs/em5VCQcE1fwFkTHI4wZ0Tm5y_0/points.pt
```

## Train/Quantize PointPillars on x86-64 + NVIDIA GPUs

### Docker image build

Execute `Makefile` as below:

```bash
$ make REGISTRY=your.docker-registry.com/ # Surely append "/".

```

### Training and Post-Training Quantization

1. Convert the dataset files (`train_0.zip` ... `train_4.zip`) to the nuScenes format using
  [mmdetection3d.git/tools/create_data.py](https://github.com/open-mmlab/mmdetection3d/blob/master/tools/create_data.py)

2. Locate the converted dataset on a large storage such as AWS FSx as below:

```bash
$ ls /mnt/fsx/public/ai-edge-contest/train/3d_labels/
maps                                                       nuscenes_infos_train.pkl
nuscenes_dbinfos_train.pkl                                 nuscenes_infos_val_mono3d.coco.json
nuscenes_gt_database                                       nuscenes_infos_val.pkl
nuscenes_infos_train_autolabel_centerpointvoxeladam02.pkl  samples
nuscenes_infos_train_mono3d.coco.json                      v1.0-trainval
```

3. Create your Kubeflow Notebook as below:
   - Docker Image:
     1. your.docker-registry.com/ai-edge-contest/pointpillars-code-gpu:latest-vai2.5.1
   - CPU / RAM: 6 CPUs / 55 Gi
   - Workspace Volume
     * \<Your own EBS\>:/home/vitis-ai-user
   - Data Volumes
     *  \<Your FSx\>:/mnt/fsx
   - Affinity / Tolerations
     * Affinity Config: p3.2xlarge (1GPU, 6vCPUs, 55GiB)

4. Clone this repository

```bash
$ cd /home/vitis-ai-user
$ mkdir repo
$ git clone <your docker registry>/ai-edge-contest-pointpillars.git repo/ai-edge-contest-pointpillars.git
```

5. Run `run_train.sh` as below:

```shell
$ conda activate vitis-ai-pytorch
$ cd repo/ai-edge-contest-pointpillars.git/
$ cd third_party/Xilinx/pt_pointpillars_nuscenes_40000_64_108G_2.5/
$ ./run_train.sh
```

- NOTE: If you encounter the error `cannot import name 'ball_query_ext' from 'mmdet3d.ops ball_query'`, it misses built `.so` files for cuda programs in `./code/mmdetection3d`. You could build them by running `python setup.py develop` in `./code/mmdetection3d`.

6. Run `run_quant.sh` as below:

```bash
$ conda activate vitis-ai-pytorch
$ cd repo/ai-edge-contest-pointpillars.git/
$ cd third_party/Xilinx/pt_pointpillars_nuscenes_40000_64_108G_2.5/
$ ./run_quant.sh
```

## Set up DPU/VexRiscv for KV260

We created our PetaLinux image (i.e. `.wic` file) and FPGA configuration of DPU/VexRiscv (e.g, `.xclbin`, `.dtbo`, etc) based on the following documents (we would like to thank all those who authored them):

* [Vitis Tutorials](https://xilinx.github.io/Vitis-Tutorials/2022-1/build/html/index.html)
* [KRIA XILINXのSOMボードのVitisプラットフォームの作り方(2022.1 版） - Qiita](https://qiita.com/basaro_k/items/e83128c265ae86801bbc)
* [KV260向けにVitisプラットフォームを作成してDPUを動かす その1 (Vitis 2022.1 + Vitis-AI v2.5) - Qiita](https://qiita.com/lp6m/items/df1b87b11f8275ee6210)
* [KV260向けにVitisプラットフォームを作成してDPUを動かす その2 (Vitis 2022.1 + Vitis-AI v2.5) - Qiita](https://qiita.com/lp6m/items/e45d957e43652695800a)
* [KV260でVexRiscv動作させた - lp6m’s blog](https://lp6m.hatenablog.com/entry/2022/10/01/011526)

Since Xilinx Vivado/Vitis project files include many developer information (e.g. paths, environment valuables),
we don't upload all of them.
Instead, we upload our `.wic` file and application files.
You should be able to set up the same environment as ours by following the steps below:

1. Download the `petalinux-sdimage.wic` from [here](https://1drv.ms/u/s!AlYlwqtjkSOsgQgxqJxun581_CJn?e=IdoKRd)
2. Burn your SD card with the above `.wic` using balenaEtcher on the host (e.g. Linux, macOS)
3. Set up Git LFS in this repository
4. Send `kv260/hardware/riscv_dpu_test` into KV260
5. Install this directory as below so that `xmutil` can load:

```bash
$ sudo mv riscv_dpu_test /lib/firmware/xilinx/
$ sudo echo "firmware: /lib/firmware/xilinx/riscv_dpu_test/binary_container_1.bin" > /etc/vart.conf
```

## Set up PetaLinux userland for inference application

### Cross-compile the post-processing module in x86-64

Our inference application is implemented in Python.
However, our post-processing module is implemented in C and RISC-V offloading is done inside this module.
After building `build/lib/libRiscvInterface.so` as below, put it next to the above `pointpillars.py` on KV260
so that our inference application can load it via `ctypes`:

```bash
# Install g++ for aarch64.
# You need to modify CXX and AR in Makefile if your g++ version is not 10
$ sudo apt install -y g++-10-aarch64-linux-gnu
$ cd kv260
$ make build-ctypes-interface
```

### Install PyTorch in KV260

Our inference application depends on PyTorch as well.
Install PyTorch into the python of KV260 as below:

```bash
$ python -m pip download torch==1.10.0 -f https://download.pytorch.org/whl/torch_stable.html
```