#!/usr/bin/python
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/vhosts/knowtology.com/httpdocs")

from app import create_app

application = create_app('default')

