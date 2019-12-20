#!/usr/bin/env python3
# pylint: disable=R,C
from flask import Blueprint, abort, jsonify, request

import caching_ldap.saltconfig
from caching_ldap import app

api = Blueprint("api", __name__, url_prefix="/v1")


@api.route('/login', methods=['POST'])
def login():
    if "username" in request.form:
        username = request.form["username"]
        if username in app.cached_users:
            app.logger.debug("Got groups %r for user %s",
                             app.cached_users[username], username)
            acls = []
            for group in app.cached_users[username]:
                acls.extend(
                    caching_ldap.saltconfig.get_acl_from_group(group=group))
            app.logger.debug("Returning ACL %r for user %s", acls, username)
            app.logger.info("Allowing user %r",
                            username,
                            extra={"user": username})
            return jsonify(acls), 200
        else:
            app.logger.info(
                "Denying user %r since they don't exist in cached_users",
                username,
                extra={"user": username})
            abort(401)
    else:
        abort(400)
