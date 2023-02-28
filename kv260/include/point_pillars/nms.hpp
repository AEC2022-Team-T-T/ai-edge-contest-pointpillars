// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#ifndef INCLUDE_POINT_PILLARS_NMS_HPP_
#define INCLUDE_POINT_PILLARS_NMS_HPP_

#include <stdint.h>

struct ScoreIndex {
  float score;
  int32_t index;
};

int32_t nms(const float bboxes[], const float scores[], int32_t num_bboxes,
            int32_t bbox_dim, float score_threshold, float nms_threshold,
            int32_t selected[]);

#endif  // INCLUDE_POINT_PILLARS_NMS_HPP_
