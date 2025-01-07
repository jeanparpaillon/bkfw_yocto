#!/bin/sh

docker build -t bkfw-builder .
docker run \
    -it \
    -v /etc/password:/etc/password \
    -v /etc/group:/etc/group \
    -v /etc/shadow:/etc/shadow \
    -v /etc/sudoers:/etc/sudoers \
    -v /etc/sudoers.d:/etc/sudoers.d \
    -v /run/user/$(id -u):/run/user/$(id -u) \
    -v ${HOME}:/home/jean \
    bkfw-builder
    # -v $(cd .. && pwd):/sources 
