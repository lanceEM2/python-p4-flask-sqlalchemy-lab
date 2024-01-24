#!/usr/bin/env python3

from random import choice as rc

from faker import Faker

from database import db
from app import app
from models import Zookeeper, Animal, Enclosure

fake = Faker()

with app.app_context():

    Animal.query.delete()
    Zookeeper.query.delete()
    Enclosure.query.delete()

    zookeepers = []
    for n in range(25):
        zk = Zookeeper(name=fake.name(), birthday=fake.date_between(
            start_date='-70y', end_date='-18y'))
        zookeepers.append(zk)

    db.session.add_all(zookeepers)
    db.session.commit()  # Commit zookeepers to the database to get their IDs

    enclosures = []
    environments = ['Desert', 'Pond', 'Ocean', 'Field', 'Trees', 'Cave', 'Cage']

    for n in range(25):
        e = Enclosure(environment=rc(environments), open_to_visitors=rc([True, False]))
        enclosures.append(e)

    db.session.add_all(enclosures)
    db.session.commit()  # Commit enclosures to the database to get their IDs

    animals = []
    species = ['Lion', 'Tiger', 'Bear', 'Hippo', 'Rhino', 'Elephant', 'Ostrich',
        'Snake', 'Monkey']

    for n in range(200):
        name = fake.first_name()
        while name in [a.name for a in animals]:
            name=fake.first_name()
            
        # Get random zookeeper and enclosure objects from the database
        random_zookeeper = rc(zookeepers)
        random_enclosure = rc(enclosures)

        # Create Animal with the obtained zookeeper and enclosure objects
        a = Animal(name=name, species=rc(species), caretaker=random_zookeeper, habitat=random_enclosure)
        animals.append(a)

    db.session.add_all(animals)
    db.session.commit()

