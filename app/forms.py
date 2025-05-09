
# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField, HiddenField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, length, NumberRange, Optional, URL





#This is the name that will bbe displayed above your input fields


# Registration Form - General user


class UsersForm(FlaskForm):
    user_type = HiddenField(default='gen_user')
    username = StringField('Username ', validators=[InputRequired()])
    password = PasswordField('Password ', validators=[InputRequired()])
    firstname = StringField('First Name ', validators=[InputRequired()])
    lastname = StringField('Last Name ', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Mobile Number', validators=[InputRequired(), length(min=7, max=15)])


#Registration Form - Driver

class DriverForm(FlaskForm):
    user_type = HiddenField(default='driver')
    username = StringField('Username ', validators=[InputRequired()])
    password = PasswordField('Password ', validators=[InputRequired()])
    firstname = StringField('First Name ', validators=[InputRequired()])
    lastname = StringField('Last Name ', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Mobile Number', validators=[InputRequired(), length(min=7, max=15)])
    


#Registration Form - Restaurant
class RestaurantForm(FlaskForm):
    user_type = HiddenField(default='restaurant')
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password ', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Mobile Number', validators=[InputRequired(), length(min=7, max=15)])
    store_name = StringField('Restaurant Name ', validators=[InputRequired()])
    store_address = StringField('Restaurant Address ', validators=[InputRequired()])

class RestaurantProduct(FlaskForm):
    name = StringField('Product Name', validators=[InputRequired(), length(min=2, max=100)])
    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0.01)])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    
    # File upload alternative for image
    image_file = FileField('Upload Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
    ])
    
    description = TextAreaField('Description', validators=[Optional(), length(max=500)])
    category = SelectField('Category', validators=[InputRequired()], 
                          choices=[
                              ('appetizer', 'Appetizer'),
                              ('main_course', 'Main Course'),
                              ('dessert', 'Dessert'),
                              ('beverage', 'Beverage'),
                              ('side', 'Side Dish'),
                              ('special', 'Daily Special')
                          ])
    
    is_vegetarian = BooleanField('Vegetarian')
    is_vegan = BooleanField('Vegan')
    is_gluten_free = BooleanField('Gluten Free')
    
    # For special deals or featured items
    is_featured = BooleanField('Feature on Homepage')
    discount_percentage = FloatField('Discount (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    
    # For inventory management
    minimum_stock = IntegerField('Minimum Stock Alert', validators=[Optional(), NumberRange(min=0)])

    
#these are the fields for when the user is logged in and wants to update their profile
# class UpdateuserForm(FlaskForm):
# address = TextAreaField('Address', validators=[InputRequired()])
# city = StringField('City', validators=[InputRequired()])
# zip_code = StringField('Zip Code', validators=[InputRequired()])

#these are the fields for when the user is logged in and wants to update their profile
# class UpdaterestaurantForm(FlaskForm):
# address = TextAreaField('Address', validators=[InputRequired()])
# city = StringField('City', validators=[InputRequired()])
# zip_code = StringField('Zip Code', validators=[InputRequired()])

#these are the fields for when the user is logged in and wants to update their profile
# class UpdateuserForm(FlaskForm):
# address = TextAreaField('Address', validators=[InputRequired()])
# city = StringField('City', validators=[InputRequired()])
# zip_code = StringField('Zip Code', validators=[InputRequired()])



#Login form - Differentiate based on user type
# This form will be used for all users General, drivers and restaurant owners.


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired()])
#     password = PasswordField('Password', validators=[InputRequired()])
   





