// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

// This implementation is based on MMDetection3D
// https://github.com/open-mmlab/mmdetection3d/blob/v0.18.1/mmdet3d/core/bbox/coders/delta_xyzwhlr_bbox_coder.py

#include "point_pillars/bbox_coders.hpp"

#include <assert.h>
#include <math.h>

static constexpr size_t MAX_SCORE_NUM = 128 * 128;

struct Peak {
  float score;
  int32_t x;
  int32_t y;
};

static int32_t _min(int32_t lhs, int32_t rhs) {
  return (lhs > rhs) ? rhs : lhs;
}

static int _compare(const void* lhs, const void* rhs) {
  const Peak* lhs_score_index = static_cast<const Peak*>(lhs);
  const Peak* rhs_score_index = static_cast<const Peak*>(rhs);
  if (rhs_score_index->score > lhs_score_index->score) {
    return 1;
  }
  if (rhs_score_index->score < lhs_score_index->score) {
    return -1;
  }
  return 0;
}

static void topk(const float* scores, int32_t width, int32_t height, int32_t k,
                 float* topk_scores, int32_t* topk_labels, float* topk_xs,
                 float* topk_ys) {
  assert(width * height <= MAX_SCORE_NUM);

  Peak peaks[MAX_SCORE_NUM] = {};
  for (auto y = 0; y < height; ++y) {
    for (auto x = 0; x < width; ++x) {
      peaks[y * width + x] = {scores[y * width + x], x, y};
    }
  }
  qsort(peaks, sizeof(peaks) / sizeof(Peak), sizeof(Peak), _compare);

  for (auto i = 0; i < _min(width * height, k); ++i) {
    topk_scores[i] = peaks[i].score;
    topk_labels[i] = 0;
    topk_xs[i] = peaks[i].x;
    topk_ys[i] = peaks[i].y;
  }
}

int32_t centerpoint_bbox_decode(const CenterPointOutput& center_point_output,
                                const CenterPointDecoderConfig& config,
                                float* bboxes, float* scores, float* labels) {
  const int32_t image_size =
      center_point_output.width * center_point_output.height;

  float topk_scores[MAX_DECODE_NUM] = {};
  int32_t topk_classes[MAX_DECODE_NUM] = {};
  float topk_xs[MAX_DECODE_NUM] = {};
  float topk_ys[MAX_DECODE_NUM] = {};
  topk(center_point_output.heatmap, center_point_output.width,
       center_point_output.height, config.max_decode_num, topk_scores,
       topk_classes, topk_xs, topk_ys);

  const int32_t score_num =
      _min(center_point_output.width * center_point_output.height,
           config.max_decode_num);

  int32_t num_bboxes = 0;
  for (auto i = 0; i < score_num; ++i) {
    const auto score = topk_scores[i];
    if (score <= config.score_threshold) continue;
    auto x = topk_xs[i];
    auto y = topk_ys[i];
    const auto index_x = static_cast<int32_t>(x);
    const auto index_y = static_cast<int32_t>(y);
    x = (x + center_point_output
                 .reg[index_y * center_point_output.width + index_x]) *
            config.out_size_factor * config.voxel_size[0] +
        config.pc_range[0];
    y = (y +
         center_point_output
             .reg[image_size + index_y * center_point_output.width + index_x]) *
            config.out_size_factor * config.voxel_size[1] +
        config.pc_range[1];
    const auto hei =
        center_point_output.hei[index_y * center_point_output.width + index_x];
    if (x < config.post_center_range[0] || y < config.post_center_range[1] ||
        hei < config.post_center_range[2] || x > config.post_center_range[3] ||
        y > config.post_center_range[4] || hei > config.post_center_range[5]) {
      continue;
    }
    const auto rot = atan2f(
        center_point_output.rot[index_y * center_point_output.width + index_x],
        center_point_output
            .rot[image_size + index_y * center_point_output.width + index_x]);

    const auto dim0 =
        center_point_output.dim[index_y * center_point_output.width + index_x];
    const auto dim1 =
        center_point_output
            .dim[image_size + index_y * center_point_output.width + index_x];
    const auto dim2 =
        center_point_output.dim[2 * image_size +
                                index_y * center_point_output.width + index_x];
    const auto vel0 =
        center_point_output.vel[index_y * center_point_output.width + index_x];
    const auto vel1 =
        center_point_output
            .vel[image_size + index_y * center_point_output.width + index_x];
    bboxes[num_bboxes * 9 + 0] = x;
    bboxes[num_bboxes * 9 + 1] = y;
    bboxes[num_bboxes * 9 + 2] = hei;
    bboxes[num_bboxes * 9 + 3] = dim0;
    bboxes[num_bboxes * 9 + 4] = dim1;
    bboxes[num_bboxes * 9 + 5] = dim2;
    bboxes[num_bboxes * 9 + 6] = rot;
    bboxes[num_bboxes * 9 + 7] = vel0;
    bboxes[num_bboxes * 9 + 8] = vel1;
    scores[num_bboxes] = score;
    labels[num_bboxes] = topk_classes[i];
    num_bboxes++;
  }
  return num_bboxes;
}
