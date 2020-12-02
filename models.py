import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv('DATABASE_URL', 'sqlite:///localhost.sqlite'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    secret_number = db.Column(db.Integer)
