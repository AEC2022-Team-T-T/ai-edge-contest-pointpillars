_base_ = ['./centerpoint_02pillar_second_secfpn_4x8_cyclic_20e_nus_autolabel.py']

model = dict(
    type='CenterPoint_quant',
    pts_voxel_encoder=dict(
        _delete_=True,
        type='HardVFE_deploy_trans_input_quant',
        in_channels=5,
        feat_channels=[64],
        voxel_size=(0.2, 0.2, 8),
        with_cluster_center=False,
        with_voxel_center=False,
        with_distance=False,
        point_cloud_range=[-51.2, -51.2, -5.0, 51.2, 51.2, 3.0],
        norm_cfg=dict(type='BN2d', eps=1e-3, momentum=0.01)),
    pts_middle_encoder=dict(
        type='PointPillarsScatter_deploy_quant', in_channels=64, output_shape=(512, 512)),
    pts_neck=dict(type='SECONDFPN_quant'),
    pts_bbox_head=dict(
        type='CenterHead_quant',
        seperate_head=dict(
            type='SeparateHead_quant')
    )
)
