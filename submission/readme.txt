The directory structure of source.tar.gz is as below:

ai-edge-contest-pointpillars.git/
|-- data ### Test data for inference on KV260.
|   |-- inputs
|   `-- models # Copy from third_party/Xilinx/pt_pointpillars_nuscenes_40000_64_108G_2.5/quantized/0x101000017010404 .
|-- docker
|-- kv260 # Inference code on KV260.
|-- LICENSE
|-- LICENSE-THIRD-PARTY
|-- Makefile
|-- README.md
|-- submission # Submission files.
|   |-- area.txt
|   |-- readme.txt # This file.
|   |-- report.pdf
|   |-- result.txt
|   |-- sd.img
|   `-- usage.md
|-- third_party
|   |-- open-mmlab
|   `-- Xilinx
|       |-- pt_pointpillars_nuscenes_40000_64_108G_2.5 # Training/Quantization code.
|       |   |-- float
|       |   |   |-- pointpillars-nus.pth # Trained weights.
|       |   |   ...
|       |   |-- quantized # Quantization artifacts from Vitis AI.
|       |   |
|       |   ...
|       `-- Vitis-AI
`-- tools
