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


export CUDA_VISIBLE_DEVICES=0

WORK_DIR=float
CONFIG=float/centerpoint_02pillar_second_secfpn_4x8_cyclic_20e_nus_autolabel.py
WEIGHTS=${WORK_DIR}/centerpoint_pillar.pth

export W_QUANT=0
python code/mmdetection3d/tools/eval.py ${CONFIG} ${WEIGHTS} --eval mAP
