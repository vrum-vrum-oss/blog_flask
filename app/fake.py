from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post


def users(count=10):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='caterpillar',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_datetime().strftime('%Y-%m-%d %H:%M:%S'),
                 last_seen=fake.past_datetime().strftime('%Y-%m-%d %H:%M:%S'),
                )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=10):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(title=fake.sentence(),
                 body=fake.text(),
                 created=fake.past_datetime(),
                 author=u,
                )
        db.session.add(p)
    db.session.commit()