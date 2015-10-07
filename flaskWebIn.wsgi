#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/knowtology.com/httpdocs")

from app import create_app
application.secret_key = 'Add your secret key'