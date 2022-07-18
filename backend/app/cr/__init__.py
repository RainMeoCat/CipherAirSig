from flask import Blueprint

cr = Blueprint('cr', __name__,)
from . import routes