#!/usr/bin/env python3
# pylint: disable=R,C

from caching_ldap.config import config
from caching_ldap import app, scheduler
from caching_ldap.ldapclient import LdapClient


def get_groups(*, search_base, search_filter):
    ldap_client = LdapClient()
    try:
        ldap_client.connect(config['ldap']['server'])
        groups = ldap_client.search_groups(search_base, search_filter)
    finally:
        ldap_client.disconnect()
    return {
        **groups,
        "su-ci-prod": [],
        "su-scm-prod": [],
    }


@scheduler.task('cron', minute='*/5')
def update_groups():
    app.cached_users = get_groups(
        search_base=config['ldap']['search_base'],
        search_filter=config['ldap']['search_filter'])
    app.logger.info('Updated %s users from LDAP', len(app.cached_users))
