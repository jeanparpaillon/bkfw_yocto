DESCRIPTION = "BKfw Firmware"
HOMEPAGE = "http://github.com/jeanparpaillon/bktel"
SECTION = "firmware"
PRIORITY = "optional"
LICENSE = "CLOSED"
#LIC_FILES_CHKSUM = "file://COPYING;md5=aa9dd28ba4e8988d5ef23897cd630463"

PACKAGES = "${PN}"

PR = "r1"

S = "${WORKDIR}/git"
SRC_URI = "git://github.com/jeanparpaillon/bkfw_roa_rg.git;rev=4cb803d535536725414697f76a711612adbcd242"
PARALLEL_MAKE = ""

inherit useradd
inherit erlang
inherit update-rc.d

DEPENDS += "erlang-native openssl curl-native"
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
  RELX_CONFIG=/nonexistent \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    oe_runmake
}

do_install() {
  install -d ${D}${servicedir}

  RELX_CONFIG="${S}/rel/prod/relx.config" \
    RELX_OPTS="--system_libs ${STAGING_LIBDIR}/erlang/lib" \
    RELX_OUTPUT_DIR="${D}${servicedir}" \
    V=1 \
    CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    oe_runmake

  # ${S}/.erlang.mk/relx --system_libs ${STAGING_LIBDIR}/erlang/lib \
  #   -c ${S}/rel/prod/relx.config \
  #   -o ${D}${servicedir}

  find ${D}${servicedir} -name '*.erl' -exec rm {} \;
  rm -rf ${D}${prefix}/src/debug
  chown -R bktel ${D}${servicedir}
  chgrp -R bktel ${D}${servicedir}

  install -d ${D}${localstatedir}/lib/bkfw
  # echo "[]." > ${D}${localstatedir}/lib/bkfw/factory.config
  echo "[]." > ${D}${localstatedir}/lib/bkfw/user.config

  install -d ${D}${localstatedir}/lib/bkfw/upload

  install -d -o bktel -g bktel ${D}${localstatedir}/lib/bkfw/scripts
  for script in ${S}/priv/scripts/*; do
      install -m 755 -o bktel -g bktel $script ${D}${localstatedir}/lib/bkfw/scripts/`basename $script`
  done

  chown -R bktel.bktel ${D}${localstatedir}/lib/bkfw

  install -d -o root -g root ${D}${sysconfdir}/init.d
  install -m 755 -o root -g root ${S}/debian/bkfw.init ${D}${sysconfdir}/init.d/bkfw

}

FILES_${PN} += " \
	    ${servicedir}/bkfw \
	    ${localstatedir}/lib/bkfw \
	    ${sysconfdir}/init.d/bkfw \
	    ${prefix}/local/bin/od \
	    "
