#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2015 Chavez <chavez@somewhere-cool.com>
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

import json
import string
import urllib

from collections import OrderedDict

DOCUMENTATION = '''
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

# informational: requirements for nodes
requirements: [ ]
'''

EXAMPLES = '''
- name: Create ACL with defaults
  consul_acl:
    action: create
    token: "master-token"
'''

#
# Module execution.
#


class ConsulACL(object):

    ALLOWED_ACTIONS = ['create', 'update']
    CREATE, UPDATE = ALLOWED_ACTIONS

    PUT_ACTIONS = [CREATE, UPDATE]
    GET_ACTIONS = []

    def __init__(self, module):
        """Takes an AnsibleModule object to set up Consul Event interaction"""
        self.module = module
        self.acl_id = module.params.get('acl_id', None)
        self.action = string.lower(module.params.get('action', ''))
        self.dc = module.params.get('dc', 'dc1')
        self.host = module.params.get('host', '127.0.0.1')
        self.port = module.params.get('port', 8500)
        self.version = module.params.get('version', 'v1')
        self.name = module.params.get('name', '')
        self.rules = module.params.get('rules', '')
        self.token = module.params.get('token', '')
        self.acl_type = module.params.get('acl_type', 'client')
        self.params = OrderedDict({})
        self.req_data = ''
        self._build_url()

    def run_cmd(self):
        self._make_api_call()

    def validate(self):
        # Check action is allowed
        if not self.action or self.action not in self.ALLOWED_ACTIONS:
            self.module.fail_json(msg='Action is required and must be one of %r' % self.ALLOWED_ACTIONS)
        # Validate action being used
        # ie self._validate_list(), self._validate_fire()
        getattr(self, "_validate_%s" % self.action)

    def _build_url(self):
        self.api_url = "http://%s:%s/%s/acl/%s" % (self.host, self.port, self.version, self.action)

    def _http_verb_for_action(self):
        if self.action in self.PUT_ACTIONS:
            return 'PUT'
        return 'GET'

    def _validate_update(self):
        if not self.acl_id:
            self.module.fail_json(msg='An ACL ID is required when updating an ACL')


    def _make_api_call(self):
        self._setup_request()

        try:
            (response, info) = fetch_url(module, self.api_url, data=self.req_data, method=self._http_verb_for_action())
        except Exception, e:
            self.module.fail_json(msg="API call ({}) failed: {}".format(self.api_url, str(e)))

        try:
            response_body = response.read()
            self._handle_response(response, response_body)
        except AttributeError, e:
            self.module.fail_json(msg="Parsing response failed: {}, info: {}".format(str(e), info))

    def _setup_request(self):
        params = urllib.urlencode(self._query_params())
        if params:
            self.api_url = self.api_url + '?' + params
        if self.action == self.CREATE:
            self._add_create_body()
        if self.action == self.UPDATE:
            self._add_update_body()
        if self.action in self.PUT_ACTIONS:
            if self.params:
                self.req_data = json.dumps(self.params)

    def _query_params(self):
        params = OrderedDict({})
        if self.dc != 'dc1':
            params['dc'] = self.dc
        if self.token:
            params['token'] = self.token
        return params


    def _add_create_body(self):
        valid_attrs = {
          "name": "Name",
          "acl_type": "Type",
          "rules": "Rules"
        }
        for attr, name in valid_attrs.iteritems():
            if hasattr(self, attr) and getattr(self, attr):
                self.params[name] = getattr(self, attr)

    def _add_update_body(self):
        valid_attrs = {
          "acl_id": "ID",
          "name": "Name",
          "acl_type": "Type",
          "rules": "Rules"
        }
        for attr, name in valid_attrs.iteritems():
            if hasattr(self, attr) and getattr(self, attr):
                self.params[name] = getattr(self, attr)

    def _handle_response(self, response, response_body):
        code = response.getcode()
        if code != 200:
            self.module.fail_json(msg="Failed with code %i and response %s" % (code, response_body))
        else:
            try:
                parsed_response = json.loads(response_body)
            except:
                parsed_response = ''
            self.module.exit_json(changed=True, succeeded=True, value=parsed_response)


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            acl_type=dict(required=False, default='client'),
            acl_id=dict(required=False, default=''),
            action=dict(required=True),
            dc=dict(required=False, default='dc1'),
            host=dict(required=False, default='127.0.0.1'),
            name=dict(required=False, default=''),
            port=dict(require=False, default=8500),
            rules=dict(required=False, default=''),
            token=dict(required=False, default=''),
            version=dict(required=False, default='v1'),
        ),
        supports_check_mode=True
    )

    # If we're in check mode, just exit pretending like we succeeded
    if module.check_mode:
        module.exit_json(changed=False)

    consul_status = ConsulACL(module)
    consul_status.run_cmd()


# import module snippets
from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == '__main__':
    main()
