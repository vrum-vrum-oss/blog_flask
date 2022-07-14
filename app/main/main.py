from flask_login import login_remembered, login_required
from . import main_bp
from flask import render_template


@main_bp.route('/')
def index():
    return render_template('main/index.html')