from database import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    verified = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, file_path):
        self.name = name.lower()
        self.file_path = file_path
