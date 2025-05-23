# Add any model classes for Flask-SQLAlchemy here

# model for Posts
from . import db
import pytz
from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin



class Users(db.Model, UserMixin):

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
    

    
class Driver(db.Model, UserMixin):
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
    


class Restaurant(db.Model, UserMixin):
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
    
    

# model for User Preferences
######################################################################################################################################

class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Food Types (stored as JSON for flexibility)
    liked_foods = db.Column(db.JSON, default=list)  # [{"name": "", "liked": bool}, ...]
    
    # Dietary Restrictions
    dietary_restrictions = db.Column(db.JSON, default=list)  # [{"name": "", "selected": bool, "priority": bool}, ...]
    
    # Flavor Preferences
    spice_level = db.Column(db.Integer, default=3, nullable=False)
    healthy_level = db.Column(db.Integer, default=3, nullable=False)
    sweet_preference = db.Column(db.Integer, default=3)
    
    # Meat Preferences
    chicken = db.Column(db.Boolean, default=False)
    fish = db.Column(db.Boolean, default=False)
    pork = db.Column(db.Boolean, default=False)
    goat = db.Column(db.Boolean, default=False)
    beef = db.Column(db.Boolean, default=False)
    no_meat = db.Column(db.Boolean, default=False)
    other_meat = db.Column(db.String(100))
    
    # Cooking Styles
    cooking_jamaican = db.Column(db.Boolean, default=False)
    cooking_indian = db.Column(db.Boolean, default=False)
    cooking_chinese = db.Column(db.Boolean, default=False)
    cooking_african = db.Column(db.Boolean, default=False)
    cooking_vegan_ital = db.Column(db.Boolean, default=False)
    cooking_italian = db.Column(db.Boolean, default=False)
    other_cooking_style = db.Column(db.String(100))
    
    # Popular Jamaican Breakfast Items
    ackee_saltfish = db.Column(db.Boolean, default=False)
    callaloo = db.Column(db.Boolean, default=False)
    cooked_saltfish = db.Column(db.Boolean, default=False)
    kidney = db.Column(db.Boolean, default=False)
    liver = db.Column(db.Boolean, default=False)
    fried_plantain = db.Column(db.Boolean, default=False)
    dumplings = db.Column(db.Boolean, default=False)
    festival = db.Column(db.Boolean, default=False)
    breadfruit = db.Column(db.Boolean, default=False)
    other_breakfast_items = db.Column(db.String(200))
    
    # Breakfast Items
    porridge = db.Column(db.Boolean, default=False)
    scrambled_eggs = db.Column(db.Boolean, default=False)
    pancakes = db.Column(db.Boolean, default=False)
    french_toast = db.Column(db.Boolean, default=False)
    waffles = db.Column(db.Boolean, default=False)
    bacon = db.Column(db.Boolean, default=False)
    sausage = db.Column(db.Boolean, default=False)
    sandwich = db.Column(db.Boolean, default=False)
    other_breakfast = db.Column(db.String(200))
    
    # Lunch Preferences
    fry_chicken = db.Column(db.Boolean, default=False)
    bake_chicken = db.Column(db.Boolean, default=False)
    curry_goat = db.Column(db.Boolean, default=False)
    soups = db.Column(db.Boolean, default=False)
    steamed_fish = db.Column(db.Boolean, default=False)
    escovitch_fish = db.Column(db.Boolean, default=False)
    patty = db.Column(db.Boolean, default=False)
    sandwiches = db.Column(db.Boolean, default=False)
    pasta = db.Column(db.Boolean, default=False)
    other_lunch = db.Column(db.String(200))
    
    # Juice Preferences
    pine_ginger = db.Column(db.Boolean, default=False)
    callallo_juice = db.Column(db.Boolean, default=False)
    june_plum = db.Column(db.Boolean, default=False)
    guava_pine = db.Column(db.Boolean, default=False)
    beet_root = db.Column(db.Boolean, default=False)
    orange_juice = db.Column(db.Boolean, default=False)
    other_juice = db.Column(db.String(200))
    
    # Budget Preference
    budget = db.Column(db.String(10), default='medium', nullable=False)
    
    # Order Times (stored as JSON)
    order_times = db.Column(db.JSON, default=list)  # [{"name": "", "selected": bool}, ...]
    
    # Additional Notes
    additional_notes = db.Column(db.String(500))
    
    # Delivery Preferences
    default_address = db.Column(db.String(255), nullable=False)
    delivery_instructions = db.Column(db.String(255))
    preferred_delivery_time = db.Column(db.String(20), default='evening', nullable=False)
    
    # Communication Preferences
    email_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    promotional_emails = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_on = db.Column(db.DateTime())
    updated_on = db.Column(db.DateTime())
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('spice_level >= 1 AND spice_level <= 5', name='spice_level_range'),
        db.CheckConstraint('healthy_level >= 1 AND healthy_level <= 5', name='healthy_level_range'),
        db.CheckConstraint('sweet_preference >= 1 AND sweet_preference <= 5', name='sweet_preference_range'),
        db.CheckConstraint("budget IN ('low', 'medium', 'high')", name='budget_choices'),
        db.CheckConstraint("preferred_delivery_time IN ('morning', 'afternoon', 'evening')", name='delivery_time_choices'),
    )
    
    def __init__(self, user_id, **kwargs):
        self.user_id = user_id
        
        # Set defaults for complex fields
        self.liked_foods = kwargs.get('liked_foods', [])
        self.dietary_restrictions = kwargs.get('dietary_restrictions', [])
        self.order_times = kwargs.get('order_times', [])
        
        # Set defaults for numeric fields
        self.spice_level = kwargs.get('spice_level', 3)
        self.healthy_level = kwargs.get('healthy_level', 3)
        self.sweet_preference = kwargs.get('sweet_preference', 3)
        
        # Set defaults for string fields
        self.budget = kwargs.get('budget', 'medium')
        self.preferred_delivery_time = kwargs.get('preferred_delivery_time', 'evening')
        
        # Set all other fields from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Set metadata
        self.created_on = datetime.now(pytz.timezone('US/Eastern'))
        self.updated_on = self.created_on
    
    def update_preferences(self, **kwargs):
        """Update user preferences with new values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_on = datetime.now(pytz.timezone('US/Eastern'))
    
    def get_preferred_foods(self):
        """Get all liked foods"""
        return [food['name'] for food in self.liked_foods if food.get('liked', False)]
    
    def get_active_restrictions(self):
        """Get all active dietary restrictions"""
        return [rest['name'] for rest in self.dietary_restrictions if rest.get('selected', False)]
    
    def get_priority_restrictions(self):
        """Get priority dietary restrictions"""
        return [rest['name'] for rest in self.dietary_restrictions if rest.get('priority', False)]
    
    def get_preferred_order_times(self):
        """Get selected order times"""
        return [time['name'] for time in self.order_times if time.get('selected', False)]
    
    def is_vegetarian(self):
        """Check if user preferences indicate vegetarian diet"""
        return self.no_meat or 'vegetarian' in self.get_active_restrictions()
    
    def is_vegan(self):
        """Check if user preferences indicate vegan diet"""
        return 'vegan' in self.get_active_restrictions()
    
    def to_dict(self):
        """Convert preferences to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'liked_foods': self.liked_foods,
            'dietary_restrictions': self.dietary_restrictions,
            'flavor_preferences': {
                'spice_level': self.spice_level,
                'healthy_level': self.healthy_level,
                'sweet_preference': self.sweet_preference
            },
            'meat_preferences': {
                'chicken': self.chicken,
                'fish': self.fish,
                'pork': self.pork,
                'goat': self.goat,
                'beef': self.beef,
                'no_meat': self.no_meat,
                'other_meat': self.other_meat
            },
            'cooking_styles': {
                'jamaican': self.cooking_jamaican,
                'indian': self.cooking_indian,
                'chinese': self.cooking_chinese,
                'african': self.cooking_african,
                'vegan_ital': self.cooking_vegan_ital,
                'italian': self.cooking_italian,
                'other': self.other_cooking_style
            },
            'breakfast_preferences': {
                'popular_jamaican': {
                    'ackee_saltfish': self.ackee_saltfish,
                    'callaloo': self.callaloo,
                    'cooked_saltfish': self.cooked_saltfish,
                    'kidney': self.kidney,
                    'liver': self.liver,
                    'fried_plantain': self.fried_plantain,
                    'dumplings': self.dumplings,
                    'festival': self.festival,
                    'breadfruit': self.breadfruit,
                    'other': self.other_breakfast_items
                },
                'general': {
                    'porridge': self.porridge,
                    'scrambled_eggs': self.scrambled_eggs,
                    'pancakes': self.pancakes,
                    'french_toast': self.french_toast,
                    'waffles': self.waffles,
                    'bacon': self.bacon,
                    'sausage': self.sausage,
                    'sandwich': self.sandwich,
                    'other': self.other_breakfast
                }
            },
            'lunch_preferences': {
                'fry_chicken': self.fry_chicken,
                'bake_chicken': self.bake_chicken,
                'curry_goat': self.curry_goat,
                'soups': self.soups,
                'steamed_fish': self.steamed_fish,
                'escovitch_fish': self.escovitch_fish,
                'patty': self.patty,
                'sandwiches': self.sandwiches,
                'pasta': self.pasta,
                'other': self.other_lunch
            },
            'juice_preferences': {
                'pine_ginger': self.pine_ginger,
                'callallo_juice': self.callallo_juice,
                'june_plum': self.june_plum,
                'guava_pine': self.guava_pine,
                'beet_root': self.beet_root,
                'orange_juice': self.orange_juice,
                'other': self.other_juice
            },
            'budget': self.budget,
            'order_times': self.order_times,
            'additional_notes': self.additional_notes,
            'delivery_preferences': {
                'default_address': self.default_address,
                'delivery_instructions': self.delivery_instructions,
                'preferred_delivery_time': self.preferred_delivery_time
            },
            'communication_preferences': {
                'email_notifications': self.email_notifications,
                'sms_notifications': self.sms_notifications,
                'promotional_emails': self.promotional_emails
            },
            'created_on': self.created_on.isoformat() if self.created_on else None,
            'updated_on': self.updated_on.isoformat() if self.updated_on else None
        }
    
    def __repr__(self):
        return f'<UserPreferences {self.user_id}>'
