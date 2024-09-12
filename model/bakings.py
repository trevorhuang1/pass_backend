""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from flask import jsonify
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Peanut(db.Model):
    __tablename__ = 'bakings'  # table name is plural, class name is singular
    # Define the User schema with "vars" from object
    
    id = db.Column(db.Integer, primary_key=True)
    _popularity = db.Column(db.Integer, unique = False, nullable = False)
    _name = db.Column(db.String(255), unique = True, nullable = False)
    

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, popularity=0, name = ""):   # variables with self prefix become part of the object, 
        self._popularity = popularity
        self._name = name

    @property
    def popularity(self):
        return self._popularity
    
    # a setter function, allows name to be updated after initial object creation
    @popularity.setter
    def popularity(self, popularity):
        self._popularity = popularity
    
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name

    # @property
    # def points(self):
    #     return self._points
    
    # # a setter function, allows name to be updated after initial object creation
    # @points.setter
    # def points(self, points):
    #     self._points = points
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "popularity": self.popularity,
            "name": self.name
        }

    # # CRUD update: updates user name, password, phone
    # # returns self
    # def update(self, name="", uid="", password="", dob='', favoritefood=''):
    #     """only updates values with length"""
    #     if len(name) > 0:
    #         self.name = name
    #     if len(uid) > 0:
    #         self.uid = uid
    #     if len(password) > 0:
    #         self.set_password(password)
    #     if dob:
    #         self.dob = dob
    #     if len(favoritefood) > 0:
    #         self.favoritefood = favoritefood
    #     db.session.commit()
    #     return self

    # CRUD delete: remove self
    # None
    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()
    #     return None


"""Database Creation and Testing """


# Builds working data for testing
def initPeanut():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        peanut1 = Peanut(5,'Smuckers Organic Creamy Peanut Butter')
        peanut2 = Peanut(4,'Wild Friends Food')
        peanut3 = Peanut(3,'Organic Unsweetened and No Salt')
        peanut4 = Peanut(2, 'Fix and Fogg')
        peanut5 = Peanut(1,'Field Day Organic and Unsalted Peanut Butter')
        peanut_brands = [peanut1,peanut2,peanut3,peanut4,peanut5]
        for peanut in peanut_brands:    
            peanut.create()