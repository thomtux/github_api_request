#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Thomas Langmar <thlan@mailbox.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


DOCUMENTATION = r'''
---
module: github_api_request
author: "Thomas Langmar (@thomtux)"
version_added: "1.0.0"
short_description: Get the latest release tag.
description: Get the latest release tag of a repository from github.
options:
    owner:
        description: The owner of the repository.
        required: true
        type: str
    repo:
        description: The repository name you want to ask.
        required: true
        type: str
requirements:
    - requests
'''

EXAMPLES = r'''
- name: Check latest version at github
    git_api_request:
      owner: "the name of the owner"
      repo: "the name of the repository"
    register: result

- name: Compare with your local installed version for example.
    debug:
      msg: "Version: {{ my_version.stdout, result.latest_release }}"
    when: my_version.stdout is version(result.latest_release, '<')

'''

RETURN = r'''
latest_release:
    description: The lateste release number.
    type: str
    returned: always
    sample: '1.0.0'
msg:
    description: The output message of the GitHub-API.
    type: str
    returned: always
    sample: 'Found'
'''

import requests
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        owner=dict(type='str', required=True),
        repo=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    url = f"https://api.github.com/repos/{module.params['owner']}/{module.params['repo']}/releases/latest"
    jsrequest = requests.get(url).json()

    if "message" in jsrequest and jsrequest["message"] == "Not Found":
        module.fail_json(msg=jsrequest["message"], meta=result)

    result['msg'] = "Found"
    result['latest_release'] = jsrequest["tag_name"]

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
