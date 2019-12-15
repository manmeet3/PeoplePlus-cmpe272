from flask import Blueprint

employee = Blueprint('employee', __name__)

from . import views