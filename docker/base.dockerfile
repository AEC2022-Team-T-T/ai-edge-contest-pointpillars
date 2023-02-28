ARG PYTORCH="1.10.0"
ARG CUDA="11.0"
ARG CUDNN="8"
ARG BASE_IMG=<base>
FROM $BASE_IMG

ENV TORCH_CUDA_ARCH_LIST="6.0 6.1 7.0+PTX"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"

# To fix GPG key error when running apt-get update
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# Insall general packages.
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 git-lfs time \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# This paragraph was required to enable CUDA in MMCV.
# See also https://mmcv.readthedocs.io/en/master/faq.html .
ENV FORCE_CUDA=1
RUN apt-get update && apt-get install -y cuda-toolkit-11-0 && apt-get clean && rm -rf /var/lib/apt/lists/*

# In "vitis-ai-gpu", following user is used for miniconda installation,
USER vitis-ai-user
WORKDIR /home/vitis-ai-user

# Trick for not repeating `conda activate vitis-ai-pytorch`.
RUN echo ". /etc/profile.d/conda.sh; conda activate vitis-ai-pytorch" > /tmp/.profile
ENV BASH_ENV=/tmp/.profile

# Install MMCV, MMDetection and MMdetection3d
COPY --chown=vitis-ai-user:vitis-ai-group third_party/Xilinx/pt_pointpillars_nuscenes_40000_64_108G_2.5/code /opt/open-mmlab
RUN cd /opt/open-mmlab/mmcv && \
    MMCV_WITH_OPS=1 pip install -e .
RUN cd /opt/open-mmlab/mmdetection && \
    pip install -r requirements/build.txt && \
    pip install -v -e .
RUN cd /opt/open-mmlab/mmdetection3d && \
    pip install -r requirements.txt && \
    pip install --no-cache-dir -v -e .

# See here: https://mmdetection3d.readthedocs.io/en/v0.12.0/faq.html#mmcv-mmdet-mmdet3d-installation
RUN pip uninstall -y 'pycocotools' 'mmpycocotools' && \
    pip install 'mmpycocotools' 'numpy<1.20.0' --force --no-deps

# Install required packages
COPY --chown=vitis-ai-user:vitis-ai-group docker/requirements.txt ./
RUN pip install -r requirements.txt && \
    rm requirements.txt

# Patch data loader in nuscenes
# This patch is a workaround patch to deal with the noisy data using in edge contest in eval stage.
# It won't affect the training of public nuScenes data.
COPY --chown=vitis-ai-user:vitis-ai-group docker/loaders.patch ./
RUN patch /opt/vitis_ai/conda/envs/vitis-ai-pytorch/lib/python3.7/site-packages/nuscenes/eval/common/loaders.py loaders.patch && \
    rm loaders.patch

# To switch to "vitis-ai-user" using `gosu` from `docker_run.sh`,
# revert to the "root".
ENV BASH_ENV=
USER root
