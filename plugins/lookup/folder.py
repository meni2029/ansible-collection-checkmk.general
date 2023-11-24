# Copyright: (c) 2023, Lars Getwan <lars.getwan@checkmk.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: folder
    author: Lars Getwan (@lgetwan)
    version_added: "3.3.0"
    short_description: Get folder attributes
    description:
      - Returns the attributes of a folder
    options:
      _terms:
        description: complete folder path using tilde as a delimiter
        required: True
      server_url:
        description: URL of the Checkmk server
        required: True
      site:
        description: site name
        required: True
      automation_user:
        description: automation user for the REST API access
        required: True
      automation_secret:
        description: automation secret for the REST API access
        required: True
      validate_certs:
        description: Wether or not to validate TLS certificates
        type: boolean
        required: False
        default: True
"""

EXAMPLES = """
- name: Get the attributes of folder /tests
  ansible.builtin.debug:
    msg: "Attributes of folder /network: {{ attributes }}"
  vars:
    attributes: "{{
                    lookup('checkmk.general.folder',
                        '~tests',
                        server_url=my_server_url,
                        site=my_site,
                        automation_user=my_user,
                        automation_secret=my_secret,
                        validate_certs=False
                        )
                 }}"
"""

RETURN = """
  _list:
    description:
      - A list of dicts of attributes of the folder(s)
    type: list
    elements: str
"""

import json

from ansible.plugins.lookup import LookupBase
from ansible_collections.checkmk.general.plugins.module_utils.lookup_api import (
    CheckMKLookupAPI,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        server_url = self.get_option("server_url")
        site = self.get_option("site")
        user = self.get_option("automation_user")
        secret = self.get_option("automation_secret")
        validate_certs = self.get_option("validate_certs")

        site_url = server_url + "/" + site

        api = CheckMKLookupAPI(
            site_url=site_url,
            user=user,
            secret=secret,
            validate_certs=validate_certs,
        )

        ret = []

        for term in terms:
            response = json.loads(
                api.get("/objects/folder_config/" + term.replace("/", "~"))
            )
            ret.append(response.get("extensions"))

        return ret
