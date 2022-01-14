DESCRIPTION = "ROA: BKTel Firmware LCD control"
HOMEPAGE = "http://github.com/jeanparpaillon/bkfw_roa"
SECTION = "firmware"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

PV = "1.8.0"
PR = "r0"

S = "${WORKDIR}/git"
SRCREV = "${PV}"
SRC_URI = "file://roa_2edfa/roa.py \
	 	   file://roa_2edfa/factory.config"

RDEPENDS_${PN} += " \
		   python \
	       python-modules \
	       python-requests \
	       python-crypt \
		   adafruit-charlcd \
	       "

do_install() {
	install -d ${D}/usr/bin
	install -m 755 -o root -g root ${WORKDIR}/roa_2edfa/roa.py ${D}/usr/bin/roa.py
	install -d ${D}${localstatedir}/lib/bkfw
	install -m 644 -o root -g root ${WORKDIR}/roa_2edfa/factory.config ${D}${localstatedir}/lib/bkfw/factory.config
}
