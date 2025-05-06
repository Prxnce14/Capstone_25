
# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField, HiddenField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, length


#This is the name that will bbe displayed above your input fields

# Base registration form for all users
class BaseRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Mobile Number', validators=[InputRequired(), length(min=7, max=15)]) 


# Registration Form - General user


class UsersForm(BaseRegistrationForm):
    user_type = HiddenField(default='gen_user')
    


#Registration Form - Driver

class DriverForm(BaseRegistrationForm):
    user_type = HiddenField(default='driver')
    
    


#Registration Form - Restaurant
class RestaurantForm(FlaskForm):
    user_type = HiddenField(default='restaurant')
    restaurant_name = StringField('Restaurant Name ', validators=[InputRequired()])
    branch_name = StringField('Branch Name ', validators=[InputRequired()])
    password = PasswordField('Password ', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Mobile Number', validators=[InputRequired(), length(min=7, max=15)])


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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')  # Optional: remember user session


class MapForm(FlaskForm):
    cur_location = StringField('Current Location', validators=[InputRequired()])
    dest_location = StringField('Destination Location', validators=[InputRequired()])




