from model.person import Person1
from app import app, db
from flask import request, jsonify

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
