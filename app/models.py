from . import db
from sqlalchemy.sql import func
from datetime import datetime
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

