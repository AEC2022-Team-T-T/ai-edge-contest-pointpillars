# Copyright 2022-2023 Woven Alpha, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

REGISTRY ?=
VAI_IMAGE := $(REGISTRY)ai-edge-contest/vitis-ai-gpu:2.5.1
BASE_REPO := $(REGISTRY)ai-edge-contest/pointpillars-gpu
NOTEBOOK_REPO := $(REGISTRY)ai-edge-contest/pointpillars-code-gpu
VAI_VERSION := $(shell echo $(VAI_IMAGE) | cut -d: -f2)
LATEST_TAG := latest-vai$(VAI_VERSION)
GIT_TAG := $(shell git describe --tags --always --dirty)-vai$(VAI_VERSION)

docker-build-notebook: docker-build-base
	docker build --build-arg=BASE_IMG=$(BASE_REPO):$(LATEST_TAG) -t $(NOTEBOOK_REPO):$(LATEST_TAG) -f docker/codeserver.dockerfile .
	docker tag $(NOTEBOOK_REPO):$(LATEST_TAG) $(NOTEBOOK_REPO):$(GIT_TAG)

docker-build-base:
	docker build --build-arg=BASE_IMG=$(VAI_IMAGE) -t $(BASE_REPO):$(LATEST_TAG) -f docker/base.dockerfile .
	docker tag $(BASE_REPO):$(LATEST_TAG) $(BASE_REPO):$(GIT_TAG)

docker-push:
	docker push $(NOTEBOOK_REPO):$(LATEST_TAG)
	docker push $(NOTEBOOK_REPO):$(GIT_TAG)
	docker push $(BASE_REPO):$(LATEST_TAG)
	docker push $(BASE_REPO):$(GIT_TAG)

archive:
	git archive HEAD --prefix ai-edge-contest-pointpillars/ -o submission/source.tar.gz
