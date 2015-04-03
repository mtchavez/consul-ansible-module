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

import base64
import json
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
  port:
    description:
      - Consul API port
    required: true
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

# informational: requirements for nodes
requirements: [ urllib, urllib2 ]
'''

EXAMPLES = '''
# PUT a value for a key
- consul_kv: action=put key=foo value=bar

# GET a value for a key
- consul_kv: action=get key=foo/bar/baz

# DELETE a key
- consul_kv: action=delete key=foo/tmp

# DELETE a directory recursively
- consul_kv: action=delete key=foo/bar recurse=true
'''

#
# Module execution.
#


class ConsulKV(object):

    ALLOWED_ACTIONS = ['GET', 'PUT', 'DELETE']
    GET, PUT, DELETE = ALLOWED_ACTIONS

    ALLOWED_PARAMS = ['dc']

    def __init__(self, module):
        """Takes an AnsibleModule object to set up Consul K/V interaction"""
        self.module = module
        self.action = string.upper(module.params.get('action', ''))
        self.key = module.params.get('key', '')
        self.value = module.params.get('value', '')
        self.host = module.params.get('host', '127.0.0.1')
        self.dc = module.params.get('dc', 'dc1')
        self.port = module.params.get('port', 8500)
        self.recurse = module.params.get('recurse', False)
        self.version = module.params.get('version', 'v1')
        self._build_url()

    def run_cmd(self):
        self.validate()
        self._make_api_call()

    def validate(self):
        # Check action is allowed
        if not self.action or self.action not in self.ALLOWED_ACTIONS:
            self.module.fail_json(msg='Action is required and must be one of GET, PUT, DELETE')
        # A key is required for any call so make sure one exists
        if not self.key:
            self.module.fail_json(msg='A key is required to interact with the k/v API')
        # Validate action being used
        # ie self._validate_get(), self._validate_put(), self._validate_delete()
        getattr(self, "_validate_%s" % string.lower(self.action))

    def _build_url(self):
        self.api_url = "http://%s:%s/%s/kv/%s" % (self.host, self.port, self.version, self.key)

    def _validate_get(self):
        pass

    def _validate_put(self):
        if not self.value:
            self.module.fail_json(msg='A value is required when using PUT')

    def _validate_delete(self):
        pass

    def _make_api_call(self):
        req = self._setup_request()

        try:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            response = opener.open(req)
        except urllib2.URLError, e:
            self.module.fail_json(msg="API call failed: %s" % str(e))

        response_body = response.read()
        self._handle_response(response_body)

    def _query_params(self):
        params = {}
        if self.dc != 'dc1':
            params['dc'] = self.dc
        if self.action in [self.DELETE, self.GET] and self.recurse:
            params['recurse'] = 'true'
        return params

    def _setup_request(self):
        params = urllib.urlencode(self._query_params())
        if params:
            self.api_url = self.api_url + '?' + params
        req = urllib2.Request(url=self.api_url)
        if self.action == self.PUT:
            req = urllib2.Request(url=self.api_url, data=self.value)
        if self.action != self.GET:
            req.get_method = lambda: self.action

        return req

    def _handle_response(self, response_body):
        if self.action != self.GET and response_body == 'true':
            self.module.exit_json(changed=True, succeeded=True, key=self.key, value=self.value)
        elif self.action == self.GET:
            parsed_response = json.loads(response_body)
            # Decode values
            for obj in parsed_response:
                obj['Value'] = base64.decodestring(obj.get('Value', ''))
            self.module.exit_json(changed=True, succeeded=True, key=self.key, value=parsed_response)
        else:
            self.module.fail_json(msg="Failed %s key: %s because %s" % (self.action, self.key, response_body))


def main():

    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True),
            dc=dict(required=False, default='dc1'),
            host=dict(required=False, default="127.0.0.1"),
            key=dict(required=True),
            port=dict(require=False, default=8500),
            recurse=dict(require=False, default=False, type='bool'),
            value=dict(required=False),
            version=dict(required=False, default='v1'),
        ),
        supports_check_mode=True
    )

    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=False)

    consulkv = ConsulKV(module)
    consulkv.run_cmd()


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

main()
