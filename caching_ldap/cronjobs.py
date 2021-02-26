#!/usr/bin/env python3
# pylint: disable=R,C
import datetime

from caching_ldap import app, scheduler


def get_groups(*, search_base, search_filter):
    _, _ = search_base, search_filter
    return {
        "frkj4220": ["driftansvariga-configurationmanagement"],
        "simlu": ["driftansvariga-configurationmanagement"],
        "su-ci-prod": [],
    }


@scheduler.task('cron', minute='*/5')
def update_groups():
    app.cached_users = get_groups(
        search_base='ou=driftansvariga,ou=Groups,dc=it,dc=su,dc=se',
        search_filter='cn=driftansvariga-*')
    app.logger.info('Updated %s users from LDAP', len(app.cached_users))
