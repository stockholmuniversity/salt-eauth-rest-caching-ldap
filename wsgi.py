#!/usr/bin/env python3
import os 

os.environ['CONFIG_FILE'] = '/local/salt/conf/config.ini'

from caching_ldap import app as application
