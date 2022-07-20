from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required, login_user, logout_user, current_user

from .forms import EditProfileForm

from . import user_bp
from ..import db
from ..models import Permission, User, Post

from app.decorators import permission_required



@user_bp.route('/<username>/')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pages = user.posts.order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pages.items
    return render_template('user.html', user=user, pages=pages, posts=posts)


@user_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated', category='success')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@user_bp.route('/<username>/follow')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash('Invalid user', 'danger')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash('You are already following this user')
        return redirect(url_for('user.user', username=username))
    
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username, 'success')
    return redirect(url_for('user.user', username=username))


@user_bp.route('/<username>/unfollow')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash('Invalid user', 'danger')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash('You are not following this user')
        return redirect(url_for('user.user', username=username))
    
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore' % username, 'info')
    return redirect(url_for('user.user', username=username))


@user_bp.route('/<username>/followers/')
def followers(username):
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash('Invalid user', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    pages = user.followers.paginate(
        page, per_page=current_app.config['BLOG_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pages.items]
    
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='user.followers', pages=pages,
                           follows=follows)
    
    
@user_bp.route('/<username>/followed_by/')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    
    if user is None:
        flash('Invalid user', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    pages = user.followed.paginate(
        page, per_page=current_app.config['BLOG_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pages.items]
    
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='user.followed_by', pages=pages,
                           follows=follows)