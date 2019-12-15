from flask import Blueprint

manager = Blueprint('manager', __name__)

from . import views