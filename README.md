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

## Configuration Files

### `config.ini`

This file contains the LDAP connection settings and ACL configuration. The default location is `/local/salt/conf/config.ini`, but you can override this by setting the `CONFIG_FILE` environment variable.

**Required sections:**

- **`[ldap]`** - LDAP server connection and search settings:
  - `server`: LDAP server URL (e.g., `ldaps://ldap.example.com`)
  - `search_base`: The base DN for LDAP searches (e.g., `ou=users,dc=example,dc=com`)
  - `search_filter`: LDAP search filter to find groups (e.g., `(&(objectClass=groupOfNames)(member={username}))`)
  - `port` (optional): LDAP port (default: 636 for LDAPS)

- **`[acl]`** - ACL configuration:
  - `acl_config`: Path to the `salt_acl.yaml` file

**Example:**
```ini
[ldap]
server = ldaps://ldap.example.com
search_base = ou=users,dc=example,dc=com
search_filter = (&(objectClass=groupOfNames)(member={username}))
port = 636

[acl]
acl_config = /path/to/salt_acl.yaml
```

### `salt_acl.yaml`

This file maps LDAP groups to Salt eauth ACLs. It defines which groups have access to which Salt commands.

**Format:**
```yaml
'ldap_group_name%':
  - 'salt_function_or_glob'
```

The `%` suffix indicates that the name is an LDAP group. Groups are matched exactly, and the functions can use globs for pattern matching.

The special key `'.*'` (without `%`) is the default ACL. It is added to the ACL of every user found in the LDAP cache, including users whose groups have no entry of their own in this file.

**Example:**
```yaml
'driftansvariga-configurationmanagement%':
  - '.*'  # Full access
'developers%':
  - 'test.ping'
  - 'state.highstate'
  - 'cmd.run'
'.*':  # Default for any user
  - 'test.ping'
```
