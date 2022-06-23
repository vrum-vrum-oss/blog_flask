from app import db
from datetime import datetime
import re


def slugify(s):
    pattern = r'[\W_]+'
    return re.sub(pattern, '_', s).lower()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()


    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

