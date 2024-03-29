from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Post, Permission
from . import api_bp
from .decorators import permission_required
from .errors import forbidden


@api_bp.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pages = Post.query.paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pages.items
    prev = None
    if pages.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pages.has_next:
        next = url_for('api.get_posts', page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pages.total
    })


@api_bp.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api_bp.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api_bp.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    post.title = request.json.get('title', post.body)
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())