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
    display_name = db.Column(db.String(255))
    password= db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    store_name = db.Column(db.String(255))
    store_address = db.Column(db.String(255))
    created_on = db.Column(db.DateTime())
     
     # Add named constraints
    __table_args__ = (
        UniqueConstraint('display_name', name='uq_restaurant_displayname'),
        UniqueConstraint('store_name', 'store_address', name='uq_resturant_name_address'),
     )

    def __init__(self, dpname, pword, em, phone, store_name, store_addr, user_type='restaurant'):
        self.display_name = dpname
        self.password = generate_password_hash(pword, method='pbkdf2:sha256')
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
        return self.display_name
        
    def __repr__(self):
        return '<Restaurant %r>' % self.store_name

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    discount_percentage = db.Column(db.Float, default=0)
    minimum_stock = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "image_url": self.image_url,
            "description": self.description,
            "category": self.category,
            "is_vegetarian": self.is_vegetarian,
            "is_vegan": self.is_vegan,
            "is_gluten_free": self.is_gluten_free,
            "is_featured": self.is_featured,
            "discount_percentage": self.discount_percentage,
            "minimum_stock": self.minimum_stock
        }