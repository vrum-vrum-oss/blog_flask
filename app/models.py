from . import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

import re


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
    created = db.Column(db.DateTime, default=func.now())

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id =db.Column(db.Integer, db.ForeignKey('role.id'))
    password_hash = db.Column(db.String(128))


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

    



class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')


    def __repr__(self):
        return '<Role: {}>'.format(self.name)

    

