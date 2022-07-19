from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required, login_user, logout_user, current_user

from .forms import EditProfileForm

from . import user_bp
from ..import db
from ..models import User, Post



@user_bp.route('/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pages = user.posts.order_by(Post.created.desc()).paginate(
        page, per_page=current_app.config['BLOG_POSTS_PER_PAGE'],
        error_out=False)
    posts = pages.items
    return render_template('user.html', user=user, pages=pages, posts=posts)

    # if page and page.isdigit():
    #     page = int(page)
    # else:
    #     page = 1
    # pages = posts.paginate(page=page, per_page=2)
    # return render_template('user.html', user=user, pages=pages)


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