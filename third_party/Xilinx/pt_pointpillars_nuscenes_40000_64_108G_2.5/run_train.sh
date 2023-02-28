# Copyright 2019 Xilinx Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

export WANDB_BASE_URL="https://api.wb.swp-ml.tri-ad.global"
if [[ -z ${WANDB_API_KEY} ]]; then
	echo "Please set WANDB_API_KEY first!"
	exit 1
fi

export CUDA_VISIBLE_DEVICES=0

CONFIG=float/centerpoint_02pillar_second_secfpn_4x8_cyclic_20e_nus_autolabel.py
WORK_DIR=workspace/centerpoint

export W_QUANT=0
python3 code/mmdetection3d/tools/train.py ${CONFIG} --work-dir ${WORK_DIR}
