from . import posts_bp
from flask import render_template
from .. import db
from ..models import Post, Tag


@posts_bp.route('/')
def view():
    posts = Post.query.all()
    return render_template('posts/blog_view.html', posts=posts)


@posts_bp.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)


@posts_bp.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter_by(slug=slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)