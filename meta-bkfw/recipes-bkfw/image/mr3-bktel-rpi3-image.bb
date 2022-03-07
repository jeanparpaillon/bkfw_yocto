require recipes-core/images/core-image-base.bb

IMAGE_INSTALL += "\
    mr3 \
    nano \
    "

export IMAGE_BASENAME = "mr3-bktel-rpi3"

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

    install -d -m -0755 -o bktel -g bktel ${IMAGE_ROOTFS}${localstatedir}/lib/bkfw
    cat <<EOF > ${IMAGE_ROOTFS}${localstatedir}/lib/bkfw/factory.config
[
  {bkfw,
    [
      {logo, "/var/lib/bkfw/logos/bktel_logo.png"},
      {debug,false}
    ] 
  }
].
EOF
}
