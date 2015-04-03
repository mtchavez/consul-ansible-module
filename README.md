# Consul K/V Ansible Module

[![Latest Version](http://img.shields.io/github/release/mtchavez/consul-ansible-module.svg?style=flat-square)](https://github.com/mtchavez/consul-ansible-module/releases)
[![Build Status](https://travis-ci.org/mtchavez/consul-ansible-module.svg?branch=master)](https://travis-ci.org/mtchavez/consul-ansible-module)

An Ansible module to interact with consul's k/v API from your playbooks and roles.

## Usage

Examples

```yaml
# PUT a value for a key
- consul_kv: action=put key=foo value=bar

# PUT value with flag
- consul_kv: action=put key=bar/baz/bizzle value="shizzle" flags=23

# GET a value for a key
- consul_kv: action=get key=foo/bar/baz

# GET keys for prefix
- consul_kv: action=get key=bar keys=true
  register: bar_keys

# GET keys up to separator
- consul_kv: action=get key=bar/ keys=true separator='/'
  register: separator_keys

# DELETE a key
- consul_kv: action=delete key=foo/tmp

# DELETE a directory recursively
- consul_kv: action=delete key=foo/bar recurse=true
```

## Documentation

```yaml
module: consul_kv
version_added: "1.9"
author: Chavez
short_description: Interact with Consul K/V API
description:
   - Use Consul K/V API in your playbooks and roles
options:
  action:
    description:
      - HTTP verb [GET, PUT, DELETE]
    required: true
  dc:
    desription:
      - The datacenter to use
    required: false
    default: dc1
  cas:
    description:
      - Check and set parameter
    require: false
  flags:
    description:
      - Opaque flag to set as metadata for a key
    require: false
  host:
    description:
      - Consul host
    required: true
    default: 127.0.0.1
  key:
    description:
      - Key to interact with in K/V store
    required: true
  keys:
    description:
      - Return keys on a GET request for a given path
    required: false
    default: False
  port:
    description:
      - Consul API port
    required: true
    default: 8500
  recurse:
    description:
      - Recurse flag for DELETE or GET actions
    required: false
    default: False
  separator:
    description:
      - Separator to use when listing keys for a GET
    required: false
  value:
    description:
      - Value to set when adding or updating a key
    required: false
  version:
    description:
      - Consul API version
    required: true
    default: v1
```

## Testing

You will need to be running a consul server locally to run the test playbook.

Run consul with
  * DC1: `consul agent --server --bootstrap-expect=1 --data-dir=ci/consul/dc1/ --log-level=debug`
  * DC2: `consul agent --server --bootstrap-expect=1 --config-file=ci/consul/dc2/config.json --data-dir=ci/consul/dc2 --log-level=debug`

Then you can run the test playbook with `ansible-playbook -i ./hosts test-consul.yml`

## TODO

* Handle allowed URL params for API endpoints
* Handle sessions
  * Locking
  * Releasing
