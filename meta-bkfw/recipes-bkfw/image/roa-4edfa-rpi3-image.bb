require recipes-core/images/core-image-base.bb

IMAGE_INSTALL += "\
    bkfw \
    roa-4edfa \
    nano \
    "

export IMAGE_BASENAME = "roa-4edfa-rpi3"

R = "r1"

IMAGE_LINGUAS = " "
USE_NLS="no"

LICENSE = "CLOSED"

ROOTFS_POSTPROCESS_COMMAND += "setup_target_image ; "

IMAGE_FEATURES += "ssh-server-dropbear"

# Manual workaround for lack of auto eth0 (see bug #875)
setup_target_image() {
    install -d -m -0755 -o root -g root ${IMAGE_ROOTFS}${sysconfdir}/network
    install -m 0644 ${TOPDIR}/files/interfaces ${IMAGE_ROOTFS}${sysconfdir}/network/interfaces

    mv ${IMAGE_ROOTFS}${sysconfdir}/inittab ${IMAGE_ROOTFS}${sysconfdir}/inittab.serial
    sed -e 's/^AMA0.*//' ${IMAGE_ROOTFS}${sysconfdir}/inittab.serial > ${IMAGE_ROOTFS}${sysconfdir}/inittab
}
