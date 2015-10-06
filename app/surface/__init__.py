from flask import Blueprint

surface = Blueprint('surface', __name__)

from . import views

