from flask_security import SQLAlchemyUserDatastore
from app.models import Role, User
from app.database import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
