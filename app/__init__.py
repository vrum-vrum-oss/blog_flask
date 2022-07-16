from flask import Flask
from sqlalchemy import true
from config import config

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import LoginManager


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
# admin = Admin()



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    moment.init_app(app)
    login_manager.init_app(app)


    from .models import Post, Tag, User, Role
    # admin.init_app(app)
    # admin.add_view(ModelView(Post, db.session))
    # admin.add_view(ModelView(Tag, db.session))
    # admin.add_view(ModelView(User, db.session))
    # admin.add_view(ModelView(Role, db.session))


    from .main import main_bp
    app.register_blueprint(main_bp)


    from .posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/blog')


    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    from .user import user_bp
    app.register_blueprint(user_bp)


    return app