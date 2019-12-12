#!/usr/bin/env python3
# pylint: disable=R,C
from flask import Blueprint, abort
from flask import current_app as app
from flask import request

api = Blueprint("api", __name__, url_prefix="/v1")


@api.route('/login', methods=['POST'])
def login():
    if "username" in request.form:
        return {'great': "success"}, 200
    else:
        abort(400)
