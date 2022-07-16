from flask import Flask, redirect, url_for, request
# from app.decorators import admin_required
from config import config

from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment

from flask_admin import Admin
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink

from flask_login import LoginManager, current_user



class MyAdminIndexView(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_admin()
    
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class AdminModelView(ModelView):   
    def is_accessible(self):
        return current_user.is_admin()





bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
admin = Admin(index_view=MyAdminIndexView())



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




    from .main import main_bp
    app.register_blueprint(main_bp)


    from .posts import posts_bp
    app.register_blueprint(posts_bp, url_prefix='/blog')


    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')


    from .user import user_bp
    app.register_blueprint(user_bp, url_prefix='/user')


    from .models import Post, Tag, User, Role
    admin.init_app(app)
    admin.add_view(AdminModelView(Post, db.session, endpoint="post"))
    admin.add_view(AdminModelView(Tag, db.session))
    admin.add_view(AdminModelView(User, db.session, endpoint="users"))
    admin.add_view(AdminModelView(Role, db.session))
    admin.add_link(MenuLink(name='Public Website', url='/'))
    

    return app











# class MyModelView(ModelView):

#     def is_accessible(self):
#         return current_user.is_admin

#     # def inaccessible_callback(self, name, **kwargs):
#     # # redirect to login page if user doesn't have access
#     # return redirect(url_for('auth.login', next=request.url))