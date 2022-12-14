#!/bin/bash -

apt-get update -y
apt-get upgrade -y
curl apt-transport-https ssl-cert ca-certificates gnupg lsb-release \
      build-essential autoconf libtool libbz2-dev libz-dev \
      liblzma-dev libzstd-dev libcurl4-openssl-dev libssl-dev libsystemd-dev \
      yasm liblz4-dev liblzo2-dev librdkafka-dev libsqlite3-dev sqlite autoconf-archive

cd /root

curl -LO https://github.com/LibtraceTeam/wandio/archive/refs/tags/4.2.4-1.tar.gz && \
  tar xf 4.2.4-1.tar.gz && \
  cd wandio-4.2.4-1 && \
  autoreconf -sif && \
  ./configure --prefix=/usr \
    --with-bzip2 \
    --with-zlib \
    --with-lzma \
    --with-zstd \
    --with-lz4 \
    --with-http && \
  make -j$(nproc) && \
  make install && \
  rm -rf 4.2.4-1.tar.gz wandio-4.2.4-1

cp configure.ac.patch /tmp/01-configure.ac.patch

curl -LO https://github.com/CAIDA/libbgpstream/releases/download/v2.2.0/libbgpstream-2.2.0.tar.gz && \
  tar xf libbgpstream-2.2.0.tar.gz && \
  cd libbgpstream-2.2.0 && \
  patch configure.ac < /tmp/01-configure.ac.patch  && \
  autoreconf -sif && \
  ./configure --prefix=/usr \
    --with-sqlite && \
  make -j$(nproc) && \
  make check && \
  make install && \
  rm -rf libbgpstream-2.2.0.tar.gz libbgpstream-2.2.0
  
pip install pybgpstream
