#!/bin/bash


. /opt/asdf/asdf.sh
. ./poky/oe-init-build-env

exec /bin/bash "$@"
