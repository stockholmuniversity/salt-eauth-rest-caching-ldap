#!/usr/bin/env python3
# pylint: disable=R,C
from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request

api = Blueprint("api", __name__, url_prefix="/v1")


@api.route('/login', methods=['POST'])
def login():
    if "username" in request.form:
        username = request.form["username"]
        if username in app.cached_users:
            app.logger.error(app.cached_users[username])
            return jsonify(app.cached_users[username]), 200
        else:
            abort(401)
    else:
        abort(400)
