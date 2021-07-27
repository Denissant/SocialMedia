from datetime import date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login_manager
from app.tools.format_dob import calculate_age


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.id}. {self.name}'


class User(db.Model, UserMixin):
    """
    contains data about registered users
    each user may have posts linked to their profile
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255))

    name_first = db.Column(db.String)
    name_last = db.Column(db.String)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    sex = db.Column(db.String)
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    picture = db.Column(db.String)

    #  One-To-Many Relationships
    post = db.relationship('PostsModel', backref='User', uselist=False)
    comment = db.relationship('Comment', backref='User', uselist=False)

    #  Many-To-Many Relationship
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, name_first, name_last, email, dob, sex, password, role_id, age=None, picture=None):
        self.username = username
        self.name_first = name_first
        self.name_last = name_last
        self.email = email
        self.dob = dob
        self.sex = sex
        self.password = generate_password_hash(password)
        self.role_id = role_id
        self.age = calculate_age(dob)
        self.picture = picture

    def __repr__(self):
        return f'{self.id}. {self.username}'

    def check_password(self, password_raw):
        return check_password_hash(self.password, password_raw)

    def has_role(self, target_role):
        return target_role in (role.name for role in self.roles)

    @classmethod
    def find_by_username(cls, temp_username):
        return cls.query.filter_by(username=temp_username).first()

    @classmethod
    def find_by_email(cls, temp_email):
        return cls.query.filter_by(email=temp_email).first()


class FriendRequest(db.Model):
    ___tablename__ = 'friend_requests'

    id = db.Column(db.Integer, primary_key=True)
    send_date = db.Column(db.DateTime)
    active = db.Column(db.Boolean)
    recipient_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, sender_user, recipient_user, active=1, send_date=date.today()):
        self.recipient_user = recipient_user
        self.sender_user = sender_user
        self.active = active
        self.send_date = send_date

    def __repr__(self):
        return f'FriendRequest ID: {self.id}'

    def accept(self):
        self.active = 0
        db.session.commit()

    def decline(self):
        self.active = 0
        db.session.commit()


# catch an Exception and specify it instead of catching every exception
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except Exception as e:
        print(e)


