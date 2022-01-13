DESCRIPTION = "ROA: BKTel Firmware LCD control"
HOMEPAGE = "http://github.com/jeanparpaillon/bkfw_roa"
SECTION = "firmware"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

PV = "1.8.0"
PR = "r0"

S = "${WORKDIR}/git"
SRCREV = "${PV}"
SRC_URI = "git://git@github.com/jeanparpaillon/bkore_roa_script.git;protocol=ssh"

RDEPENDS_${PN} += " \
	       python-modules \
	       python-requests \
	       python-crypt \
	       adafruit-charlcd \
	       "

inherit setuptools
