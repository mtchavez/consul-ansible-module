#!/bin/bash
#
# Install and set up consul to run server for tests
#
set -ev

OS_NAME=`uname -s | awk '{print tolower($0)}'`
CONSUL_VER=0.7.0
CONSUL_DL_URL=https://releases.hashicorp.com/consul/${CONSUL_VER}/consul_${CONSUL_VER}_${OS_NAME}_amd64.zip

curl -L $CONSUL_DL_URL > consul.zip
unzip -o consul.zip -d $PWD/bin/
chmod +x $PWD/bin/consul

export PATH=$PATH:$PWD/bin

# DC1
consul agent --server=true --bootstrap-expect=1 --data-dir=$PWD/ci/consul/dc1 --config-file=$PWD/ci/consul/dc1/config.json &

sleep 25

consul agent --server=true --bootstrap-expect=1 --data-dir=$PWD/ci/consul/dc2 --config-file=$PWD/ci/consul/dc2/config.json &

sleep 25

# vim: ft=sh:
