#!/usr/bin/python
import sys
import logging
from app import create_app
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/knowtology.com/httpdocs")

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
