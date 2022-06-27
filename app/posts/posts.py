from shutil import register_unpack_format
from . import posts_bp
from flask import render_template, request, redirect, url_for
from .. import db
from ..models import Post, Tag
from .forms import PostForm

@posts_bp.route('/', methods=['GET', 'POST'])
def view():
    q = request.args.get('q')
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).all()
    else:
        posts = Post.query.order_by(Post.created.desc()).all()
    return render_template('posts/blog_view.html', posts=posts)


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        try:
            post = Post(title=title, body=body)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something wrong')

        return redirect(url_for('posts.view'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


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