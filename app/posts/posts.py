from flask_login import login_required
from . import posts_bp
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from .. import db
from ..models import Permission, Post, Tag
from .forms import PostForm

@posts_bp.route('/')
def view():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    
    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q)).order_by(Post.created.desc())#.all()
    else:
        posts = Post.query.order_by(Post.created.desc())#.all()
    
    pages = posts.paginate(page=page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'], error_out=False)
    posts = pages.items

    return render_template('posts/blog_view.html', pages=pages, posts=posts)



@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.view'))

    return render_template('posts/create_post.html', form=form)


@posts_bp.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


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