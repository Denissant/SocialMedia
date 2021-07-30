from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app import admin, db
from app.models import User, PostsModel, Comment, Role, FriendRequest, friendships
from app.tools.check_auth import check_auth


class AdminModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        if check_auth():
            return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


class ModModelView(ModelView):

    def is_accessible(self):
        if check_auth():
            return current_user.has_role('mod')

    def inaccessible_callback(self, name, **kwargs):
        abort(403)


admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(PostsModel, db.session))
admin.add_view(AdminModelView(Comment, db.session))
admin.add_view(AdminModelView(FriendRequest, db.session))
