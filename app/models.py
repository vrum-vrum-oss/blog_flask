from . import db, login_manager
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app

import re
import jwt
import hashlib
from datetime import datetime, timezone


def slugify(s):
    pattern = r'[\W_]+'
    temp = re.sub(pattern, '_', s).lower()
    return re.sub('_$','', temp)


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=func.now(), index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()


    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    
    def __repr__(self):
        return '<Tag id: {}, name: {}>'.format(self.id, self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id =db.Column(db.Integer, db.ForeignKey('role.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=func.now())
    last_seen = db.Column(db.DateTime(), default=func.now())
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.role is None:
            # set the admin or default role depending on email address
            if self.email == current_app.config['BLOG_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
            if self.email is not None and self.avatar_hash is None:
                self.avatar_hash = self.gravatar_hash()


    def __repr__(self):
        return '<User: {}>'.format(self.username)


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self,expiration=3600):
        token = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token


    def confirm(self, token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def generate_reset_token(self, expiration=3600):
        token = jwt.encode(
            {
                "reset": self.id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return token


    @staticmethod
    def reset_password(token, new_password):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True


    # Add helper methods self.can and self.is_admin
    # to simplify implementation of roles and permissions
    def can(self, perm):
        # Check if the requested permission is present in the role
        return self.role is not None and self.role.has_permission(perm)


    def is_admin(self):
        # Check for administration permissions
        return self.can(Permission.ADMIN)


    def ping(self):
        self.last_seen = func.now()
        db.session.add(self)
        db.session.commit()


    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()


    def gravatar(self, size=100, default='monsterid', rating='g'):
        url = 'https://gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                url=url, hash=hash, size=size, default=default, rating=rating)



class AnonymousUser(AnonymousUserMixin):
    """
    Implementing custom anonymous user class enables the app
    to call current_user.can() and current_user.is_admin()
    without having to check whether the user is looged in first
    """
    def can(self, permissions):
        return False


    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    """
    Users are assigned a descrete role. Each role defines what actions
    it allows to perform through a list of permissions.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # True only for one role which is assigned to new users upon registration
    default = db.Column(db.Boolean, default=False, index=True)
    permissions= db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    def __repr__(self):
        return '<Role: {}>'.format(self.name)


    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm


    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm


    def reset_permission(self):
        self.permissions = 0


    def has_permission(self, perm):
        """
        Check if a combined permission value includes the given permission
        using bitwise AND operator
        """
        return self.permissions & perm == perm


    @staticmethod
    def insert_roles():
        """
        Add roles and permissions to the database automatically
        """
        roles = {
            'User':    [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Mod':     [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
                        Permission.MODERATE],
            'Admin':   [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
                        Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    
class Permission:
    """ 
    Permission values are stored as powers of two. It allows permissions
    to be combined, giving each possible combination of permissions
    a unique value
    """
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
