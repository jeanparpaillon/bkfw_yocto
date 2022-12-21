IMAGE=rra-rpi3-image

BUILD_CONTAINER=yocto-build

all:
	cd poky && . ./oe-init-build-env ../build && bitbake $(IMAGE)

build-env:
	docker run -it -v $(HOME):$(HOME) -v $(PWD)/docker/asdf:$(HOME)/.asdf -v /scratch:/scratch $(BUILD_CONTAINER)

build-image: $(BUILD_CONTAINER)

$(BUILD_CONTAINER):
	docker build -t $@ -f docker/Dockerfile docker

.PHONY: $(BUILD_CONTAINER) build-env build-image