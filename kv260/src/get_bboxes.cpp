// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

// This implementation is based on MMDetection3D
// https://github.com/open-mmlab/mmdetection3d/blob/v0.18.1/mmdet3d/models/dense_heads/centerpoint_head.py

#include "point_pillars/get_bboxes.hpp"

#include <math.h>
#include <stddef.h>

#include "point_pillars/bbox_coders.hpp"
#include "point_pillars/nms.hpp"

// Intermediate buffers
static float bboxes_before_nms[MAX_DECODE_NUM][BBOX_DIM];
static float scores_before_nms[MAX_DECODE_NUM];
static float labels_before_nms[MAX_DECODE_NUM];
static int32_t selected[MAX_DECODE_NUM];

static float _sigmoid(float value) { return 1.0f / (1.0f + expf(-value)); }

static void _xywhr2xyxyr(const float bboxes[], int32_t num_bboxes,
                         int32_t bbox_dim, float converted_bboxes[]) {
  const int32_t converted_bbox_dim = 5;
  for (auto i = 0; i < num_bboxes; ++i) {
    int32_t index = i * bbox_dim;
    const float bbox_xywhr[] = {bboxes[index + 0], bboxes[index + 1],
                                bboxes[index + 3], bboxes[index + 4],
                                bboxes[index + 6]};
    const auto half_w = bbox_xywhr[2] / 2.0f;
    const auto half_h = bbox_xywhr[3] / 2.0f;
    converted_bboxes[i * converted_bbox_dim + 0] = bbox_xywhr[0] - half_w;
    converted_bboxes[i * converted_bbox_dim + 1] = bbox_xywhr[1] - half_h;
    converted_bboxes[i * converted_bbox_dim + 2] = bbox_xywhr[0] + half_w;
    converted_bboxes[i * converted_bbox_dim + 3] = bbox_xywhr[1] + half_h;
    converted_bboxes[i * converted_bbox_dim + 4] = bbox_xywhr[4];
  }
}

int32_t centerpoint_get_bboxes(CenterPointOutput center_point_output[2],
                               float bboxes[][BBOX_DIM], float scores[],
                               int32_t labels[]) {
  int32_t num_bboxes = 0;

  for (auto task_id = 0; task_id < NUM_INPUTS; ++task_id) {
    const auto width = center_point_output[task_id].width;
    const auto height = center_point_output[task_id].height;

    // Apply sigmoid function to heatmap
    for (auto i = 0; i < height * width; ++i) {
      center_point_output[task_id].heatmap[i] =
          _sigmoid(center_point_output[task_id].heatmap[i]);
    }

    // Normalize dimension
    for (auto i = 0; i < 3 * height * width; ++i) {
      center_point_output[task_id].dim[i] =
          expf(center_point_output[task_id].dim[i]);
    }

    // Decode centerpoint outputs
    const CenterPointDecoderConfig config = {
        MAX_DECODE_NUM,
        DECODE_SCORE_THRESHOLD,
        OUT_SIZE_FACTOR,
        {VOXEL_SIZE[0], VOXEL_SIZE[1]},
        {PC_RANGE[0], PC_RANGE[1]},
        {POST_CENTER_RANGE[0], POST_CENTER_RANGE[1], POST_CENTER_RANGE[2],
         POST_CENTER_RANGE[3], POST_CENTER_RANGE[4], POST_CENTER_RANGE[5]}};
    int32_t num_decoded_bboxes = centerpoint_bbox_decode(
        center_point_output[task_id], config, bboxes_before_nms[0],
        scores_before_nms, labels_before_nms);

    // Apply non-maximum suppression
    float bboxes_for_nms[MAX_DECODE_NUM][BBOX_FOR_NMS_DIM];
    _xywhr2xyxyr(bboxes_before_nms[0], num_decoded_bboxes, BBOX_DIM,
                 bboxes_for_nms[0]);

    int32_t num_selected =
        nms(bboxes_for_nms[0], scores_before_nms, num_decoded_bboxes,
            BBOX_FOR_NMS_DIM, NMS_SCORE_THRESHOLD, NMS_THRESHOLD, selected);

    for (auto i = 0; i < num_selected; ++i) {
      if (i == NMS_MAX_NUM) break;
      auto selected_index = selected[i];
      for (auto j = 0; j < BBOX_DIM; ++j) {
        bboxes[num_bboxes][j] = bboxes_before_nms[selected_index][j];
      }
      scores[num_bboxes] = scores_before_nms[selected_index];
      labels[num_bboxes] = task_id;
      ++num_bboxes;
    }
  }

  for (auto i = 0; i < num_bboxes; ++i) {
    bboxes[i][2] = bboxes[i][2] - bboxes[i][5] * 0.5f;
  }

  return num_bboxes;
}
