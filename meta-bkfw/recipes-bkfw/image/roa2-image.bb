require recipes-core/images/rpi-basic-image.bb

IMAGE_INSTALL += "\
    bkfw \
    roa2 \
    nano \
    "

export IMAGE_BASENAME = "bkfw-roa2"

R = "r0"

IMAGE_LINGUAS = " "
USE_NLS="no"

LICENSE = "CLOSED"

ROOTFS_POSTPROCESS_COMMAND += "setup_target_image ; "

# Manual workaround for lack of auto eth0 (see bug #875)
setup_target_image() {
    install -d -m -0755 -o root -g root ${IMAGE_ROOTFS}${sysconfdir}/network
    install -m 0644 ${TOPDIR}/files/interfaces ${IMAGE_ROOTFS}${sysconfdir}/network/interfaces
    install -m 0644 ${TOPDIR}/files/factory.config ${IMAGE_ROOTFS}${localstatedir}/lib/bkfw/factory.config

    mv ${IMAGE_ROOTFS}${sysconfdir}/inittab ${IMAGE_ROOTFS}${sysconfdir}/inittab.serial
    sed -e 's/^AMA0.*//' ${IMAGE_ROOTFS}${sysconfdir}/inittab.serial > ${IMAGE_ROOTFS}${sysconfdir}/inittab
}
