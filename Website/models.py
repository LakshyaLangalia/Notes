# creates the classes which represent tables within the database

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pyodbc

class Note(db.Model):
    # Every note has a unique id, the information conatined within the note, 
    # the date at which it was taken, and the user it is associated with
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# usermixin allows compatibility for methods like get_id() which is required by flask_login
class User(db.Model, UserMixin):
    # every user has an id, email, password, first name
    # 'notes' defines a one-to-many relationship with the Note class
    # allows a user to access all note objects; not a column but a back-reference to the 
    # user id foreign key in the Note table.
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)   
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

