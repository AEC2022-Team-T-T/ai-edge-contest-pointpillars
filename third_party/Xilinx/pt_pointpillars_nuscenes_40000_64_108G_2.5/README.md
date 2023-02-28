### Contents
1. [Installation](#installation)
2. [Preparation](#preparation)
3. [Train/Eval](#traineval)
4. [Performance](#performance)
5. [Model_info](#model_info)
6. [Acknowledgement](#acknowledgement)

### Installation

1. Environment requirement
    - anaconda3
    - python 3.6
    - pytorch 1.4
    - mmcv, mmdetection, mmdetection3d etc.
    - vai_q_pytorch(Optional, required for quantization)
    - XIR Python frontend (Optional, required for dumping xmodel)

2. Installation with Docker

   First refer to [vitis-ai](https://github.com/Xilinx/Vitis-AI/tree/master/) to obtain the docker image. Remember to use the gpu docker (with pytorch=1.4) for this model.
   ```bash
   conda activate vitis-ai-pytorch
   # If you use the docker with torch=1.4, then no need to install it again
   # pip install --user torch==1.4.0+cu100 torchvision==0.5.0+cu100 -c pytorch
    
   # nvcc is required
   sudo apt-get update && sudo apt-get install cuda-toolkit-10-0
   export CUDA_HOME=/usr/local/cuda    
   # the default gcc version is gcc-9, we should config to gcc-7 to make it compatible with cudatoolkit-10.0
   sudo update-alternatives --config gcc

   cd code

   # install mmcv 1.15(commit 23b2bdbf52c8c4960dc696ec35901146f839fd6d)：
   # git clone https://github.com/open-mmlab/mmcv.git
   cd mmcv
   # git checkout 23b2bdbf52c8c4960dc6
   MMCV_WITH_OPS=1 pip install --user -e .  # package mmcv-full will be installed after this step
   cd ..

   # install mmdetection 2.5.0 (commit eb7bfbc62658b60e5be8bb00a40d5e3018971f78):
   # git clone https://github.com/open-mmlab/mmdetection.git
   cd mmdetection
   # git checkout eb7bfbc62658b60e5be8
   pip install --user -r requirements/build.txt
   pip install --user -v -e .  # or "python setup.py develop"
   cd ..

   # our code is derived from mmdetection3d 0.6.1 (commit 64a8c455bc900c792e68b0ac9c1fe89ab168d7d4):
   cd mmdetection3d
   pip install --user -r requirements.txt
   pip install --user -v -e .  # or "python setup.py develop"
   cd ..

   cd ..

   # to avoid bug in mmdetection3d caused by the conflic bewteen pycocotools and mmpycocotools
   pip uninstall pycocotools
   pip uninstall mmpycocotools
   pip install --user mmpycocotools

   export PYTHONPATH=${PWD}/code/mmdetection3d:${PYTHONPATH}
   ```

### Preparation

1. Dataset description

nuScenes V1.0 includes 1000 driving scenes and 23 object classes are annotated with accurate 3D bounding boxes at 2Hz over the entire dataset. According to the official protocal, 850 scenes for training(700) and validation(150), and 150 scenes for testing. For the 23 object classes, similar classes are merged and rare classes are removed, which results in 10 classes for the [detection challenge](https://www.nuscenes.org/object-detection). Please refer to [nuScenes overview](https://www.nuscenes.org/nuscenes) for more details.

2. Download nuScenes V1.0 full dataset data [HERE]( https://www.nuscenes.org/download). 
  ```plain
  |
  ├── data
  │   ├── nuscenes
  │   │   ├── maps
  │   │   ├── samples
  │   │   ├── sweeps
  │   │   ├── v1.0-test
  |   |   ├── v1.0-trainval
  ```
  Prepare nuscenes data by running
  ```bash
  python code/mmdetection3d/tools/create_data.py nuscenes --root-path ./data/nuscenes --out-dir ./data/nuscenes --extra-tag nuscenes
  ```

### Train/Eval

1. Evaluation
  - Configure the data path in `float/nus-3d.py`.
  ```python
  ...
  data = dict(
    ...
    train=dict(
        ...
        ann_file=data_root + 'nuscenes_infos_train.pkl',
        ...),
    val=dict(
        ...
        ann_file=data_root + 'nuscenes_infos_val.pkl',
        ...),
  ```
  - Execute run_eval.sh.
  ```shell
  bash run_eval.sh
  ```

2. Training
  - The main configuration `hv_pointpillars_secfpn_sbn-all_4x4_2x_nus-3d.py` includes related configuration files in the field `_base_`. If variables defined in the files in `_base_` are reset in `hv_pointpillars_secfpn_sbn-all_4x4_2x_nus-3d.py`, then the original configuration will be overridden.
  - Execute run_train.sh.
  ```shell
  bash run_train.sh
  ```

3. Model quantization
  - Note: for quantization, if you do the calibration (with fast-finetune) yourself, the accuracy of quantized model may slightly differ from the reported, for the reason that we random sample an subset with 300 samples for fast-finetune. For more details, you could check the arguments in `code/mmdetection3d/tools/quant.py`.
  ```shell
  bash run_quant.sh
  ```

### Performance

|Model|mAP|NDS|
|-|-|-|
|float|42.2|55.1|
|quant(with fast-finetune trick)|40.5|53.0|

### Model_info

1. Data preprocess
  ```
  Voxelization on BEV -> pillars
  Utilize PointNet on each pillars
  Generate peseudo BEV image
  ``` 

### Acknowledgement
This repo is derived from [mmdetection3d](https://github.com/open-mmlab/mmdetection3d.git), [mmdetection](https://github.com/open-mmlab/mmdetection.git) and [mmcv](https://github.com/open-mmlab/mmcv.git), many thanks to open-mmlab for the contribution to the community.
