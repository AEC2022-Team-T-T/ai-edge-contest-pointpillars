// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

#include "./utility.hpp"
#include "catch2/catch.hpp"
#include "point_pillars/nms.hpp"

TEST_CASE("nms is applied correctly", "[nms]") {
  static constexpr size_t kNumBBoxes = 1000;
  static constexpr size_t kBBoxDim = 5;

  // Load input data
  float bboxes[kNumBBoxes][kBBoxDim];
  ReadBinaryFile("test/bin/nms/bboxes.bin", bboxes[0]);
  float scores[kNumBBoxes];
  ReadBinaryFile("test/bin/nms/scores.bin", scores);

  // Apply non maximum suppression
  int32_t selected[kNumBBoxes];
  int32_t num_selected =
      nms(bboxes[0], scores, kNumBBoxes, kBBoxDim, 0.05f, 0.2f, selected);

  // Prepare expected data
  static constexpr size_t kExpectedNumSelected = 26;
  int64_t expected_selected[kExpectedNumSelected];
  ReadBinaryFile("test/bin/nms/selected.bin", expected_selected);

  // Check results
  REQUIRE(num_selected == kExpectedNumSelected);
  for (size_t i = 0; i < num_selected; ++i) {
    REQUIRE(selected[i] == static_cast<int32_t>(expected_selected[i]));
  }
}
