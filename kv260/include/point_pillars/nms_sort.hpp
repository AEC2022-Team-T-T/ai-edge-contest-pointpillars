#ifndef NMS_SORT_HPP_
#define NMS_SORT_HPP_

#include <stdint.h>
#include <cstddef>
#include "point_pillars/nms.hpp"

struct exec_env
{
        int uio0_fd;
        int uio1_fd;
        unsigned int *IMEM_BASE;
        unsigned int *DMEM_BASE;
};

struct exec_env *init();
void reset(struct exec_env *env);
void nms_sort(struct exec_env *, struct ScoreIndex[], size_t);

#endif // NMS_SORT_HPP_
