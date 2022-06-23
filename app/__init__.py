from flask import Flask
from config import config
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from .main import main_bp
from .posts import posts_bp


# bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    
    # bootstrap.init_app(app)
    db.init_app(app)

    
    app.register_blueprint(main_bp)
    app.register_blueprint(posts_bp, url_prefix='/blog')


    return app