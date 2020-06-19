from app import db

class Divida1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person1.id'))
    name = db.Column(db.String(98))
    price = db.Column(db.Float)
    data_vencimento = db.Column(db.String(29))
    is_pago = db.Column(db.Boolean)

    def __init__(self, name, price, data_vencimento, is_pago, person_id):
        self.name = name
        self.price = price
        self.data_vencimento = data_vencimento
        self.is_pago = is_pago
        self.person_id = person_id