DESCRIPTION = "AdafruitLCD controller"
HOMEPAGE = "https://github.com/adafruit/Adafruit_Python_CharLCD"
SECTION = "firmware"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

S = "${WORKDIR}/git"
SRCREV = "e5952eb4a9cc3d5dba9b7cc13e0eb1d4cf1733e1"
SRC_URI = "git://github.com/jeanparpaillon/Adafruit_Python_CharLCD"

PV = "0.1+git${SRCREV}"
PR = "r0"

RDEPENDS_${PN} += " \
	       python-modules \
	       adafruit-gpio \
	       "

inherit setuptools
