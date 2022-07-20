from flask_login import login_required
from . import posts_bp
from flask import render_template, request, redirect, url_for, flash, current_app, abort, make_response
from flask_login import current_user
from .. import db
from ..models import Permission, Post, Tag, Comment
from .forms import PostForm, CommentForm

@posts_bp.route('/')
def view():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    
    if q:
        posts = query.filter(Post.title.contains(q) | Post.body.contains(q)).order_by(Post.created.desc())
    else:
        posts = query.order_by(Post.created.desc())
    
    pages = posts.paginate(page=page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'], error_out=False)
    posts = pages.items

    return render_template('posts/blog_view.html', pages=pages, posts=posts, show_followed=show_followed)


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
    
    if current_user != post.author and \
        not current_user.can(Permission.ADMIN):
            abort(403)

    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        flash('The post has been updated', 'success')
        return redirect(url_for('posts.post_detail', slug=post.slug))

    return render_template('posts/edit_post.html', post=post, form=form)


@posts_bp.route('/<slug>', methods=['GET', 'POST'])
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first()
    tags = post.tags
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published', 'success')
        return redirect(url_for('posts.post_detail', slug=slug, page=-1))
    
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['BLOG_COMMENTS_PER_PAGE'] + 1
    pages = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['BLOG_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pages.items
    
    return render_template('posts/post_detail.html', posts=[post], tags=tags,
                                form=form, comments=comments, pages=pages)



def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)











@posts_bp.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter_by(slug=slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)


@posts_bp.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('posts.view')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@posts_bp.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('posts.view')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp