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
export CUDA_HOME=/usr/local/cuda
export W_QUANT=1
readonly WORK_DIR=float
readonly Q_CONFIG=${WORK_DIR}/centerpoint_02pillar_second_secfpn_4x8_cyclic_20e_nus_autolabel_hardvfe_quant.py
readonly WEIGHTS=${WORK_DIR}/centerpoint_pillar.pth
readonly DEBUG_OPTS=${DEBUG_OPTS:-}
readonly ARCH=${1:-0x101000017010404}

# Note: for this model, direct 8bit-quantization gets an accuracy that is not so satisfactory, so we use the fast-finetune trick
# Q_DIR=quantized
# echo "Calibrating model quantization..."
# MODE='calib'
# python code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --calib_len 400
# echo "Testing quantized model..."
# MODE='test'
# python code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --eval 'bbox'
# echo "Dumping xmodel..."
# python code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --dump_xmodel

# Note: for this model, utilize the fast-finetune trick could improve the accuracy of quantized model
Q_DIR=quantized
echo "Calibrating model quantization..."
MODE='calib'
${PRECOMMAND:-time} python ${DEBUG_OPTS} code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --calib_len 100 --fast_finetune
echo "Testing quantized model..."
MODE='test'
${PRECOMMAND:-time} python ${DEBUG_OPTS} code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --fast_finetune --eval 'bbox'
echo "Dumping xmodel..."
${PRECOMMAND:-time} python ${DEBUG_OPTS} code/mmdetection3d/tools/quant.py ${Q_CONFIG} ${WEIGHTS} --quant_mode ${MODE} --quant_dir ${Q_DIR} --fast_finetune --dump_xmodel

echo "Compile to XIR..."
compiled_dir=${Q_DIR}/${ARCH}
arch_json=$(mktemp --suffix=.json)
echo {\"fingerprint\": \"${ARCH}\"} > ${arch_json}
for xmodel in $(find . -path "./${Q_DIR}/*_int.xmodel"); do
  net_name=$(basename ${xmodel})
  net_name=${net_name::-11} # 11 is from "_int.xmodel"
  net_dir=${compiled_dir}/${net_name}
  ${PRECOMMAND:-time} mkdir -p ${net_dir}
  ${PRECOMMAND:-time} vai_c_xir --xmodel ${xmodel} --arch ${arch_json} --net_name ${net_name} --output_dir ${net_dir}
done
