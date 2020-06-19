from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySql2020!@localhost/workshop-python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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


@app.route('/divida')
def index():
    dividas = Divida1.query.all()

    result = []
    for divida in dividas:
        person = Person1.query.get(divida.person_id)
        data = {
            "id": divida.id,
            "name": divida.name,
            "person": person.name,
            "price": divida.price,
            "data_vencimento": divida.data_vencimento,
            "Pago": divida.is_pago
        }
        result.append(data)

    return jsonify(result)


@app.route('/divida', methods=['POST'])
def insert_divida():
    name = request.json['name']
    price = request.json['price']
    data_vencimento = request.json['data_vencimento']
    is_pago = request.json['is_pago']
    person_id = request.json['person_id']
    divida = Divida1(name, price, data_vencimento, is_pago, person_id)

    db.session.add(divida)
    db.session.commit()

    return f"{name} inserida com sucesso"


@app.route('/divida/<id>', methods=['GET'])
def get_divida(id):
    divida = Divida1.query.get(id)
    person = Person1.query.get(divida.person_id)

    result = {
        "id": divida.id,
        "name": divida.name,
        "person": person.name,
        "price": divida.price,
        "data_vencimento": divida.data_vencimento,
        "is_pago": divida.is_pago,
        "pserson_id": divida.person_id
    }

    return jsonify(result)


@app.route('/divida/<id>', methods=['PUT'])
def update_divida(id):
    divida = Divida1.query.get(id)
    divida.name = request.json['name']
    divida.price = request.json['price']
    divida.data_vencimento = request.json['data_vencimento']
    divida.is_pago = request.json['is_pago']
    divida.person_id = request.json['person_id']
    db.session.commit()

    return f"A Dívida {divida.name} foi atualizada com sucesso"


@app.route('/divida/<id>', methods=['DELETE'])
def delete_divida(id):
    divida = Divida1.query.get(id)
    db.session.delete(divida)
    db.session.commit()

    return f"A Dívida {divida.name} foi deletada com sucesso"


#--------------Person--------------#

class Person1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    divida = db.relationship("Divida1")
    name = db.Column(db.String(98))
    email = db.Column(db.String(148))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route('/person')
def index_person():
    people = Person1.query.all()

    result = []
    for person in people:
        data = {}
        data['id'] = person.id  # == data { "id": person.id, ...}
        data['name'] = person.name
        data['email'] = person.email

        result.append(data)
    return jsonify(result)


@app.route('/person', methods=['POST'])
def insert_person():
    name = request.json['name']
    email = request.json['email']
    person = Person1(name, email)

    db.session.add(person)
    db.session.commit()

    return "Pessoa inserida com sucesso"


@app.route('/person/<id>', methods=['GET'])
def get_person(id):
    person = Person1.query.get(id)

    result = {
        'id': person.id,
        'name': person.name,
        'email': person.email
    }

    return jsonify(result)


@app.route('/person', methods=['PUT'])
def update_person():
    id = request.json['id']
    person = Person1.query.get(id)
    person.name = request.json['name']
    person.email = request.json['email']

    db.session.commit()

    return "Pessoa atualizada com sucesso"

@app.route('/person/<id>', methods=['DELETE'])
def delete_person(id):
    person = Person1.query.get(id)
    db.session.delete(person)
    db.session.commit()

    return f"Pessoa {person.name} deletada com sucesso"


#===========================================================#
#---------------Rotas além do Crud--------------------------#

@app.route('/divida/person/<id>', methods=['GET'])
def divida_by_user(id):
    dividas = Divida1.query.filter(Divida1.person_id == id).all()
    person = Person1.query.get(id)
    data = []

    for divida in dividas:
        deb = {
            "id": divida.id,
            "name": divida.name,
            "price": divida.price,
            "data_vencimento": divida.data_vencimento,
            "is_pago": divida.is_pago
        }
        data.append(deb)

    result = [{
        'id': person.id,
        'name': person.name,
        'email': person.email,
        'dividas': data
    }]
    return jsonify(result)


@app.route('/divida/pagar/<id>', methods=['PATCH'])
def pagar(id):
    divida = Divida1.query.get(id)
    divida.is_pago = True
    db.session.commit()
    return f"Divida da {divida.name} no valor de {divida.price} paga com sucesso!"


@app.route('/dividas/pagas', methods=['GET'])
def pagas():
    dividas = Divida1.query.filter(Divida1.is_pago == True).all()
    result = []
    for divida in dividas:
        data = {
            "id": divida.id,
            "name": divida.name,
            "price": divida.price,
            "data_vencimento": divida.data_vencimento,
            "is_pago": divida.is_pago
        }
        result.append(data)
    return jsonify(result)
