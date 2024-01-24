#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import Zookeeper, Enclosure, Animal

from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = f'''
            <h1>ID: {animal.id}</h1>
            <h1>Name: {animal.name}</h1>
            <h1>Species: {animal.species}</h1>
            <h1>Zookeeper: {animal.caretaker.name if animal.caretaker else None}</h1>
            <h1>Enclosure: {animal.habitat.environment if animal.habitat else None}</h1>
        '''
        return make_response(response_body, 200)
    else:
        response_body = '<h1>Error : Animal not found</h1>'
        response = make_response(response_body, 404)
        return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        response_body = f'''
            <h1>ID: {zookeeper.id}</h1>
            <h1>name: {zookeeper.name}</h1>
            <h1>birthday: {zookeeper.birthday}</h1>
            <h1>animals: {[animal.name for animal in zookeeper.animals]}</h1>
        '''
        return make_response(response_body, 200)
    else:
        response_body = '<h1>Error: Zookeeper not found</h1>'
        response = make_response(response_body, 404)
        return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        response_body = f'''
            <h1>ID: {enclosure.id}</h1>
            <h1>environment: {enclosure.environment}</h1>
            <h1>open_to_visitors: {enclosure.open_to_visitors}</h1>
            <h1>animals: {[animal.name for animal in enclosure.animals]}</h1>
        '''
        return make_response(response_body, 200)
    else:
        response_body = '<h1>Error: Enclosure not found</h1>'
        response = make_response(response_body, 404)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
