DESCRIPTION = "Python requests"
HOMEPAGE = "http://python-requests.org/"
SECTION = "python/devel"
LICENSE = "CLOSED"

PACKAGES = "${PN}"

S = "${WORKDIR}/git"
SRCREV = "v2.10.0"
SRC_URI = "git://github.com/kennethreitz/requests"

PV = "2.10.0"
PR = "r0"

RDEPENDS_${PN} += " \
	       python-modules \
	       python-urllib3 \
	       "

inherit setuptools
