#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/codezero/")

from codezero import app as application
application.secret_key = 'your secret key'
