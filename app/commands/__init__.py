from flask_migrate import MigrateCommand
from flask_script import Manager, Server

from app import create_app
from .db_populate import InitDbCommand

app = create_app()

manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('db_populate', InitDbCommand)
manager.add_command('runserver', Server(port=5080))
