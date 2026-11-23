#!/usr/bin/env python3
# pylint: disable=R,C
import yaml
from caching_ldap import app
from caching_ldap.config import config

# Key in the ACL config whose ACL applies to every cached user
DEFAULT_ACL_KEY = '.*'


def get_acl_from_config():
    """Get access control list from configuration."""
    salt_acl_yaml = """
    'driftansvariga-configurationmanagement%':
      - '.*'
    '.*':
      - 'test.ping'
      - 'state.highstate'
    """
    salt_acl_yaml = config['acl'].get('acl_config', salt_acl_yaml)
    with open(salt_acl_yaml, 'r') as f:
        salt_acl_yaml = f.read()
    groups = yaml.safe_load(salt_acl_yaml)
    app.logger.debug("Groups found in config: %r", groups)
    return groups


def get_acl_from_groups(*, groups):
    """Get the merged ACL for the groups plus the default ACL for any user."""
    acl_config = get_acl_from_config()
    acls = []
    for key in [group + '%' for group in groups] + [DEFAULT_ACL_KEY]:
        for entry in acl_config.get(key) or []:
            if entry not in acls:
                acls.append(entry)
    return acls
