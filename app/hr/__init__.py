from flask import Blueprint

hr = Blueprint('hr', __name__)

from . import views
from . import forms