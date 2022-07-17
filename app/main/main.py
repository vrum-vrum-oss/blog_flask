from flask_login import login_remembered, login_required

from app.decorators import admin_required, permission_required
from . import main_bp
from ..models import Permission
from flask import render_template


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/administrator')
@login_required
@admin_required
def for_admins_only():
    return "For admins!"


@main_bp.route('/moderator')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"