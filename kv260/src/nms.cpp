// Copyright 2022 Woven Alpha, Inc.
// All rights reserved.

// This implementation is based on MMDetection3D
// https://github.com/open-mmlab/mmdetection3d/blob/v0.18.1/mmdet3d/ops/iou3d/src/iou3d_kernel.cu

#include "point_pillars/nms.hpp"
#include "point_pillars/nms_sort.hpp"

#include <math.h>
#include <stdlib.h>

static constexpr size_t MAX_BBOXES = 1000;
static constexpr float EPS = 1e-8;

struct Point {
  float x;
  float y;
  Point() { x = 0.0f, y = 0.0f; }
  Point(float _x, float _y) { x = _x, y = _y; }

  void set(float _x, float _y) {
    x = _x;
    y = _y;
  }

  Point operator+(const Point& b) const { return Point(x + b.x, y + b.y); }
  Point operator-(const Point& b) const { return Point(x - b.x, y - b.y); }
};

static float _min(float lhs, float rhs) { return (lhs > rhs) ? rhs : lhs; }

static float _max(float lhs, float rhs) { return (lhs > rhs) ? lhs : rhs; }

static bool _check_rect_cross(const Point& p1, const Point& p2, const Point& q1,
                              const Point& q2) {
  return _min(p1.x, p2.x) <= _max(q1.x, q2.x) &&
         _min(q1.x, q2.x) <= _max(p1.x, p2.x) &&
         _min(p1.y, p2.y) <= _max(q1.y, q2.y) &&
         _min(q1.y, q2.y) <= _max(p1.y, p2.y);
}

static Point _rotate_around_center(const Point& center, const float angle_cos,
                                   const float angle_sin, const Point& p) {
  float new_x =
      (p.x - center.x) * angle_cos + (p.y - center.y) * angle_sin + center.x;
  float new_y =
      -(p.x - center.x) * angle_sin + (p.y - center.y) * angle_cos + center.y;
  return Point(new_x, new_y);
}

static float _cross(const Point& a, const Point& b) {
  return a.x * b.y - a.y * b.x;
}

static float _cross(const Point& p1, const Point& p2, const Point& p0) {
  return (p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y);
}

static bool _intersection(const Point& p1, const Point& p0, const Point& q1,
                          const Point& q0, Point* ans) {
  // fast exclusion
  if (_check_rect_cross(p0, p1, q0, q1) == 0) return false;

  // check cross standing
  float s1 = _cross(q0, p1, p0);
  float s2 = _cross(p1, q1, p0);
  float s3 = _cross(p0, q1, q0);
  float s4 = _cross(q1, p1, q0);

  if (!(s1 * s2 > 0 && s3 * s4 > 0)) return false;

  // calculate intersection of two lines
  float s5 = _cross(q1, p1, p0);
  if (fabsf(s5 - s1) > EPS) {
    ans->x = (s5 * q0.x - s1 * q1.x) / (s5 - s1);
    ans->y = (s5 * q0.y - s1 * q1.y) / (s5 - s1);
  } else {
    float a0 = p0.y - p1.y, b0 = p1.x - p0.x, c0 = p0.x * p1.y - p1.x * p0.y;
    float a1 = q0.y - q1.y, b1 = q1.x - q0.x, c1 = q0.x * q1.y - q1.x * q0.y;
    float D = a0 * b1 - a1 * b0;
    ans->x = (b0 * c1 - b1 * c0) / D;
    ans->y = (a1 * c0 - a0 * c1) / D;
  }

  return true;
}

static bool _check_in_box2d(const float box[], const Point& p) {
  // params: box (5) [x1, y1, x2, y2, angle]
  const auto MARGIN = 1e-5f;

  const auto center_x = (box[0] + box[2]) / 2;
  const auto center_y = (box[1] + box[3]) / 2;
  const auto angle_cos = cos(-box[4]);
  const auto angle_sin =
      sin(-box[4]);  // rotate the point in the opposite direction of box
  const auto rot_x =
      (p.x - center_x) * angle_cos + (p.y - center_y) * angle_sin + center_x;
  const auto rot_y =
      -(p.x - center_x) * angle_sin + (p.y - center_y) * angle_cos + center_y;
  return (rot_x > box[0] - MARGIN && rot_x < box[2] + MARGIN &&
          rot_y > box[1] - MARGIN && rot_y < box[3] + MARGIN);
}

static bool _point_cmp(const Point& a, const Point& b, const Point& center) {
  return atan2f(a.y - center.y, a.x - center.x) >
         atan2f(b.y - center.y, b.x - center.x);
}

static float _box_overlap(const float box_a[], const float box_b[]) {
  // params: box_a (5) [x1, y1, x2, y2, angle]
  // params: box_b (5) [x1, y1, x2, y2, angle]

  const auto a_x1 = box_a[0];
  const auto a_y1 = box_a[1];
  const auto a_x2 = box_a[2];
  const auto a_y2 = box_a[3];
  const auto a_angle = box_a[4];
  const auto b_x1 = box_b[0];
  const auto b_y1 = box_b[1];
  const auto b_x2 = box_b[2];
  const auto b_y2 = box_b[3];
  const auto b_angle = box_b[4];

  const Point center_a((a_x1 + a_x2) / 2.0f, (a_y1 + a_y2) / 2.0f);
  const Point center_b((b_x1 + b_x2) / 2.0f, (b_y1 + b_y2) / 2.0f);

  Point box_a_corners[] = {Point(a_x1, a_y1), Point(a_x2, a_y1),
                           Point(a_x2, a_y2), Point(a_x1, a_y2),
                           Point(0.0f, 0.0f)};
  Point box_b_corners[] = {Point(b_x1, b_y1), Point(b_x2, b_y1),
                           Point(b_x2, b_y2), Point(b_x1, b_y2),
                           Point(0.0f, 0.0f)};

  // get oriented corners
  const auto a_angle_cos = cosf(a_angle);
  const auto a_angle_sin = sinf(a_angle);
  const auto b_angle_cos = cosf(b_angle);
  const auto b_angle_sin = sinf(b_angle);

  for (int k = 0; k < 4; k++) {
    box_a_corners[k] = _rotate_around_center(center_a, a_angle_cos, a_angle_sin,
                                             box_a_corners[k]);
    box_b_corners[k] = _rotate_around_center(center_b, b_angle_cos, b_angle_sin,
                                             box_b_corners[k]);
  }

  box_a_corners[4] = box_a_corners[0];
  box_b_corners[4] = box_b_corners[0];

  // get intersection of lines
  Point cross_points[16];
  Point poly_center;
  auto cnt = 0;

  poly_center.set(0, 0);
  for (auto i = 0; i < 4; i++) {
    for (auto j = 0; j < 4; j++) {
      if (_intersection(box_a_corners[i + 1], box_a_corners[i],
                        box_b_corners[j + 1], box_b_corners[j],
                        &cross_points[cnt])) {
        poly_center = poly_center + cross_points[cnt];
        cnt++;
      }
    }
  }

  // check corners
  for (auto k = 0; k < 4; k++) {
    if (_check_in_box2d(box_a, box_b_corners[k])) {
      poly_center = poly_center + box_b_corners[k];
      cross_points[cnt] = box_b_corners[k];
      cnt++;
    }
    if (_check_in_box2d(box_b, box_a_corners[k])) {
      poly_center = poly_center + box_a_corners[k];
      cross_points[cnt] = box_a_corners[k];
      cnt++;
    }
  }

  poly_center.x /= cnt;
  poly_center.y /= cnt;

  // sort the points of polygon
  Point temp;
  for (auto j = 0; j < cnt - 1; j++) {
    for (auto i = 0; i < cnt - j - 1; i++) {
      if (_point_cmp(cross_points[i], cross_points[i + 1], poly_center)) {
        const auto tmp = cross_points[i];
        cross_points[i] = cross_points[i + 1];
        cross_points[i + 1] = tmp;
      }
    }
  }

  // get the overlap areas
  auto area = 0.0f;
  for (auto k = 0; k < cnt - 1; k++) {
    area += _cross(cross_points[k] - cross_points[0],
                   cross_points[k + 1] - cross_points[0]);
  }

  return fabsf(area) / 2.0f;
}

static float _iou_bev(const float box_a[], const float box_b[]) {
  // params: box_a (5) [x1, y1, x2, y2, angle]
  // params: box_b (5) [x1, y1, x2, y2, angle]
  float sa = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1]);
  float sb = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1]);
  float s_overlap = _box_overlap(box_a, box_b);
  return s_overlap / _max(sa + sb - s_overlap, EPS);
}

static int _compare(const void* lhs, const void* rhs) {
  const ScoreIndex* lhs_score_index = static_cast<const ScoreIndex*>(lhs);
  const ScoreIndex* rhs_score_index = static_cast<const ScoreIndex*>(rhs);
  if (rhs_score_index->score > lhs_score_index->score) {
    return 1;
  }
  if (rhs_score_index->score < lhs_score_index->score) {
    return -1;
  }
  return 0;
}

int32_t nms(const float bboxes[], const float scores[], int32_t num_bboxes,
            int32_t bbox_dim, float score_threshold, float nms_threshold,
            int32_t selected[]) {
  bool keep[MAX_BBOXES] = {};
  for (auto i = 0; i < num_bboxes; ++i) {
    // If the score of bbox is below threshold, it won't be selected.
    if (scores[i] > score_threshold) {
      keep[i] = true;
    }
  }

  // Sort indices by scores
  ScoreIndex score_index[MAX_BBOXES] = {};
  for (auto i = 0; i < num_bboxes; ++i) {
    score_index[i] = {scores[i], i};
  }

  exec_env * env = init();
  nms_sort(env, score_index, num_bboxes);
  reset(env);

  // Apply non maximum suppression
  for (auto i = 0; i < num_bboxes - 1; ++i) {
    if (!keep[score_index[i].index]) {
      continue;
    }
    const auto& current_bbox = bboxes[score_index[i].index];
    for (auto j = i + 1; j < num_bboxes; ++j) {
      if (!keep[score_index[j].index]) {
        continue;
      }
      if (_iou_bev(bboxes + score_index[i].index * bbox_dim,
                   bboxes + score_index[j].index * bbox_dim) > nms_threshold) {
        keep[score_index[j].index] = false;
      }
    }
  }

  // Get indices of selected bounding box
  int32_t num_selected = 0;
  for (auto i = 0; i < num_bboxes; ++i) {
    if (keep[score_index[i].index]) {
      selected[num_selected] = score_index[i].index;
      num_selected++;
    }
  }
  return num_selected;
}
