FROM ubuntu:20.04

# Set default shell to /bin/bash.
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

# Install required library
# hadolint ignore=SC2046,DL3008
RUN set -x && \
    apt-get update && \
    apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
        autoconf \
        automake \
        autotools-dev \
        bc \
        bison \
        build-essential \
        ca-certificates \
        curl \
        device-tree-compiler \
        flex \
        gawk \
        git \
        gperf \
        libexpat-dev \
        libgmp-dev \
        libmpc-dev \
        libmpfr-dev \
        libtool \
        libusb-1.0-0-dev \
        patchutils \
        pkg-config \
        python3 \
        texinfo \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/opt/riscv/bin:$PATH
ENV RISCV=/opt/riscv

# Build and install RISC-V GNU Toolchain
WORKDIR /opt
ARG TAG
# hadolint ignore=DL3003
RUN git clone https://github.com/riscv-collab/riscv-gnu-toolchain.git -b ${TAG} && \
    cd /opt/riscv-gnu-toolchain && \
    ./configure --prefix=/opt/riscv --enable-multilib && \
    make linux -j8

# Build and install Spike RISC-V ISA Simulator
WORKDIR /opt
# hadolint ignore=DL3003
RUN git clone https://github.com/riscv-software-src/riscv-isa-sim.git && \
    cd /opt/riscv-isa-sim && \
    mkdir build && \
    cd build && \
    ../configure --prefix=${RISCV} && \
    make -j8 && \
    make install

# Build and install RISC-V Proxy Kernel and Boot Loader
WORKDIR /opt
# hadolint ignore=DL3003
RUN git clone https://github.com/riscv-software-src/riscv-pk.git && \
    cd /opt/riscv-pk && \
    mkdir build && \
    cd build && \
    ../configure --prefix=${RISCV} --host=riscv64-unknown-linux-gnu && \
    make -j8 && \
    make install
