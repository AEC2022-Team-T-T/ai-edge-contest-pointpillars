// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#ifndef INCLUDE_POINT_PILLARS_BBOX_CODERS_HPP_
#define INCLUDE_POINT_PILLARS_BBOX_CODERS_HPP_

#include <stdint.h>

#include "point_pillars/get_bboxes.hpp"

struct CenterPointDecoderConfig {
  int32_t max_decode_num;
  float score_threshold;
  float out_size_factor;
  float voxel_size[2];
  float pc_range[2];
  float post_center_range[6];
};

int32_t centerpoint_bbox_decode(const CenterPointOutput& center_point_output,
                                const CenterPointDecoderConfig& config,
                                float* bboxes, float* scores, float* labels);

#endif  // INCLUDE_POINT_PILLARS_BBOX_CODERS_HPP_
