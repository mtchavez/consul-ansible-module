#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2013 Chavez <chavez@somewhere-cool.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import string


DOCUMENTATION = '''
---
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
  key:
    description:
      - Key to interact with in K/V store
    required: true
  value:
    description:
      - Value to set when adding or updating a key
    required: false

# informational: requirements for nodes
requirements: [ urllib2 ]
'''

EXAMPLES = '''
- consul_kv: action=put key=foo value=bar
'''

#
# Module execution.
#


def _build_url(params):
    return "http://%s:%s/%s/kv/%s" % (params['host'], params['port'], params['version'], params['key'])


def main():

    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True),
            dc=dict(required=False, default='dc1'),
            host=dict(required=False, default="127.0.0.1"),
            key=dict(required=True),
            port=dict(require=False, default=8500),
            value=dict(required=False),
            version=dict(required=False, default='v1'),
        ),
        supports_check_mode=True
    )

    ALLOWED_ACTIONS = ['GET', 'PUT', 'DELETE']
    GET, PUT, DELETE = ALLOWED_ACTIONS

    action = string.upper(module.params.get('action', ''))
    if not action or action not in ALLOWED_ACTIONS:
        module.fail_json(msg='Action is required and must be one of GET, PUT, DELETE')

    key = module.params.get('key', '')
    if not key:
        module.fail_json(msg='A key is required to interact with the k/v API')

    value = module.params.get('value', '')
    if action == PUT and not value:
        module.fail_json(msg='A value is required when using PUT')

    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=False)

    # Send the data to NewRelic
    url = _build_url(module.params)

    req = urllib2.Request(url=url)
    if action == PUT:
        req = urllib2.Request(url=url, data=value)
    if action != GET:
        req.get_method = lambda: action

    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        response = opener.open(req)
    except urllib2.URLError, e:
        module.fail_json(msg="API call failed: %s" % str(e))

    response_body = response.read()
    if action != GET and response_body == 'true':
        module.exit_json(changed=True, succeeded=True, key=key, value=value)
    else:
        module.fail_json(msg="Failed %s key: %s because %s" % (action, key, response_body))


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

main()
