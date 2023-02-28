// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#include <math.h>
#include <string.h>

#include "./utility.hpp"
#include "catch2/catch.hpp"
#include "point_pillars/get_bboxes.hpp"

TEST_CASE("get_bbox of CenterPointHead is applied correctly", "[get_bbox]") {
  static constexpr size_t kWidth = 128;
  static constexpr size_t kHeight = 128;
  static constexpr size_t kNumInputs = 2;

  float heatmap0[1 * kHeight * kWidth] = {};
  float hei0[1 * kHeight * kWidth] = {};
  float dim0[3 * kHeight * kWidth] = {};
  float rot0[2 * kHeight * kWidth] = {};
  float vel0[2 * kHeight * kWidth] = {};
  float reg0[2 * kHeight * kWidth] = {};
  float heatmap1[1 * kHeight * kWidth] = {};
  float hei1[1 * kHeight * kWidth] = {};
  float dim1[3 * kHeight * kWidth] = {};
  float rot1[2 * kHeight * kWidth] = {};
  float vel1[2 * kHeight * kWidth] = {};
  float reg1[2 * kHeight * kWidth] = {};
  float* input_buffers[2][6] = {{heatmap0, hei0, dim0, rot0, vel0, reg0},
                                {heatmap1, hei1, dim1, rot1, vel1, reg1}};

  CenterPointOutput inputs[kNumInputs] = {};
  char file_base[6][8] = {"heatmap", "height", "dim", "rot", "vel", "reg"};
  for (auto n = 0; n < kNumInputs; ++n) {
    for (auto i = 0; i < 6; ++i) {
      char file_name[64] = {};
      snprintf(file_name, sizeof(file_name), "test/bin/get_bboxes/%s%d.bin",
               file_base[i], n);
      ReadBinaryFile(file_name, input_buffers[n][i]);
      switch (i) {
        case 0:
          inputs[n].heatmap = input_buffers[n][i];
          break;
        case 1:
          inputs[n].hei = input_buffers[n][i];
          break;
        case 2:
          inputs[n].dim = input_buffers[n][i];
          break;
        case 3:
          inputs[n].rot = input_buffers[n][i];
          break;
        case 4:
          inputs[n].vel = input_buffers[n][i];
          break;
        case 5:
          inputs[n].reg = input_buffers[n][i];
          break;
      }
    }
    inputs[n].width = kWidth;
    inputs[n].height = kHeight;
  }

  // Apply get_bboxes
  float bboxes[83 * 2][9];
  float scores[83 * 2];
  int32_t labels[83 * 2];
  int32_t num_bboxes = centerpoint_get_bboxes(inputs, bboxes, scores, labels);

  // Prepare expected data
  static constexpr size_t kExpectedNumBBoxes = 120;
  float expected_bboxes[kExpectedNumBBoxes][9];
  ReadBinaryFile("test/bin/get_bboxes/bboxes.bin", expected_bboxes[0]);
  float expected_scores[kExpectedNumBBoxes];
  ReadBinaryFile("test/bin/get_bboxes/scores.bin", expected_scores);
  int32_t expected_labels[kExpectedNumBBoxes];
  ReadBinaryFile("test/bin/get_bboxes/labels.bin", expected_labels);

  // Check results
  REQUIRE(num_bboxes == kExpectedNumBBoxes);
  for (auto i = 0; i < num_bboxes; ++i) {
    for (auto j = 0; j < 9; ++j) {
      REQUIRE(fabsf(bboxes[i][j] - expected_bboxes[i][j]) < 1e-5f);
    }
  }
  for (auto i = 0; i < num_bboxes; ++i) {
    REQUIRE(fabsf(scores[i] - expected_scores[i]) < 1e-5f);
  }
  REQUIRE(memcmp(labels, expected_labels, num_bboxes * sizeof(float)) == 0);
}
