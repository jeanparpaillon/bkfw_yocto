IMAGE=rra-rpi3-image

all:
	cd poky && . ./oe-init-build-env ../build && bitbake $(IMAGE)
