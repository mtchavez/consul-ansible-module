#!/bin/bash
#
# Install and set up consul to run server for tests
#
set -ev

CONSUL_VER=0.5.0
CONSUL_DL_URL=https://dl.bintray.com/mitchellh/consul/${CONSUL_VER}_$(uname -s)_$(uname -m).zip

curl -L $CONSUL_DL_URL > $PWD/bin/consul
chmod +x $PWD/bin/consul

export PATH=$PATH:$PWD/bin
echo $PATH

consul agent --server=true --bootstrap-expect=1 --data-dir=.

# vim: ft=sh:
