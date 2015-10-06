from flask import Blueprint

granules = Blueprint('granules', __name__)

from . import views

