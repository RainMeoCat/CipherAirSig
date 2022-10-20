from flask import Blueprint

airsign = Blueprint('airsign', __name__,)
from . import routes