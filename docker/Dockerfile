FROM debian:buster
LABEL author="Jean Parpaillon <jean.parpaillon@free.fr>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt -y --force-yes install gawk wget git-core diffstat unzip texinfo gcc-multilib \
    build-essential chrpath socat autoconf automake libtool libglib2.0-dev \
    libarchive-dev cpio sudo locales curl libcapstone3 \
    liblzma-dev libsqlite3-dev libreadline-dev libncurses5-dev libssl-dev libbz2-dev

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

RUN groupadd -g 1000 jean && \
    useradd -m -s /bin/bash -u 1000 -g 1000 jean
RUN addgroup jean sudo

USER jean

ENV ASDF_DIR=/opt/asdf
ADD asdf /opt/asdf
RUN . /opt/asdf/asdf.sh && \
    asdf plugin add python && \
    asdf install python 3.6.15 && \
    asdf global python 3.6.15

COPY docker-entrypoint.sh /docker-entrypoint.sh

WORKDIR /home/jean/BA_Projets/bktel/git/bkfw_yocto

ENTRYPOINT ["/docker-entrypoint.sh"]
