#!/usr/bin/env python3
# pylint: disable=R,C
import os

import werkzeug
from flask import Flask
from flask_apscheduler import APScheduler

if os.environ.get("FLASK_ENV") == 'development':
    from su.logging import logging, console, structured  # noqa: F401
else:
    from su.logging import logging, structured  # noqa: F401

app = Flask(__name__)

app.logger.setLevel(logging.INFO)

# v1 imports app, so it must exist before we import v1
from caching_ldap.v1 import api as api_v1  # isort:skip # noqa: E402
app.register_blueprint(api_v1)

scheduler = APScheduler()
scheduler.api_enabled = False
scheduler.init_app(app)
scheduler.start()

# Must be after app and scheduler is initialized.
from caching_ldap import cronjobs  # isort:skip # noqa: E402 F401

app.cached_users = {}

# TODO:
# * configure
#   * ldap
#     * server/url
#     * ldap-credentials
#     * search_base
#     * search_filter
#   * salt acl config file
#   * logging levels
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

@app.before_first_request
def before_first_request():
    # Make sure app.cached_users is initialized when receiving the first
    # request to the app
    if not app.cached_users:
        cronjobs.update_groups()

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
