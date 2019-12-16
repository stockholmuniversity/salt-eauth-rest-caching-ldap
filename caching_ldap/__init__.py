#!/usr/bin/env python3
# pylint: disable=R,C
import werkzeug
from flask import Flask

from caching_ldap.v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1)

# TODO:
# * cron which:
#   * finds all driftansvariga-*-groups and add them to cached_users[uid]
# * On /login
#   * Get all groups from cached_users[uid]
#   * Read the yaml config
#   * Create list returned_acl
#   * iterate over each group key e.g.
#     'driftansvariga-configurationmanagement%':
#     * if it exists in cached_users[uid]:
#       * add it to a returned_acl
#   * return returned_acl

@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_http_errors(e):
    return {"description": e.description, "code": e.code}, e.code


@app.errorhandler(Exception)
def handle_exceptions(e):
    app.logger.exception(e)
    return {"description": "Internal Server Error", "code": 500}, 500


@app.route('/status')
def status():
    return {'status': 'OK'}, 200


if __name__ == '__main__':
    app.run()
