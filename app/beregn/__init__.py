from flask import Blueprint

bp = Blueprint('beregn', __name__)

from app.beregn import routes
