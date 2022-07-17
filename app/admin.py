from flask_login import current_user

from flask_admin import Admin
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink


from . import db


from .models import Post, Tag, User, Role


class MyAdminIndexView(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_admin()
    
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class AdminModelView(ModelView):   
    def is_accessible(self):
        return current_user.is_admin()


admin = Admin(index_view=MyAdminIndexView())


admin.add_view(AdminModelView(Post, db.session, endpoint="post"))
admin.add_view(AdminModelView(Tag, db.session))
admin.add_view(AdminModelView(User, db.session, endpoint="users"))
admin.add_view(AdminModelView(Role, db.session))
admin.add_link(MenuLink(name='Public Website', url='/'))