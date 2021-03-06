# Consul HTTP API Ansible Module

[![Latest Version](http://img.shields.io/github/release/mtchavez/consul-ansible-module.svg?style=flat-square)](https://github.com/mtchavez/consul-ansible-module/releases)
[![Build Status](https://travis-ci.org/mtchavez/consul-ansible-module.svg?branch=master)](https://travis-ci.org/mtchavez/consul-ansible-module)

An Ansible module to interact with consul's API from your playbooks and roles.

## API Endpoints

* [ACL](#acl)
* [Events](#events)
* [Key/Value](#keyvalue)
* [Session](#session)
* [Status](#status)

### [ACL](#acl)

#### Usage

```yaml
- name: Create ACL with defaults
  consul_acl:
    action: create
    token: "master-token"

- name: Update ACL
  consul_acl:
    action: update
    acl_id: "existing-acl-id"
    name: "updated-acl-name"
    token: "master-token"

- name: List ACL
  consul_acl:
    action: list
    token: "master-token"

- name: Get ACL replication
  consul_acl:
    action: replication
    token: "master-token"

- name: Get ACL info
  consul_acl:
    action: info
    acl_id: "asdf-1234-asdf-1234"
    token: "master-token"

- name: Destroy ACL
  consul_acl:
    action: destroy
    acl_id: "asdf-1234-asdf-1234"
    token: "master-token"

- name: Clone ACL
  consul_acl:
    action: clone
    acl_id: "asdf-1234-asdf-1234"
    token: "master-token"
```

#### Documentation

```yaml
---
module: consul_acl
version_added: "1.9"
author: Chavez
short_description: Interact with Consul ACL API
description:
   - Use Consul ACL API in your playbooks and roles
options:
  acl_type:
    description:
      - Type of ACL
    required: false
  action:
    description:
      - One of [create]
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
  name:
    description:
      - Name of event to fire
    required: false
  port:
    description:
      - Consul API port
    required: true
  rules:
    description:
      - ACL rules to set or update
    required: false
  token:
    description:
      - ACL token to use with requests
    required: false
  version:
    description:
      - Consul API version
    required: true
    default: v1
```


### [Events](#events)

#### Usage

Examples

```yaml
- name: Event new
  consul_event:
    action: fire
    name: deploy
  register: new_event

- name: Event new
  consul_event:
    action: list
  register: all_events

```

#### Documentation

```yaml
---
module: consul_events
version_added: "1.9"
author: Chavez
short_description: Interact with Consul Event API
description:
   - Use Consul Event API in your playbooks and roles
options:
  action:
    description:
      - One of [leader, peers]
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
  name:
    description:
      - Name of event to fire
    required: false
  node:
    description:
      - Node query filter for event fire
    required: false
  port:
    description:
      - Consul API port
    required: true
  service:
```

### [Key/Value](#keyvalue)

#### Usage

Examples

```yaml
- name: PUT a value for a key
  consul_kv:
    action: put
    key: foo
    value: bar

- name: PUT value with flag
  consul_kv:
    action: put
    key: bar/baz/bizzle
    value: shizzle
    flags: 23

- name: GET key for PUT with check and set
  consul_kv:
    action: get
    key: bar/baz/bizzle
  register: bizzle

- name: PUT check and set
  consul_kv:
    action: put
    key: bar/baz/bizzle
    value: "no shizzle"
    cas: "{{ item.ModifyIndex|int }}"
  with_items: bizzle.value

- name: PUT with session
  consul_kv:
    action: put
    key: razzle/acquired
    value: true
    acquire: "some-valid-session"

- name: PUT with session release
  consul_kv:
    action: put
    key: razzle/acquired
    value: true
    release: "some-valid-session"

- name: GET a value for a key
  consul_kv:
    action: get
    key: foo/bar/baz

- name: GET keys for prefix
  consul_kv:
    action: get
    key: bar
    keys: true
  register: bar_keys

- name: GET keys up to separator
  consul_kv:
    action: get
    key: bar/
    keys: true
    separator: "/"
  register: separator_keys

- name: DELETE a key
  consul_kv:
    action: delete
    key: foo/tmp

- name: DELETE a directory recursively
  consul_kv:
    action: delete
    key: foo/bar
    recurse: true
```

#### Documentation

```yaml
module: consul_kv
version_added: "1.9"
author: Chavez
short_description: Interact with Consul K/V API
description:
   - Use Consul K/V API in your playbooks and roles
options:
  acquire:
    - description:
      - Session to use for PUT requests
    required: false

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
  release:
    - description:
      - Session to release for PUT requests
    required: false
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

### [Session](#session)

#### Usage

Examples
```yaml
- name: Session create
  consul_session:
    action: create
    ttl: 15s
  register: session

- name: Get session info
  consul_session:
    action: info
    session: "{{ session.value.ID }}"
  register: session_info

- name: Session create with all params
  consul_session:
    action: create
    lock_delay: 25s
    node: "{{ item.Node }}"
    behavior: delete
    checks: ""
    ttl: 25s
  register: session_params
  with_items: "{{ session_info.value }}"

- name: Get session params info
  consul_session:
    action: info
    session: "{{ item.value.ID }}"
  register: session_params_info
  with_items: "{{ session_params.results }}"

- name: Get session renew
  consul_session:
    action: renew
    session: "{{ session.value.ID }}"
  register: session_renew

- name: List sessions
  consul_session:
    action: list
  register: all_sessions

- name: All sessions for a node
  consul_session:
    action: node
    node: "{{ item.Node }}"
  register: node_sessions
  with_items: "{{ session_info.value }}"

- name: Destroy session
  consul_session:
    action: destroy
    session: "{{ item }}"
  with_items:
    - "{{ session.value.ID }}"
    - "{{ session_params.results[0].value.ID }}"
```

#### Documentation
```yaml
module: consul_session
version_added: "1.9"
author: Chavez
short_description: Interact with Consul Sessions API
description:
   - Use Consul Sessions API in your playbooks and roles
options:
  action:
    description:
      - API session action [create, destroy, info, node, list, renew]
    required: true
  behavior:
    description:
      - Controls when the session is invalidated [release, delete]
    require: false
  checks:
    description:
      - List of associated health checks comma separated "foo,bar,baz"
    required: false
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
  lock_delay:
    description:
      - Time to delay the lock of the session
    require: false
  node:
    description:
      - Node name to set on create
    required: false
  port:
    description:
      - Consul API port
    required: true
  session:
    description:
      - Consul session to interact with
    require: false
  ttl:
    description:
      - Session TTL
    required: false
  version:
    description:
      - Consul API version
    required: true
    default: v1
```

### [Status](#status)

#### Usage

Examples

```yaml
- name: Get leader
  consul_status:
    action: leader
  register: leader

- name: Get peers
  consul_status:
    action: peers
  register: peers
```

#### Documentation
```yaml
module: consul_status
version_added: "1.9"
author: Chavez
short_description: Interact with Consul Status API
description:
   - Use Consul Status API in your playbooks and roles
options:
  action:
    description:
      - One of [leader, peers]
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
  port:
    description:
      - Consul API port
    required: true
  version:
    description:
      - Consul API version
    required: true
    default: v1

# informational: requirements for nodes
requirements: [ ]
```

## Testing

You will need to be running a consul server locally to run the test playbook.

Run consul with
  * DC1: `consul agent --server --bootstrap-expect=1 --data-dir=ci/consul/dc1/ --log-level=debug --config-file=ci/consul/dc1/config.json`
  * DC2: `consul agent --server --bootstrap-expect=1 --config-file=ci/consul/dc2/config.json --data-dir=ci/consul/dc2 --log-level=debug`

Then you can run the test playbook with `ansible-playbook -i ./hosts test-consul.yml`

## TODO

- ACL API
  - [x]  `/v1/acl/create`
  - [x]  `/v1/acl/update`
  - [x]  `/v1/acl/destroy/<id>`
  - [x]  `/v1/acl/info/<id>`
  - [x]  `/v1/acl/clone/<id>`
  - [x]  `/v1/acl/list`
  - [x]  `/v1/acl/replication`
- Agent API
  - [ ] `/v1/agent/checks`
  - [ ] `/v1/agent/services`
  - [ ] `/v1/agent/members`
  - [ ] `/v1/agent/self`
  - [ ] `/v1/agent/maintenance`
  - [ ] `/v1/agent/join/<address>`
  - [ ] `/v1/agent/force-leave/<node>`
  - [ ] `/v1/agent/check/register`
  - [ ] `/v1/agent/check/deregister/<checkID>`
  - [ ] `/v1/agent/check/pass/<checkID>`
  - [ ] `/v1/agent/check/warn/<checkID>`
  - [ ] `/v1/agent/check/fail/<checkID>`
  - [ ] `/v1/agent/check/update/<checkID>`
  - [ ] `/v1/agent/service/register`
  - [ ] `/v1/agent/service/deregister/<serviceID>`
  - [ ] `/v1/agent/service/maintenance/<serviceID>`
- Catalog API
  - [ ] `/v1/catalog/register`
  - [ ] `/v1/catalog/deregister`
  - [ ] `/v1/catalog/datacenters`
  - [ ] `/v1/catalog/nodes`
  - [ ] `/v1/catalog/services`
  - [ ] `/v1/catalog/service/<service>`
  - [ ] `/v1/catalog/node/<node>`
- Coordinate API
  - [ ] ` /v1/coordinate/datacenters`
  - [ ] ` /v1/coordinate/nodes`
- Events API
  - [x] fire
  - [x] list
- Health Checks API
  - [ ] `/v1/health/node/<node>`
  - [ ] `/v1/health/checks/<service>`
  - [ ] `/v1/health/service/<service>`
  - [ ] `/v1/health/state/<state>`
- Key/Value API
  - [x] GET
  - [x] PUT
  - [x] DELETE
  - [x] Session acquire PUT
  - [x] Session release PUT
- Prepared Queries API
  - [ ] `/v1/query`
  - [ ] `/v1/query/<query`
  - [ ] `/v1/query/<query or name>/execute`
  - [ ] `/v1/query/<query or name>/explain`
- Session API
  - [x] create
  - [x] destroy
  - [x] info
  - [x] node
  - [x] list
  - [x] renew
- Status API
  - [x] leader
  - [x] peers
