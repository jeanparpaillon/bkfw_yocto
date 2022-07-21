DESCRIPTION = "BKfw Firmware"
HOMEPAGE = "http://github.com/jeanparpaillon/bkfw_mr3"
SECTION = "firmware"
PRIORITY = "optional"
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://COPYING;md5=aa9dd28ba4e8988d5ef23897cd630463"

PACKAGES = "${PN}"
 
# Set ipk package name (need to be sync with check_pkg script)
# PKG_mr3 = "bkfw"

PR = "r1"

#S = "${TMPDIR}/../../.."
SRC_URI = "\
  git://github.com/jeanparpaillon/bkfw_mr3.git;rev=48bcd919b2bf994cab03f290c775bcce5164696d \
  file://logo/bktel_logo.png \
  file://logo/l2k_logo.png \
  file://logo/Packetlight_logo.png \
  "
S = "${WORKDIR}/git"

PARALLEL_MAKE = ""

inherit useradd
inherit erlang
inherit update-rc.d

DEPENDS += "erlang-native openssl"
RDEPENDS_${PN} += "gawk erlang"

EXTRA_OEMAKE = "all"

USERADD_PACKAGES = "${PN}"
USERADD_PARAM_${PN} = "-u 1000 -g 1000 -d ${servicedir}/bkfw -r -s /bin/sh bktel"
GROUPADD_PARAM_${PN} = "-g 1000 bktel"

# Avoid 'already-stripped' error
INSANE_SKIP_${PN} = "already-stripped host-user-contaminated"
INHIBIT_PACKAGE_DEBUG_SPLIT = '1'
INHIBIT_PACKAGE_STRIP = '1'

INITSCRIPT_NAME = "bkfw"
INITSCRIPT_PARAMS = "defaults 99"

PREFERRED_VERSION_erlang = "21.3.8.24"
PREFERRED_VERSION_erlang-native = "21.3.8.24"

do_compile() {
  RELX_CONFIG=/invalid oe_runmake
}

do_install() {
  install -d ${D}${servicedir}

  ${S}/relx --system_libs ${STAGING_LIBDIR}/erlang/lib \
    -c ${S}/rel/relx.config \
    -o ${D}${servicedir}

  find ${D}${servicedir} -name '*.erl' -exec rm {} \;
  rm -rf ${D}${prefix}/src/debug
  chown -R bktel ${D}${servicedir}
  chgrp -R bktel ${D}${servicedir}

  install -d ${D}${localstatedir}/lib/bkfw
  # install -o bktel -g bktel ${WORKDIR}/mr3/factory.config ${D}${localstatedir}/lib/bkfw/factory.config
  echo "[]." > ${D}${localstatedir}/lib/bkfw/user.config

  install -d ${D}${localstatedir}/lib/bkfw/upload

  install -d -o bktel -g bktel ${D}${localstatedir}/lib/bkfw/scripts
  for script in ${S}/priv/scripts/*; do
      install -m 755 -o bktel -g bktel $script ${D}${localstatedir}/lib/bkfw/scripts/`basename $script`
  done

  chown -R bktel.bktel ${D}${localstatedir}/lib/bkfw

  install -d -o root -g root ${D}${sysconfdir}/init.d
  install -m 755 -o root -g root ${S}/debian/bkfw.init ${D}${sysconfdir}/init.d/bkfw

  install -d -o bktel -g bktel ${D}${localstatedir}/lib/bkfw/logos
  for logo in ${WORKDIR}/logo/*; do
      install -m 644 -o bktel -g bktel $logo ${D}${localstatedir}/lib/bkfw/logos/`basename $logo`
  done
}

FILES_${PN} += " \
	    ${servicedir}/bkfw \
	    ${localstatedir}/lib/bkfw \
	    ${sysconfdir}/init.d/bkfw \
	    ${prefix}/local/bin/od \
	    "
