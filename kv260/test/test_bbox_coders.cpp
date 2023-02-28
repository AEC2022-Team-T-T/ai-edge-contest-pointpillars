// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#include <math.h>
#include <string.h>

#include "./utility.hpp"
#include "catch2/catch.hpp"
#include "point_pillars/bbox_coders.hpp"

TEST_CASE("bounding boxes are decoded correctly by CenterPointBBoxCoder",
          "[bbox_coders]") {
  // Load inputs
  static constexpr size_t kWidth = 128;
  static constexpr size_t kHeight = 128;

  float heatmap_buffer[kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_heatmap.bin", &heatmap_buffer);
  float rot_sin_buffer[kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_rots.bin", rot_sin_buffer);
  float rot_cos_buffer[kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_rotc.bin", rot_cos_buffer);
  float hei_buffer[kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_hei.bin", hei_buffer);
  float dim_buffer[3 * kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_dim.bin", dim_buffer);
  float vel_buffer[2 * kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_vel.bin", vel_buffer);
  float reg_buffer[2 * kHeight * kWidth] = {};
  ReadBinaryFile("test/bin/bbox_coders/batch_reg.bin", reg_buffer);

  float rot_buffer[2 * kHeight * kWidth] = {};
  memcpy(rot_buffer, rot_sin_buffer, kHeight * kWidth * sizeof(float));
  memcpy(rot_buffer + kHeight * kWidth, rot_cos_buffer,
         kHeight * kWidth * sizeof(float));

  CenterPointOutput center_point_output = {
      heatmap_buffer, hei_buffer, dim_buffer, rot_buffer,
      vel_buffer,     reg_buffer, kWidth,     kHeight};

  // Decode bboxes
  CenterPointDecoderConfig config = {
      500,
      0.1f,
      4.0f,
      {0.2f, 0.2f},
      {-51.2f, -51.2f},
      {-61.2f, -61.2f, -10.0f, 61.2f, 61.2f, 10.0f}};

  float bboxes[1000][9];
  float scores[1000];
  float labels[1000];
  int32_t num_bboxes = centerpoint_bbox_decode(center_point_output, config,
                                               bboxes[0], scores, labels);

  // Prepare expected data
  static constexpr size_t kExpectedNumBBoxes = 148;
  float expected_bboxes[kExpectedNumBBoxes][9];
  ReadBinaryFile("test/bin/bbox_coders/bboxes.bin", expected_bboxes);
  float expected_scores[kExpectedNumBBoxes];
  ReadBinaryFile("test/bin/bbox_coders/scores.bin", expected_scores);
  float expected_labels[kExpectedNumBBoxes];
  ReadBinaryFile("test/bin/bbox_coders/labels.bin", expected_labels);

  // Check results
  REQUIRE(num_bboxes == kExpectedNumBBoxes);
  for (auto i = 0; i < num_bboxes; ++i) {
    for (auto j = 0; j < 9; ++j) {
      REQUIRE(fabsf(bboxes[i][j] - expected_bboxes[i][j]) < 1.0e-5f);
    }
  }
  REQUIRE(memcmp(scores, expected_scores, num_bboxes * sizeof(float)) == 0);
  REQUIRE(memcmp(labels, expected_labels, num_bboxes * sizeof(float)) == 0);
}
