from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes
from . import user_auth