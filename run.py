from app.commands import manager
from app.routes import list_pages, auth, success_register, logoff
from app.admin.admin_model import AdminModelView, ModModelView
from app import create_app

if __name__ == '__main__':
    manager.run()
