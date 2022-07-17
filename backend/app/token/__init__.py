from flask import Blueprint

token = Blueprint('token', __name__,)
from . import routes