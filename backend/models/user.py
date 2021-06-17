import enum
from database import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class UserType(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(db.Model, SerializerMixin):
    serialize_only = ('id', 'username', 'email', 'created', 'user_type')

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String, nullable=False)
    user_type = db.Column(db.Enum(UserType))

    def __init__(self, username, email, password, user_type):
        self.username = username
        self.email = email
        self.password = password
        self.user_type = user_type
    
    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
