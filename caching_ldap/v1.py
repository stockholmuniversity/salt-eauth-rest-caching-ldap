#!/usr/bin/env python3
# pylint: disable=R,C
from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/v1")


@api.route('/login', methods=['POST'])
def login():
    return {'great': "success"}, 200
