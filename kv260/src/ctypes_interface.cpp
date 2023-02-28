/*
 * Copyright 2022-2023 Woven Planet Holdings.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include <stdio.h>
#include <point_pillars/get_bboxes.hpp>
#ifdef __cplusplus
extern "C" {
#endif

/**
 * Interface to pass Numpy ndarrays to the actual postprocess. 
 *
 * @param heatmap1 from SeparateHead's first head  (1,128,128)
 * @param height1  from SeparateHead's first head  (1,128,128)
 * @param dim1     from SeparateHead's first head  (3,128,128)
 * @param rot1     from SeparateHead's first head  (2,128,128)
 * @param vel1     from SeparateHead's first head  (2,128,128)
 * @param reg1     from SeparateHead's first head  (2,128,128)
 * @param heatmap2 from SeparateHead's second head (1,128,128)
 * @param height2  from SeparateHead's second head (1,128,128)
 * @param dim2     from SeparateHead's second head (3,128,128)
 * @param rot2     from SeparateHead's second head (2,128,128)
 * @param vel2     from SeparateHead's second head (2,128,128)
 * @param reg2     from SeparateHead's second head (2,128,128)
 * @return Number of detected objects.
 */
int postprocess(
    float* heatmap1,
    float* height1,
    float* dim1,
    float* rot1,
    float* vel1,
    float* reg1,
    float* heatmap2,
    float* height2,
    float* dim2,
    float* rot2,
    float* vel2,
    float* reg2) {
  // NOTE: For the testing purpose, now printing the last element.
  int ret;
  float bboxes[NMS_MAX_NUM*2][BBOX_DIM];
  float scores[NMS_MAX_NUM*2];
  int32_t labels[NMS_MAX_NUM*2];
  CenterPointOutput center_point_output[NUM_INPUTS];
  center_point_output[0].heatmap = heatmap1;
  center_point_output[0].hei     = height1;
  center_point_output[0].dim     = dim1;
  center_point_output[0].rot     = rot1;
  center_point_output[0].vel     = vel1;
  center_point_output[0].reg     = reg1;
  center_point_output[0].width   = 128;
  center_point_output[0].height  = 128;
  center_point_output[1].heatmap = heatmap2;
  center_point_output[1].hei     = height2;
  center_point_output[1].dim     = dim2;
  center_point_output[1].rot     = rot2;
  center_point_output[1].vel     = vel2;
  center_point_output[1].reg     = reg2;
  center_point_output[1].width   = 128;
  center_point_output[1].height  = 128;
  ret = centerpoint_get_bboxes(center_point_output, bboxes, scores, labels);
  return (int)ret;
}

#ifdef __cplusplus
}
#endif
