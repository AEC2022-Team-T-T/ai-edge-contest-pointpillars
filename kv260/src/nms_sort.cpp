#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <fcntl.h>
#include <dirent.h>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>
#include <assert.h>

#include "point_pillars/nms_sort.hpp"

#define REG(address) *(volatile unsigned int *)(address)


int reset_and_run()
{
        int fd;
        char attr[32];

        DIR *dir = opendir("/sys/class/gpio/gpio172");
        if (!dir)
        {
                fd = open("/sys/class/gpio/export", O_WRONLY);
                if (fd < 0)
                {
                        perror("open(/sys/class/gpio/export)");
                        return -1;
                }
                strcpy(attr, "172");
                write(fd, attr, strlen(attr));
                close(fd);
                dir = opendir("/sys/class/gpio/gpio172");
                if (!dir)
                {
                        return -1;
                }
        }
        closedir(dir);

        fd = open("/sys/class/gpio/gpio172/direction", O_WRONLY);
        if (fd < 0)
        {
                perror("open(/sys/class/gpio/gpio172/direction)");
                return -1;
        }
        strcpy(attr, "out");
        write(fd, attr, strlen(attr));
        close(fd);

        fd = open("/sys/class/gpio/gpio172/value", O_WRONLY);
        if (fd < 0)
        {
                perror("open(/sys/class/gpio/gpio172/value)");
                return -1;
        }
        sprintf(attr, "%d", 0);
        write(fd, attr, strlen(attr));

        sprintf(attr, "%d", 1);
        write(fd, attr, strlen(attr));
        close(fd);
        return 0;
}

unsigned int float_as_uint(float f)
{
        union
        {
                float f;
                unsigned int i;
        } union_a;
        union_a.f = f;
        return union_a.i;
}

float uint_as_float(unsigned int i)
{
        union
        {
                float f;
                unsigned int i;
        } union_a;
        union_a.i = i;
        return union_a.f;
}

unsigned int int_as_uint(int x)
{
        union
        {
                int in;
                unsigned int u;
        } union_a;
        union_a.in = x;
        return union_a.u;
}

int uint_as_int(unsigned int x)
{
        union
        {
                int in;
                unsigned int u;
        } union_a;
        union_a.u = x;
        return union_a.in;
}

// sort in nms
void set_instructions(unsigned int *IMEM_BASE)
{
        int i = 0;
        IMEM_BASE[i++] = 0xa0020537; //        lui     a0,0xa0020
        IMEM_BASE[i++] = 0x00052583; //        lw      a1,0(a0) # ffffffffa0020000 <.L88+0xffffffffa001ff94>
        IMEM_BASE[i++] = 0x00450513; //        addi    a0,a0,4
        IMEM_BASE[i++] = 0x06058063; //        beqz    a1,6c <.L88>
        IMEM_BASE[i++] = 0x00359793; //        slli    a5,a1,0x3
        IMEM_BASE[i++] = 0x00850713; //        addi    a4,a0,8
        IMEM_BASE[i++] = 0x00f50633; //        add     a2,a0,a5
        IMEM_BASE[i++] = 0x00100813; //        li      a6,1
        IMEM_BASE[i++] = 0x02b87c63; //        bgeu    a6,a1,58 <.L90>
        IMEM_BASE[i++] = 0x00070793; //        mv      a5,a4
        IMEM_BASE[i++] = 0x0007a787; //        flw     fa5,0(a5)
        IMEM_BASE[i++] = 0xff872707; //        flw     fa4,-8(a4)
        IMEM_BASE[i++] = 0xa0f716d3; //        flt.s   a3,fa4,fa5
        IMEM_BASE[i++] = 0x00068e63; //        beqz    a3,50 <.L91>
        IMEM_BASE[i++] = 0xffc72503; //        lw      a0,-4(a4)
        IMEM_BASE[i++] = 0x0047a683; //        lw      a3,4(a5)
        IMEM_BASE[i++] = 0x00e7a027; //        fsw     fa4,0(a5)
        IMEM_BASE[i++] = 0x00a7a223; //        sw      a0,4(a5)
        IMEM_BASE[i++] = 0xfef72c27; //        fsw     fa5,-8(a4)
        IMEM_BASE[i++] = 0xfed72e23; //        sw      a3,-4(a4)
        IMEM_BASE[i++] = 0x00878793; //        addi    a5,a5,8
        IMEM_BASE[i++] = 0xfcc79ae3; //        bne     a5,a2,28 <.L93>
        IMEM_BASE[i++] = 0x00180793; //        addi    a5,a6,1
        IMEM_BASE[i++] = 0x00870713; //        addi    a4,a4,8
        IMEM_BASE[i++] = 0x01058663; //        beq     a1,a6,6c <.L88>
        IMEM_BASE[i++] = 0x00078813; //        mv      a6,a5
        IMEM_BASE[i++] = 0xfb9ff06f; //        j       20 <.L94>
        IMEM_BASE[i++] = 0x00008067; //        ret
}


// initialization for RISCV Execution
struct exec_env *init()
{
        struct exec_env *env = (struct exec_env *)malloc(sizeof(struct exec_env));
        env->uio0_fd = open("/dev/uio4", O_RDWR | O_SYNC);
        env->DMEM_BASE = (unsigned int *)mmap(NULL, 0x20000, PROT_READ | PROT_WRITE, MAP_SHARED, env->uio0_fd, 0);
        env->uio1_fd = open("/dev/uio5", O_RDWR | O_SYNC);
        env->IMEM_BASE = (unsigned int *)mmap(NULL, 0x4000, PROT_READ | PROT_WRITE, MAP_SHARED, env->uio1_fd, 0);
        if (env->uio0_fd < 0 || env->uio1_fd < 0)
        {
                printf("Device Open Error");
                exit(-1);
        }

        set_instructions(env->IMEM_BASE);
        return env;
}

void reset(struct exec_env *env)
{
        close(env->uio0_fd);
        close(env->uio1_fd);
        free(env);
}

void nms_sort(struct exec_env *env, struct ScoreIndex lst[], size_t size)
{
        env->DMEM_BASE[0] = int_as_uint(size);
        for (int i = 0; i < size; i++)
        {
                env->DMEM_BASE[1 + i * 2] = float_as_uint(lst[i].score);
                env->DMEM_BASE[2 + i * 2] = int_as_uint(lst[i].index);
        }
        reset_and_run();

// wait RISC-V execution completion
        usleep(1000);
        for (int i = 0; i < size; i++)
        {
                lst[i].score = uint_as_float(env->DMEM_BASE[1 + i * 2]);
                lst[i].index = uint_as_int(env->DMEM_BASE[2 + i * 2]);
        }
}

#ifdef TEST
int main()
{
        struct exec_env *env = init();

        struct ScoreIndex inputs[3];
        inputs[0].index = 10;
        inputs[1].index = 11;
        inputs[2].index = 12;
        inputs[0].score = 100.0f;
        inputs[1].score = 333.0f;
        inputs[2].score = 222.0f;

        nms_sort(env, inputs, 3);

        for (auto i = 0; i < 3; i++)
        {
                printf("score %lf\n", inputs[i].score);
        }

        assert(inputs[0].score == 333.0f);
        assert(inputs[1].score == 222.0f);
        assert(inputs[2].score == 100.0f);

        reset(env);
}
#endif
