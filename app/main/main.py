from flask_login import login_remembered, login_required

from app.decorators import admin_required, permission_required
from . import main_bp
from ..models import Permission
from flask import render_template, abort, current_app, request

from flask_sqlalchemy import get_debug_queries


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


@main_bp.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main_bp.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['BLOG_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                    (query.statement, query.parameters, query.duration, query.context))
    return response
