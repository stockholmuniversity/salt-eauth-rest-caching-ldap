#!/usr/bin/env python3
# pylint: disable=R,C
import string

import yaml
from caching_ldap import app


def get_acl_from_config():
    salt_acl_yaml = """
    'driftansvariga-configurationmanagement%':
      - '.*'
    '.*':
      - 'test.ping'
      - 'state.highstate'
    """
    groups = yaml.safe_load(salt_acl_yaml)
    app.logger.debug("Groups found in config: %r", groups)
    return groups


def get_acl_from_group(*, group):
    groups = get_acl_from_config()
    return groups.get(group + '%', [])
