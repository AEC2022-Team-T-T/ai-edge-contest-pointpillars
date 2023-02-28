// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#ifndef INCLUDE_POINT_PILLARS_GET_BBOXES_HPP_
#define INCLUDE_POINT_PILLARS_GET_BBOXES_HPP_

#include <stddef.h>
#include <stdint.h>

// Parameters
static constexpr size_t NUM_INPUTS = 2;
static constexpr size_t BBOX_DIM = 9;
static constexpr size_t BBOX_FOR_NMS_DIM = 5;
static constexpr size_t MAX_DECODE_NUM = 500;
static constexpr float DECODE_SCORE_THRESHOLD = 0.1f;
static constexpr float OUT_SIZE_FACTOR = 4.0f;
static constexpr float VOXEL_SIZE[2] = {0.2f, 0.2f};
static constexpr float PC_RANGE[2] = {-51.2f, -51.2f};
static constexpr float POST_CENTER_RANGE[6] = {-61.2f, -61.2f, -10.0f,
                                               61.2f,  61.2f,  10.0f};
static constexpr float NMS_SCORE_THRESHOLD = 0.1f;
static constexpr float NMS_THRESHOLD = 0.2f;
static constexpr size_t NMS_MAX_NUM = 83;

// Input struct
struct CenterPointOutput {
  float* heatmap;
  float* hei;
  float* dim;
  float* rot;
  float* vel;
  float* reg;
  int32_t width;
  int32_t height;
};

int32_t centerpoint_get_bboxes(
    CenterPointOutput center_point_output[NUM_INPUTS], float bboxes[][BBOX_DIM],
    float scores[], int32_t labels[]);

#endif  // INCLUDE_POINT_PILLARS_GET_BBOXES_HPP_
