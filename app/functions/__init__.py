from flask import Blueprint

functions = Blueprint('functions', __name__)

from . import functions

