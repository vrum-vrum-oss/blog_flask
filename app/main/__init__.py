from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='templates')

from . import main
from ..models import Permission


# Make Permission variable available to all templates during rendering
@main_bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)