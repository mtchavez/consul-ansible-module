# Consul K/V Ansible Module

[![Latest Version](http://img.shields.io/github/release/mtchavez/consul-ansible-module.svg?style=flat-square)](https://github.com/mtchavez/consul-ansible-module/releases)
[![Build Status](https://travis-ci.org/mtchavez/consul-ansible-module.svg?branch=master)](https://travis-ci.org/mtchavez/consul-ansible-module)

An Ansible module to interact with consul's k/v API from your playbooks and roles.

## Usage

Examples

```yaml
# PUT a value for a key
- consul_kv: action=put key=foo value=bar

# GET a value for a key
- consul_kv: action=get key=foo/bar/baz

# DELETE a key
- consul_kv: action=delete key=foo/tmp

# DELETE a directory recursively
- consul_kv: action=delete key=foo/bar recurse=true

# GET keys for prefix
- consul_kv: action=get key=bar keys=true
  register: bar_keys
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

Run consul with `consul agent --server=true --bootstrap-expect=1 --data-dir=.`
which will run a single node server.

Then you can run the test playbook with `ansible-playbook -i ./hosts test-consul.yml`


## TODO

* Handle allowed URL params for API endpoints
* Handle sessions
  * Locking
  * Releasing
* GET only keys under a given prefix
* Recursive GET for keys under a given prefix
