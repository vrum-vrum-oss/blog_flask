from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from . import user_bp
from ..import db
from ..models import User



@user_bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)