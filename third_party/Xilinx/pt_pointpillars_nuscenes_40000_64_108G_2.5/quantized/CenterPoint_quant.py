# GENETARED BY NNDCT, DO NOT EDIT!

import torch
import pytorch_nndct as py_nndct
class CenterPoint_quant(torch.nn.Module):
    def __init__(self):
        super(CenterPoint_quant, self).__init__()
        self.module_0 = py_nndct.nn.Module('const') #CenterPoint_quant::7894
        self.module_1 = py_nndct.nn.Input() #CenterPoint_quant::input_0
        self.module_2 = py_nndct.nn.Input() #CenterPoint_quant::input_1
        self.module_3 = py_nndct.nn.Input() #CenterPoint_quant::input_2
        self.module_4 = py_nndct.nn.quant_input() #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/QuantStub[quant]/input.1
        self.module_5 = py_nndct.nn.Conv2d(in_channels=5, out_channels=64, kernel_size=[1, 1], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/VFELayer_deploy_quant[vfe_layers]/ModuleList[0]/Conv2d[conv]/input.3
        self.module_6 = py_nndct.nn.ReLU(inplace=False) #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/VFELayer_deploy_quant[vfe_layers]/ModuleList[0]/ReLU[relu]/6470
        self.module_7 = py_nndct.nn.Module('max') #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/VFELayer_deploy_quant[vfe_layers]/ModuleList[0]/Max[max]/inputs.3
        self.module_8 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/DeQuantStub[dequant]/6475
        self.module_9 = py_nndct.nn.Module('squeeze') #CenterPoint_quant::CenterPoint_quant/HardVFE_deploy_trans_input_quant[pts_voxel_encoder]/voxel_features
        self.module_10 = py_nndct.nn.Module('zeros') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6495
        self.module_11 = py_nndct.nn.strided_slice() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6500
        self.module_12 = py_nndct.nn.Module('select') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6503
        self.module_13 = py_nndct.nn.Module('equal') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6505
        self.module_14 = py_nndct.nn.strided_slice() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6510
        self.module_15 = py_nndct.nn.Index() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6512
        self.module_16 = py_nndct.nn.strided_slice() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6517
        self.module_17 = py_nndct.nn.Module('select') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6520
        self.module_18 = py_nndct.nn.Module('elemwise_mul') #CenterPoint_quant::7895
        self.module_19 = py_nndct.nn.strided_slice() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6527
        self.module_20 = py_nndct.nn.Module('select') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6530
        self.module_21 = py_nndct.nn.Add() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6532
        self.module_22 = py_nndct.nn.Module('cast') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6538
        self.module_23 = py_nndct.nn.strided_slice() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6543
        self.module_24 = py_nndct.nn.Index() #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6546
        self.module_25 = py_nndct.nn.Module('stack') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/6558
        self.module_26 = py_nndct.nn.Module('reshape') #CenterPoint_quant::CenterPoint_quant/PointPillarsScatter_deploy_quant[pts_middle_encoder]/inputs
        self.module_27 = py_nndct.nn.quant_input() #CenterPoint_quant::CenterPoint_quant/QuantStub[quant]/input.7
        self.module_28 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/Conv2d[0]/input.9
        self.module_29 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/ReLU[2]/input.13
        self.module_30 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/Conv2d[3]/input.15
        self.module_31 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/ReLU[5]/input.19
        self.module_32 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/Conv2d[6]/input.21
        self.module_33 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/ReLU[8]/input.25
        self.module_34 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/Conv2d[9]/input.27
        self.module_35 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[0]/ReLU[11]/input.31
        self.module_36 = py_nndct.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[0]/input.33
        self.module_37 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[2]/input.37
        self.module_38 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[3]/input.39
        self.module_39 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[5]/input.43
        self.module_40 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[6]/input.45
        self.module_41 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[8]/input.49
        self.module_42 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[9]/input.51
        self.module_43 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[11]/input.55
        self.module_44 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[12]/input.57
        self.module_45 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[14]/input.61
        self.module_46 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/Conv2d[15]/input.63
        self.module_47 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[1]/ReLU[17]/input.67
        self.module_48 = py_nndct.nn.Conv2d(in_channels=128, out_channels=256, kernel_size=[3, 3], stride=[2, 2], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[0]/input.69
        self.module_49 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[2]/input.73
        self.module_50 = py_nndct.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[3]/input.75
        self.module_51 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[5]/input.79
        self.module_52 = py_nndct.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[6]/input.81
        self.module_53 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[8]/input.85
        self.module_54 = py_nndct.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[9]/input.87
        self.module_55 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[11]/input.91
        self.module_56 = py_nndct.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[12]/input.93
        self.module_57 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[14]/input.97
        self.module_58 = py_nndct.nn.Conv2d(in_channels=256, out_channels=256, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/Conv2d[15]/input.99
        self.module_59 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECOND[pts_backbone]/Sequential[blocks]/ModuleList[2]/ReLU[17]/6983
        self.module_60 = py_nndct.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[0]/Conv2d[0]/input.103
        self.module_61 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[0]/ReLU[2]/7013
        self.module_62 = py_nndct.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=[1, 1], stride=[1, 1], padding=[0, 0], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[1]/Conv2d[0]/input.107
        self.module_63 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[1]/ReLU[2]/7039
        self.module_64 = py_nndct.nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=[2, 2], stride=[2, 2], padding=[0, 0], output_padding=[0, 0], groups=1, bias=True, dilation=[1, 1]) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[2]/ConvTranspose2d[0]/input.111
        self.module_65 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Sequential[deblocks]/ModuleList[2]/ReLU[2]/7065
        self.module_66 = py_nndct.nn.Cat() #CenterPoint_quant::CenterPoint_quant/SECONDFPN_quant[pts_neck]/Cat[cat]/input.115
        self.module_67 = py_nndct.nn.Conv2d(in_channels=384, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/ConvModule[shared_conv]/Conv2d[conv]/input.117
        self.module_68 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/ConvModule[shared_conv]/ReLU[activate]/input.121
        self.module_69 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[reg]/ConvModule[0]/Conv2d[conv]/input.123
        self.module_70 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[reg]/ConvModule[0]/ReLU[activate]/input.127
        self.module_71 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[reg]/Conv2d[1]/ip.1
        self.module_72 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[height]/ConvModule[0]/Conv2d[conv]/input.129
        self.module_73 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[height]/ConvModule[0]/ReLU[activate]/input.133
        self.module_74 = py_nndct.nn.Conv2d(in_channels=64, out_channels=1, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[height]/Conv2d[1]/ip.3
        self.module_75 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[dim]/ConvModule[0]/Conv2d[conv]/input.135
        self.module_76 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[dim]/ConvModule[0]/ReLU[activate]/input.139
        self.module_77 = py_nndct.nn.Conv2d(in_channels=64, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[dim]/Conv2d[1]/ip.5
        self.module_78 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[rot]/ConvModule[0]/Conv2d[conv]/input.141
        self.module_79 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[rot]/ConvModule[0]/ReLU[activate]/input.145
        self.module_80 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[rot]/Conv2d[1]/ip.7
        self.module_81 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[vel]/ConvModule[0]/Conv2d[conv]/input.147
        self.module_82 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[vel]/ConvModule[0]/ReLU[activate]/input.151
        self.module_83 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[vel]/Conv2d[1]/ip.9
        self.module_84 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[heatmap]/ConvModule[0]/Conv2d[conv]/input.153
        self.module_85 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[heatmap]/ConvModule[0]/ReLU[activate]/input.157
        self.module_86 = py_nndct.nn.Conv2d(in_channels=64, out_channels=1, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[0]/Sequential[heatmap]/Conv2d[1]/ip.11
        self.module_87 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[reg]/ConvModule[0]/Conv2d[conv]/input.159
        self.module_88 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[reg]/ConvModule[0]/ReLU[activate]/input.163
        self.module_89 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[reg]/Conv2d[1]/ip.13
        self.module_90 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[height]/ConvModule[0]/Conv2d[conv]/input.165
        self.module_91 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[height]/ConvModule[0]/ReLU[activate]/input.169
        self.module_92 = py_nndct.nn.Conv2d(in_channels=64, out_channels=1, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[height]/Conv2d[1]/ip.15
        self.module_93 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[dim]/ConvModule[0]/Conv2d[conv]/input.171
        self.module_94 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[dim]/ConvModule[0]/ReLU[activate]/input.175
        self.module_95 = py_nndct.nn.Conv2d(in_channels=64, out_channels=3, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[dim]/Conv2d[1]/ip.17
        self.module_96 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[rot]/ConvModule[0]/Conv2d[conv]/input.177
        self.module_97 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[rot]/ConvModule[0]/ReLU[activate]/input.181
        self.module_98 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[rot]/Conv2d[1]/ip.19
        self.module_99 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[vel]/ConvModule[0]/Conv2d[conv]/input.183
        self.module_100 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[vel]/ConvModule[0]/ReLU[activate]/input.187
        self.module_101 = py_nndct.nn.Conv2d(in_channels=64, out_channels=2, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[vel]/Conv2d[1]/ip.21
        self.module_102 = py_nndct.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[heatmap]/ConvModule[0]/Conv2d[conv]/input.189
        self.module_103 = py_nndct.nn.ReLU(inplace=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[heatmap]/ConvModule[0]/ReLU[activate]/input
        self.module_104 = py_nndct.nn.Conv2d(in_channels=64, out_channels=1, kernel_size=[3, 3], stride=[1, 1], padding=[1, 1], dilation=[1, 1], groups=1, bias=True) #CenterPoint_quant::CenterPoint_quant/CenterHead_quant[pts_bbox_head]/SeparateHead_quant[task_heads]/ModuleList[1]/Sequential[heatmap]/Conv2d[1]/ip
        self.module_105 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7662
        self.module_106 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7665
        self.module_107 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7668
        self.module_108 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7671
        self.module_109 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7674
        self.module_110 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7677
        self.module_111 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7680
        self.module_112 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7683
        self.module_113 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7686
        self.module_114 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7689
        self.module_115 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7692
        self.module_116 = py_nndct.nn.dequant_output() #CenterPoint_quant::CenterPoint_quant/DeQuantStub[dequant]/7695

    def forward(self, *args):
        output_module_0 = self.module_0(data=512.0, dtype=torch.float, device='cpu')
        output_module_1 = self.module_1(input=args[0])
        output_module_2 = self.module_2(input=args[1])
        output_module_3 = self.module_3(input=args[2])
        output_module_1 = self.module_4(input=output_module_1)
        output_module_1 = self.module_5(output_module_1)
        output_module_1 = self.module_6(output_module_1)
        output_module_7_0,output_module_7_1 = self.module_7(input=output_module_1, dim=(3), keepdim=True)
        output_module_7_0 = self.module_8(input=output_module_7_0)
        output_module_7_0 = self.module_9(input=output_module_7_0)
        output_module_10 = self.module_10(size=[64,262144], dtype=torch.float, device='cpu')
        output_module_11 = self.module_11(input=output_module_3, dim=[0], start=[0], end=[9223372036854775807], step=[1])
        output_module_11 = self.module_12(input=output_module_11, dim=1, index=0)
        output_module_11 = self.module_13(input=output_module_11, other=0)
        output_module_14 = self.module_14(input=output_module_3, dim=[1], start=[0], end=[9223372036854775807], step=[1])
        output_module_14 = self.module_15(input=output_module_14, index=[output_module_11])
        output_module_16 = self.module_16(input=output_module_14, dim=[0], start=[0], end=[9223372036854775807], step=[1])
        output_module_16 = self.module_17(input=output_module_16, dim=1, index=2)
        output_module_16 = self.module_18(input=output_module_16, other=output_module_0)
        output_module_19 = self.module_19(input=output_module_14, dim=[0], start=[0], end=[9223372036854775807], step=[1])
        output_module_19 = self.module_20(input=output_module_19, dim=1, index=3)
        output_module_16 = self.module_21(input=output_module_16, other=output_module_19, alpha=1)
        output_module_16 = self.module_22(input=output_module_16, dtype=torch.int64)
        output_module_7_0 = self.module_23(input=output_module_7_0, dim=[0], start=[0], end=[9223372036854775807], step=[1])
        output_module_7_0 = self.module_24(input=output_module_7_0, index=[None,output_module_11])
        output_module_10[:,output_module_16] = output_module_7_0
        output_module_10 = self.module_25(tensors=[output_module_10], dim=0)
        output_module_10 = self.module_26(input=output_module_10, shape=[1,64,512,512])
        output_module_10 = self.module_27(input=output_module_10)
        output_module_10 = self.module_28(output_module_10)
        output_module_10 = self.module_29(output_module_10)
        output_module_10 = self.module_30(output_module_10)
        output_module_10 = self.module_31(output_module_10)
        output_module_10 = self.module_32(output_module_10)
        output_module_10 = self.module_33(output_module_10)
        output_module_10 = self.module_34(output_module_10)
        output_module_10 = self.module_35(output_module_10)
        output_module_36 = self.module_36(output_module_10)
        output_module_36 = self.module_37(output_module_36)
        output_module_36 = self.module_38(output_module_36)
        output_module_36 = self.module_39(output_module_36)
        output_module_36 = self.module_40(output_module_36)
        output_module_36 = self.module_41(output_module_36)
        output_module_36 = self.module_42(output_module_36)
        output_module_36 = self.module_43(output_module_36)
        output_module_36 = self.module_44(output_module_36)
        output_module_36 = self.module_45(output_module_36)
        output_module_36 = self.module_46(output_module_36)
        output_module_36 = self.module_47(output_module_36)
        output_module_48 = self.module_48(output_module_36)
        output_module_48 = self.module_49(output_module_48)
        output_module_48 = self.module_50(output_module_48)
        output_module_48 = self.module_51(output_module_48)
        output_module_48 = self.module_52(output_module_48)
        output_module_48 = self.module_53(output_module_48)
        output_module_48 = self.module_54(output_module_48)
        output_module_48 = self.module_55(output_module_48)
        output_module_48 = self.module_56(output_module_48)
        output_module_48 = self.module_57(output_module_48)
        output_module_48 = self.module_58(output_module_48)
        output_module_48 = self.module_59(output_module_48)
        output_module_60 = self.module_60(output_module_10)
        output_module_60 = self.module_61(output_module_60)
        output_module_62 = self.module_62(output_module_36)
        output_module_62 = self.module_63(output_module_62)
        output_module_48 = self.module_64(output_module_48)
        output_module_48 = self.module_65(output_module_48)
        output_module_60 = self.module_66(dim=1, tensors=[output_module_60,output_module_62,output_module_48])
        output_module_60 = self.module_67(output_module_60)
        output_module_60 = self.module_68(output_module_60)
        output_module_69 = self.module_69(output_module_60)
        output_module_69 = self.module_70(output_module_69)
        output_module_69 = self.module_71(output_module_69)
        output_module_72 = self.module_72(output_module_60)
        output_module_72 = self.module_73(output_module_72)
        output_module_72 = self.module_74(output_module_72)
        output_module_75 = self.module_75(output_module_60)
        output_module_75 = self.module_76(output_module_75)
        output_module_75 = self.module_77(output_module_75)
        output_module_78 = self.module_78(output_module_60)
        output_module_78 = self.module_79(output_module_78)
        output_module_78 = self.module_80(output_module_78)
        output_module_81 = self.module_81(output_module_60)
        output_module_81 = self.module_82(output_module_81)
        output_module_81 = self.module_83(output_module_81)
        output_module_84 = self.module_84(output_module_60)
        output_module_84 = self.module_85(output_module_84)
        output_module_84 = self.module_86(output_module_84)
        output_module_87 = self.module_87(output_module_60)
        output_module_87 = self.module_88(output_module_87)
        output_module_87 = self.module_89(output_module_87)
        output_module_90 = self.module_90(output_module_60)
        output_module_90 = self.module_91(output_module_90)
        output_module_90 = self.module_92(output_module_90)
        output_module_93 = self.module_93(output_module_60)
        output_module_93 = self.module_94(output_module_93)
        output_module_93 = self.module_95(output_module_93)
        output_module_96 = self.module_96(output_module_60)
        output_module_96 = self.module_97(output_module_96)
        output_module_96 = self.module_98(output_module_96)
        output_module_99 = self.module_99(output_module_60)
        output_module_99 = self.module_100(output_module_99)
        output_module_99 = self.module_101(output_module_99)
        output_module_102 = self.module_102(output_module_60)
        output_module_102 = self.module_103(output_module_102)
        output_module_102 = self.module_104(output_module_102)
        output_module_69 = self.module_105(input=output_module_69)
        output_module_72 = self.module_106(input=output_module_72)
        output_module_75 = self.module_107(input=output_module_75)
        output_module_78 = self.module_108(input=output_module_78)
        output_module_81 = self.module_109(input=output_module_81)
        output_module_84 = self.module_110(input=output_module_84)
        output_module_87 = self.module_111(input=output_module_87)
        output_module_90 = self.module_112(input=output_module_90)
        output_module_93 = self.module_113(input=output_module_93)
        output_module_96 = self.module_114(input=output_module_96)
        output_module_99 = self.module_115(input=output_module_99)
        output_module_102 = self.module_116(input=output_module_102)
        return output_module_69,output_module_72,output_module_75,output_module_78,output_module_81,output_module_84,output_module_87,output_module_90,output_module_93,output_module_96,output_module_99,output_module_102
