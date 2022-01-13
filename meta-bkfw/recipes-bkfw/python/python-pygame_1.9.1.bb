DESCRIPTION = "Python Game Engine"
HOMEPAGE = "http://www.pygame.org"
SECTION = "devel/python"
LICENSE = "LGPL"
LIC_FILES_CHKSUM = "file://LGPL;md5=7fbc338309ac38fefcd64b04bb903e34"

SRCNAME = "pygame"
PR = "r0"

# SETUP DEPENDS
DEPENDS = "tiff zlib libpng jpeg libsdl libsdl-ttf libsdl-image libsdl-mixer flac libmikmod libvorbis"

SRC_URI = "http://www.pygame.org/ftp/${SRCNAME}-${PV}release.tar.gz \
           file://pygame-1.9.1release.patch "

S = "${WORKDIR}/${SRCNAME}-${PV}release"

inherit distutils

#DEPENDS += "python-setuptools-native"

DISTUTILS_INSTALL_ARGS = "--root=${D} \
    --prefix=${prefix} \
    --install-lib=${PYTHON_SITEPACKAGES_DIR} \
    --install-data=${datadir}"

COMPATIBLE_MACHINE = "(raspberrypi|carhud)"

# COPY Setup.in TO Setup SO WE HAVE A BASIS TO START FROM
do_configure() {
         cp ${S}/Setup.in ${S}/Setup
}

#do_compile_prepend() {
#         echo $STAGING_LIBDIR
#         echo $STAGING_INCDIR
#}

SRC_URI[md5sum] = "1c4cdc708d17c8250a2d78ef997222fc"
SRC_URI[sha256sum] = "a26095472ae4be9631e0d5bfb9a52ac57a3a091e45757913128e4a473807d433"
