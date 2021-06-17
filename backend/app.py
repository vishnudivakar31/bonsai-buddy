from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.user_api import user_api
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:interOP123@localhost:5432/bonsai-buddies'
db.init_app(app)
app.register_blueprint(user_api)

def setup_database():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    setup_database()
    app.run(debug=True, port=5000)
