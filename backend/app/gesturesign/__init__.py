from flask import Blueprint

gsign = Blueprint('gsign', __name__,)
from . import routes