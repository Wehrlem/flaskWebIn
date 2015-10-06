from flask import Blueprint

experts = Blueprint('experts', __name__)

from . import views

