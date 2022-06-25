from . import posts_bp
from flask import render_template
from .. import db
from ..models import Post


@posts_bp.route('/')
def view():
    posts = Post.query.all()

    return render_template('posts/blog_view.html', posts=posts)


@posts_bp.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first()
    return render_template('posts/post_detail.html', post=post)