from flask import Flask, redirect, url_for, request
# from app.decorators import admin_required
from config import config

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from flask_pagedown import PageDown

from flask_login import LoginManager, current_user


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


from app.admin import admin


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
    admin.init_app(app)
    pagedown.init_app(app)


    from .main import main_bp
    app.register_blueprint(main_bp)


    from .posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/blog')


    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    

    return app