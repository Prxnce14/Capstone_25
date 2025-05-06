# Add any model classes for Flask-SQLAlchemy here

# model for Posts
from . import db
import pytz
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import UniqueConstraint


class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())

    # Add named constraints
    __table_args__ = (
        UniqueConstraint('username', name='uq_users_username'),
       
    )


    def __init__(self, uname, pword, fname, lname, em, phone, user_type='gen_user'):
        self.username = uname
        self.password = generate_password_hash(pword, method='pbkdf2:sha256')
        self.firstname = fname
        self.lastname = lname
        self.email = em
        self.phone_number = phone
        self.user_type = user_type
        self.created_on = datetime.now(pytz.timezone('US/Eastern'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def get_username(self):
        return self.username
        
    def __repr__(self):
        return '<User %r>' % self.username
    

    
class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())


    # Add named constraints
    __table_args__ = (
        UniqueConstraint('username', name='uq_driver_username'),
       
    )


    def __init__(self, uname, pword, fname, lname, em, phone, user_type='driver'):
        self.username = uname
        self.password = generate_password_hash(pword, method='pbkdf2:sha256')
        self.firstname = fname
        self.lastname = lname
        self.email = em
        self.phone_number = phone
        self.user_type = user_type
        self.created_on = datetime.now(pytz.timezone('US/Eastern'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def get_username(self):
        return self.username
        
    def __repr__(self):
        return '<Driver %r>' % self.username
    


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key = True)
    user_type = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password= db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    store_name = db.Column(db.String(255))
    store_address = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())
     
     # Add named constraints
    __table_args__ = (
        UniqueConstraint('username', name='uq_restaurant_username'),
        UniqueConstraint('store_name', 'store_address', name='uq_resturant_name_address'),
     )

    def __init__(self, uname, pword, fname, lname, em, phone, store_name, store_addr, user_type='restaurant'):
        self.username = uname
        self.password = generate_password_hash(pword, method='pbkdf2:sha256')
        self.firstname = fname
        self.lastname = lname
        self.email = em
        self.phone_number = phone
        self.store_name = store_name
        self.store_address = store_addr
        self.user_type = user_type
        self.created_on = datetime.now(pytz.timezone('US/Eastern'))

    def is_authenticated(self): 
        return True
     
    def is_active(self):
        return True
     
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
        
    def get_username(self):
        return self.username
        
    def __repr__(self):
        return '<Restaurant %r>' % self.store_name
    