DESCRIPTION = "Adafruit GPIO"
HOMEPAGE = "https://github.com/adafruit/Adafruit_Python_GPIO"
SECTION = "firmware"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

S = "${WORKDIR}/git"
# SRCREV = "38cd1bb542b09936672190be4a592b233e147626"
SRCREV="a6ec9ad3f72e586fd30af82e29e529c6c0c3e5bf"
SRC_URI = "git://github.com/jeanparpaillon/Adafruit_Python_GPIO;branch=rpi3"

PV = "0.2+git${SRCREV}"
PR = "r0"

RDEPENDS_${PN} += " \
	       python-modules \
	       python2-rpi-gpio \
	       "

inherit setuptools
