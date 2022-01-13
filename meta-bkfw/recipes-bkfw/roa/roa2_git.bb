DESCRIPTION = "ROA: BKTel Firmware Touchscreen control"
HOMEPAGE = "http://github.com/jeanparpaillon/bkfw_roa"
SECTION = "firmware"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

PV = "1.7.0b0"
PR = "r0"

S = "${WORKDIR}/git"
SRCREV = "${PV}"
SRC_URI = "git://git@github.com/jeanparpaillon/bkfw_roa.git;protocol=ssh;branch=roa2"

# Python
RDEPENDS_${PN} += " \
	       python-modules \
	       python-requests \
	       python-crypt \
	       "

# SDL
RDEPENDS_${PN} += "libsdl jpeg libsdl-dev libsdl-ttf libsdl-ttf-dev libsdl-mixer libsdl-mixer-dev libsdl-image libsdl-image-dev"

# RASPBERRY PI GPIO
RDEPENDS_${PN} += "adafruit-gpio"

# PYGAME
RDEPENDS_${PN} += "python-pygame"

inherit setuptools
