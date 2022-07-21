from flask import Blueprint

lepton = Blueprint('lepton', __name__,)
from . import routes