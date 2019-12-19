# caching\_ldap

caching\_ldap is an REST authorization API for [Salt's External Authentication
System (eauth)](https://docs.saltstack.com/en/latest/topics/eauth/index.html)
using the [eauth
rest](https://docs.saltstack.com/en/latest/ref/auth/all/salt.auth.rest.html).

You send in a username, password doesn't matter since we just authorize not
authenticate, and caching\_ldap give back an [eauth
ACL](https://docs.saltstack.com/en/latest/topics/eauth/index.html#external-authentication-system-configuration)
for that user which is expanded from cached LDAP groups refreshed on an interval.

## Usage

1. Configure your `external_auth` for your salt-master and salt-api:
   ```yaml
   eauth_acl_module: rest
   external_auth:
     rest:
       ^url: http://localhost:8080/v1/login
       'admins%':
         - '.*'
       'users%':
         - 'test.ping'
         - 'state.highstate'
   ```

1. Deploy this Flask-app on your salt master.
   ```terminal
   $ cd salt-eauth-rest-caching-ldap
   $ python3 -mvenv .
   $ source bin/activate
   $ pip3 install .
   ```
1. Serve `wsgi.py` with an [WGSI server](https://wsgi.readthedocs.io/en/latest/servers.html).
