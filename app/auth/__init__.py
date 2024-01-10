from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes
from . import user_auth
from . import doctor_auth
from . import admin_auth