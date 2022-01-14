DESCRIPTION = "BKfw Firmware"
HOMEPAGE = "http://github.com/jeanparpaillon/bktel"
SECTION = "firmware"
PRIORITY = "optional"
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://COPYING;md5=aa9dd28ba4e8988d5ef23897cd630463"

PACKAGES = "${PN}"

PR = "r1"

S = "${WORKDIR}/bkfw"
SRC_URI = "file://bkfw.tar.gz \
           file://scripts/changeInterface.awk \
           file://scripts/check_pkg.sh \
           file://scripts/commit_network.sh \
           file://scripts/readInterfaces.awk \
           file://scripts/restart.sh \
           file://scripts/upgrade.sh"

PARALLEL_MAKE = ""

inherit useradd
inherit erlang
inherit update-rc.d

DEPENDS += "erlang-native openssl"
RDEPENDS_${PN} += "gawk erlang"

USERADD_PACKAGES = "${PN}"
USERADD_PARAM_${PN} = "-u 1000 -g 1000 -d ${servicedir}/bkfw -r -s /bin/sh bktel"
GROUPADD_PARAM_${PN} = "-g 1000 bktel"

# Avoid 'already-stripped' error
INSANE_SKIP_${PN} = "already-stripped host-user-contaminated"
INHIBIT_PACKAGE_DEBUG_SPLIT = '1'
INHIBIT_PACKAGE_STRIP = '1'

INITSCRIPT_NAME = "bkfw"
INITSCRIPT_PARAMS = "defaults 99"

PREFERRED_VERSION_erlang = "18.2.3"
PREFERRED_VERSION_erlang-native = "18.2.3"

do_install() {
  install -d ${D}${servicedir}/bkfw

  cp -a ${S}/* ${D}${servicedir}/bkfw/
  chown -R bktel ${D}${servicedir}
  chgrp -R bktel ${D}${servicedir}

  install -d ${D}${localstatedir}/lib/bkfw
  echo "[]." > ${D}${localstatedir}/lib/bkfw/factory.config
  echo "[]." > ${D}${localstatedir}/lib/bkfw/user.config

  install -d ${D}${localstatedir}/lib/bkfw/upload

  install -d -o bktel -g bktel ${D}${localstatedir}/lib/bkfw/scripts
  for script in ${WORKDIR}/scripts/*; do
      install -m 755 -o bktel -g bktel $script ${D}${localstatedir}/lib/bkfw/scripts/`basename $script`
  done

  chown -R bktel.bktel ${D}${localstatedir}/lib/bkfw

  install -d -o root -g root ${D}${sysconfdir}/init.d
  install -m 755 -o root -g root ${WORKDIR}/bkfw.init ${D}${sysconfdir}/init.d/bkfw
}

FILES_${PN} += " \
	    ${servicedir}/bkfw \
	    ${localstatedir}/lib/bkfw \
	    ${sysconfdir}/init.d/bkfw \
	    ${prefix}/local/bin/od \
	    "
