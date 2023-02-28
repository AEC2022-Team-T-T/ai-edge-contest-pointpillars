PROJECT_DIR := $(realpath $(dir $(lastword $(MAKEFILE_LIST))))
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)
CURRENT_USERNAME := $(shell whoami)
DOCKER_IMAGE := riscv_gnu_toolchain
DOCKER_TAG := 2022.10.11
DOCKER_RUN_OPTIONS := --rm \
	-v ${PROJECT_DIR}:/workspace \
	-w /workspace \
	--user ${CURRENT_UID}:${CURRENT_GID} \
	-e USER=${CURRENT_USERNAME}
DOCKER_RUN = docker run ${DOCKER_RUN_OPTIONS} ${DOCKER_IMAGE}:${DOCKER_TAG}
CXX := aarch64-linux-gnu-g++-10
AR := aarch64-linux-gnu-gcc-ar-10
CXXFLAGS = -O2
LDFLAGS = -lm -lstdc++ -static
BUILD_DIR ?= ./build
SRC_DIR ?= ./src
SRCS := $(shell find $(SRC_DIR) -name *.cpp)
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)
DMPS := $(SRCS:%=$(BUILD_DIR)/%.dmp)
INC_FLAGS = -Iinclude
LIB_NAME = $(BUILD_DIR)/lib/libpoint_pillars.a
CTYPES_NAME = $(BUILD_DIR)/lib/libRiscvInterface.so

TEST_DIR ?= ./test
TEST_SRCS := $(shell find $(TEST_DIR) -name *.cpp)
TEST_INC_FLAGS = -Ithird_party -Itest
TEST_EXEC = $(BUILD_DIR)/test/test_point_pillars

RISCV_PROXY_KERNEL = /opt/riscv/riscv64-unknown-linux-gnu/bin/pk

.PHONY: help
help: ## This help
	@grep -E '^[a-zA-Z0-9_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: docker-build
docker-build: ## Build docker image
	docker buildx build -t ${DOCKER_IMAGE}:${DOCKER_TAG} -f docker/Dockerfile --build-arg TAG=${DOCKER_TAG} docker

.PHONY: install-pre-commit-hook
install-pre-commit-hook: ## Set up pre-commit.
	pip3 install pre-commit
	pre-commit install -t pre-commit -t pre-push

.PHONY: all
all: ## Clean project, Build library and test, run test, and dump assembly code
	make clean
	make build
	make test
	make dmp

.PHONY: build
build: $(OBJS) ## Build library and test
	make build-lib
	make build-test

.PHONY: build-lib
build-lib: $(OBJS) ## Build library
	mkdir -p $(dir $(LIB_NAME))
	$(AR) r $(LIB_NAME) $(OBJS)

.PHONY: build-ctypes-interface
build-ctypes-interface: build-lib
	$(CXX) $(CXXFLAGS) $(INC_FLAGS) -fpic -Wall -o $(BUILD_DIR)/ctypes_interface.o -c $(SRC_DIR)/ctypes_interface.cpp
	$(CXX) -shared -o $(CTYPES_NAME) $(BUILD_DIR)/ctypes_interface.o $(LIB_NAME)

$(BUILD_DIR)/%.cpp.o: %.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) $(INC_FLAGS) -c $< -o $@

.PHONY: build-test
build-test: build-lib ## Build test
	mkdir -p $(dir $(TEST_EXEC))
	$(CXX) $(CXXFLAGS) $(INC_FLAGS) $(TEST_INC_FLAGS) $(TEST_SRCS) -o $(TEST_EXEC) $(LIB_NAME) $(LDFLAGS)

.PHONY: test
test: ## Run test
	docker run ${DOCKER_RUN_OPTIONS} ${DOCKER_IMAGE}:${DOCKER_TAG} \
	spike $(RISCV_PROXY_KERNEL) $(TEST_EXEC)

.PHONY: dmp
dmp: $(DMPS) ## Dump assembly code

$(BUILD_DIR)/%.cpp.dmp: $(BUILD_DIR)/%.cpp.o
	docker run ${DOCKER_RUN_OPTIONS} ${DOCKER_IMAGE}:${DOCKER_TAG} \
	riscv64-unknown-linux-gnu-objdump -d $< > $@

.PHONY: clean
clean:
	rm -rf build
