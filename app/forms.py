
# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, PasswordField, HiddenField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Email, DataRequired, length, NumberRange, Optional, URL



from wtforms import StringField, TextAreaField, SelectField, PasswordField, HiddenField, BooleanField, IntegerField, FieldList, FormField
from wtforms.validators import InputRequired, Email, DataRequired, length, Optional, NumberRange, Length


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
    display_name = StringField('Public Display Name', validators=[InputRequired()])
    password = PasswordField('Password ', validators=[InputRequired()])
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


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')  # Optional: remember user session


class MapForm(FlaskForm):
    cur_location = StringField('Current Location', validators=[InputRequired()])
    dest_location = StringField('Destination Location', validators=[InputRequired()])





# Preference form for general users to select their preferences during onboarding
####################################################################################################################################################


# Base food preference forms
class FoodTypeForm(FlaskForm):
    name = StringField('Food Name', validators=[InputRequired()])
    liked = BooleanField('Liked', default=False)


class DietaryRestrictionForm(FlaskForm):
    name = StringField('Restriction Name', validators=[InputRequired()])
    selected = BooleanField('Selected', default=False)
    priority = BooleanField('Priority', default=False)


class OrderTimeForm(FlaskForm):
    name = StringField('Time Name', validators=[InputRequired()])
    selected = BooleanField('Selected', default=False)


# Specialized food preference forms with improved structure
class FlavorPreferencesForm(FlaskForm):
    spice_level = IntegerField('Spice Level',
                              validators=[InputRequired(), NumberRange(min=1, max=5)],
                              default=3)
    healthy_level = IntegerField('Healthy Level',
                                validators=[InputRequired(), NumberRange(min=1, max=5)],
                                default=3)
    sweet_preference = IntegerField('Sweet Level',
                                   validators=[Optional(), NumberRange(min=1, max=5)],
                                   default=3)


class MeatPreferencesForm(FlaskForm):
    chicken = BooleanField('Chicken', default=False)
    fish = BooleanField('Fish', default=False)
    pork = BooleanField('Pork', default=False)
    goat = BooleanField('Goat', default=False)
    beef = BooleanField('Beef', default=False)
    no_meat = BooleanField("Don't eat meat", default=False)
    other_meat = StringField('Other meat', validators=[Optional(), Length(max=100)])


class CookingStylesForm(FlaskForm):
    jamaican = BooleanField('Jamaican', default=False)
    indian = BooleanField('Indian', default=False)
    chinese = BooleanField('Chinese', default=False)
    african = BooleanField('African', default=False)
    vegan_ital = BooleanField('Vegan/Ital/Rastafarian', default=False)
    italian = BooleanField('Italian', default=False)
    other_style = StringField('Other cooking style', validators=[Optional(), Length(max=100)])


# Popular Jamaican breakfast items

class PopularBreakfastItemsForm(FlaskForm):
    ackee_saltfish = BooleanField('Ackee & Saltfish', default=False)
    callaloo = BooleanField('Callaloo', default=False)
    cooked_saltfish = BooleanField('Cooked-up Saltfish', default=False)
    kidney = BooleanField('Kidney', default=False)
    liver = BooleanField('Liver', default=False)
    fried_plantain = BooleanField('Fried Plantain', default=False)
    dumplings = BooleanField('Dumplings', default=False)
    festival = BooleanField('Festival', default=False)
    breadfruit = BooleanField('Breadfruit', default=False)
    other_breakfast_items = StringField('Other breakfast items', validators=[Optional(), Length(max=200)])


class BreakfastItemsForm(FlaskForm):
    # Hot breakfast items
    porridge = BooleanField('Porridge', default=False)
    scrambled_eggs = BooleanField('Scrambled Eggs', default=False)
    
    # Sweet breakfast items
    pancakes = BooleanField('Pancakes', default=False)
    french_toast = BooleanField('French Toast', default=False)
    waffles = BooleanField('Waffles', default=False)
    
    # Protein items
    bacon = BooleanField('Bacon', default=False)
    sausage = BooleanField('Sausage', default=False)
    
    # Other items
    sandwich = BooleanField('Sandwich', default=False)
    
    other_breakfast = StringField('Other breakfast items', validators=[Optional(), Length(max=200)])


# Meal time preference forms
class LunchPreferencesForm(FlaskForm):
    fry_chicken = BooleanField('Fried Chicken', default=False)
    bake_chicken = BooleanField('Sandwiches', default=False)
    curry_goat = BooleanField('Curry Goat', default=False)
    soups = BooleanField('Soups', default=False)
    steamed_fish = BooleanField('Steamed Fish', default=False)
    escovitch_fish = BooleanField('Escovitch Fish', default=False)
    patty = BooleanField('Patty', default=False)
    sandwiches = BooleanField('Sandwiches', default=False)
    pasta = BooleanField('Pasta', default=False)
    other_lunch = StringField('Other lunch preferences', validators=[Optional(), Length(max=200)])

# Juice preferences
class JuicePreferencesForm(FlaskForm):
    pine_ginger = BooleanField('Pine & Ginger Juice ', default=False)
    callallo = BooleanField('Callaloo Juice', default=False)
    june_plum = BooleanField('June Plum Juice', default=False)
    guava_pine = BooleanField('Guava-Pineapple Juice', default=False)
    beet_root = BooleanField('Beet Root Juice', default=False)
    orange = BooleanField('Orange Juice', default=False)
    other_juice = StringField('Other juice preferences', validators=[Optional(), Length(max=200)])



# Comprehensive Food Preferences Form
class FoodPreferencesForm(FlaskForm):
    # General food types (using existing structure)
    liked_foods = FieldList(FormField(FoodTypeForm), min_entries=0)
    
    # Dietary restrictions
    dietary_restrictions = FieldList(FormField(DietaryRestrictionForm), min_entries=0)
    
    # Flavor preferences
    flavor_preferences = FormField(FlavorPreferencesForm)
    
    # Specialized preferences
    meat_preferences = FormField(MeatPreferencesForm)
    cooking_styles = FormField(CookingStylesForm)
    
    # Meal-specific preferences
    breakfast_preferences = FormField(BreakfastItemsForm)
    lunch_preferences = FormField(LunchPreferencesForm)
    juice_preferences = FormField(JuicePreferencesForm)
    popular_preferences = FieldList(FormField(PopularBreakfastItemsForm), min_entries=0)
    
    # budget
    budget = SelectField('Budget Preference',
                        choices=[('low', '$ - Budget-friendly'),
                                ('medium', '$$ - Moderate'),
                                ('high', '$$$ - Premium')],
                        validators=[InputRequired()],
                        default='medium')
    
    # Order times
    order_times = FieldList(FormField(OrderTimeForm), min_entries=0)
    
    # Additional preferences
    additional_notes = StringField('Additional Food Preferences/Allergies',
                                  validators=[Optional(), Length(max=500)])


# Helper form for creating custom food preference sections
class CustomFoodPreferenceForm(FlaskForm):
    category_name = StringField('Preference Category', validators=[InputRequired()])
    preferences = FieldList(StringField('Preference Item'), min_entries=1)


# Existing forms (unchanged)
class DeliveryPreferencesForm(FlaskForm):
    default_address = StringField('Default Delivery Address', validators=[InputRequired()])
    delivery_instructions = StringField('Special Delivery Instructions', validators=[Optional()])
    preferred_delivery_time = SelectField('Preferred Delivery Time',
                                        choices=[
                                            ('morning', 'Morning (9 AM - 12 PM)'),
                                            ('afternoon', 'Afternoon (12 PM - 5 PM)'),
                                            ('evening', 'Evening (5 PM - 9 PM)')
                                        ],
                                        validators=[InputRequired()],
                                        default='evening')


class CommunicationPreferencesForm(FlaskForm):
    email_notifications = BooleanField('Email Notifications', default=True)
    sms_notifications = BooleanField('SMS Notifications', default=False)
    promotional_emails = BooleanField('Promotional Emails', default=False)


# Enhanced onboarding form
class OnboardingForm(FlaskForm):
    # Food preferences (now comprehensive)
    food_preferences = FormField(FoodPreferencesForm)
    
    # Delivery preferences
    delivery_preferences = FormField(DeliveryPreferencesForm)
    
    # Communication preferences
    communication_preferences = FormField(CommunicationPreferencesForm)
