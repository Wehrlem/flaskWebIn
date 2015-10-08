from flask import Blueprint

orient = Blueprint('orient', __name__)

from . import views
