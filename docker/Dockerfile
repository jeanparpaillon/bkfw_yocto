FROM debian:bullseye
LABEL author="Jean Parpaillon <jean.parpaillon@free.fr>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt -y --force-yes install gawk wget git-core diffstat unzip texinfo gcc-multilib \
    build-essential chrpath socat autoconf automake libtool libglib2.0-dev \
    libarchive-dev cpio sudo locales curl libcapstone4

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8  

RUN groupadd -g 1000 jean && \
    useradd -m -s /bin/bash -u 1000 -g 1000 jean

USER jean
WORKDIR /home/jean

# ENTRYPOINT ["/bin/bash"]
