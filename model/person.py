from app import db
from model.debt import Divida1


class Person1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    divida = db.relationship(Divida1)
    name = db.Column(db.String(98))
    email = db.Column(db.String(148))

    def __init__(self, name, email):
        self.name = name
        self.email = email
