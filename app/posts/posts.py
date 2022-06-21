from . import posts_bp
from flask import render_template


@posts_bp.route('/')
def view():
    return render_template('posts/view.html')