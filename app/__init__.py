from flask import Flask
from config import config

# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
admin = Admin()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    
    # bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Post, Tag, User, Role
    admin.init_app(app)
    admin.add_view(ModelView(Post, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))


    from .main import main_bp
    app.register_blueprint(main_bp)


    from .posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/blog')


    return app