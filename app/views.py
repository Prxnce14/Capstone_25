import os
import logging
from logging.handlers import RotatingFileHandler
from app import app, db, login_manager, log_security_event
from flask import render_template, request, redirect, url_for, make_response, jsonify, flash, session
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UsersForm, DriverForm, RestaurantForm, LoginForm
from app.models import Users
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token




###
# Routing for our application.
###

# @app.route('/vue/')
# def vue_app():
#     return render_template('index.html')

@app.route('/')
def home():
    """Renders the default home page."""
    # return render_template('home.html')
    return jsonify(message="Welcome to Pelican Eats!")


@app.route('/api/gen/register', methods=['POST'])
def register():
    """Renders the general user registration page."""
    if request.method =='POST':
        try:
            userform = UsersForm()
            if userform.validate_on_submit():

                print("ready to process the form")
                uname = userform.username.data
                pword = userform.password.data
                fname = userform.firstname.data
                lname = userform.lastname.data
                email = userform.email.data
                phone = userform.phone_number.data        
                new_user = Users(uname, pword, fname, lname, email, phone, user_type='gen_user')
                # Check if the username already exists
                existing_user = Users.query.filter_by(username=uname).first()
                if existing_user:
                    return jsonify({"error": "Username already exists"}), 400

                db.session.add(new_user)
                db.session.commit()

                # Log registration event
                log_security_event(
                    app.security_logger, 
                    request, 
                    'registration_success', 
                    user_id=new_user.get_id(), 
                    username=uname,
                    message="User successfully registered"
                )

                return jsonify({
                    "message": "User Successfully added",
                    "username": uname,
                })
            

            else:
                errors = form_errors(userform)
                return jsonify({'errors': errors})

        except Exception as e:
             # Handle any exceptions here
            return jsonify({'error': str(e)}), 500  # Return JSON response for error
    


@app.route('/api/login', methods=['POST'])
def login():
    """Renders the website's login page."""
    
    if request.method == 'POST':
        try:
            log_form = LoginForm()
            if log_form.validate_on_submit():

                print("ready to process the login form")

                uname = log_form.username.data
                password = log_form.password.data
                

                # Using your model, query database for a user based on the username
                # and password submitted. Remember you need to compare the password hash.
                # Then store the result of that query to a `user` variable so it can be
                # passed to the login_user() method below. the 2nd usrername holds the value from the form

                # Log login attempt
                log_security_event(
                    app.security_logger, 
                    request, 
                    'login_attempt', 
                    username=uname,
                    message="Login attempt initiated"
                )

                
                # Query the database for the user
                user = Users.query.filter_by(username=uname).first()
                
                if user is not None and check_password_hash(user.password, password):

                    # If the user is not blank, meaning if a user was actually found,
                    # then login the user and create the user session.
                    # user should be an instance of your `Users class
                    # Gets user id, load into session
                    # login_user(user)
                    print("user found")
                    login_user(user)
                    
                    # Log successful login
                    log_security_event(
                        app.security_logger, 
                        request, 
                        'login_success', 
                        user_id=user.get_id(), 
                        username=user.get_username(),
                        message=f"User successfully logged in"
                    )

                    # Generate expiration time
                    timestamp = datetime.utcnow()
                    exp = timestamp + timedelta(hours=24)
                    
                    # Create payload
                    payload = {
                        "id": user.get_id(),
                        "name": user.get_username(),
                        "user_type": user.user_type,
                        "exp": exp
                    }

                    # Generate JWT token
                    access_token= create_access_token(identity=user.get_id(), additional_claims=payload)

                    response ={
                        'message': f'{user.get_username()} Successfully logged in' ,
                        'id': user.get_id() ,
                        'user_type': user.user_type,
                        'access_token': access_token,
                        'redirect': get_redirect_url(user.user_type)
                    }

                    # Return the token to the client
                    return  jsonify(response), 200
                
                else:
                    # If the user was not found, then return an error message.
                    log_security_event(
                        app.security_logger, 
                        request, 
                        'login_failure', 
                        username=uname,
                        message=f"Invalid username or password",
                        level=logging.WARNING
                    )
                    return jsonify({"error": "Invalid username or password"}), 401
            
            else:
                errors = form_errors(log_form)

                # Log form valdation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'login_form_validation_failed', 
                    message=str(errors), 
                    level=logging.WARNING
                )
                return jsonify({'errors': errors})
            
        except Exception as e:
            # Handle any exceptions here

            #Log the exception
            log_security_event(
                app.security_logger, 
                request, 
                'login_error', 
                username=uname if 'uname' in locals() else None,
                message=f"Error during login: {str(e)}",
                level=logging.ERROR
            )
            return jsonify({'error': str(e)}), 500  # Return JSON response for error




def get_redirect_url(user_type):
    """Return the appropriate redirect URL based on user type"""
    if user_type == 'gen_user':
        return 'gen/dashboard'
    elif user_type == 'driver':
        return '/driver/dashboard'
    elif user_type == 'restaurant':
        return '/restaurant/dashboard'



@app.route('/api/map-config', methods=['GET'])
def get_map_config():
    """Return map configuration including API key and map ID."""
    myapi_key = os.environ.get('API_KEY')
    mymap_id = os.environ.get('MAP_ID')
    
    response = jsonify({
        'api_key': myapi_key,
        'map_id': mymap_id
    })
    
    # Set cache control headers
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response
    


#endpoint for csrf token

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/api/preferences', methods=['POST'])
def save_preferences():
    """save user preferences from the quiz"""
    try:
        data = request.json
        user_id = data.get('userName', str(datetime.now().timestamp()))  # Generate ID if not provided
        
        # Validate input data
        required_fields = ['foodType', 'dietaryRestrictions', 'spiceLevels', 'budget', 'orderTimes']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Store preferences
        PREFERENCES_DB[user_id] = {
            'foodType': data['foodType'],
            'dietaryRestrictions': data['dietaryRestrictions'],
            'spiceLevels': data['spiceLevels'],
            'budget': data['budget'],
            'orderTimes': data['orderTimes'],
            'created_at': datetime.now().isoformat()
        }
        
        # Generate initial recommendations based on preferences
        recommendations = generate_recommendations(user_id)
        
        return jsonify({
            'success': True,
            'userId': user_id,
            'message': 'Preferences saved successfully',
            'initialRecommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preferences/<user_id>', methods=['GET'])
def get_preferences(user_id):
    """Get user preferences by user ID"""
    if user_id not in PREFERENCES_DB:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(PREFERENCES_DB[user_id])


def generate_recommendations(user_id):
    """
    Generate food recommendations based on user preferences and popularity
    using content-based filtering
    """
    if user_id not in PREFERENCES_DB:
        return []
    
    user_prefs = PREFERENCES_DB[user_id]
    
    # Extract dietary restrictions that are high priority
    high_priority_restrictions = [
        r['name'].lower() for r in user_prefs['dietaryRestrictions'] 
        if r['priority']
    ]
    
    # Extract all dietary restrictions
    all_restrictions = [
        r['name'].lower() for r in user_prefs['dietaryRestrictions']
    ]
    
    # Get user's flavor preferences
    spice_preference = user_prefs['spiceLevels']['spiceLevel']
    healthy_preference = user_prefs['spiceLevels']['healthyLevel']
    budgetOptions = user_prefs['budget']
    
    # Score each food item based on user preferences
    scored_items = []
    for item in FOOD_DB['items']:
        # Skip items that violate high priority restrictions
        if high_priority_restrictions:
            # Check if any required dietary tag is missing
            required_tags = []
            if 'vegetarian' in high_priority_restrictions:
                required_tags.append('vegetarian')
            if 'vegan' in high_priority_restrictions:
                required_tags.append('vegan')
            if 'gluten-free' in high_priority_restrictions:
                required_tags.append('gluten-free')
            
            # If any required tag is missing, skip this item
            if any(tag not in item['dietary_tags'] for tag in required_tags):
                continue
        
        # Calculate match score
        score = 0
        
        # Popularity factor (0-100)
        score += item['popularity'] * 0.3
        
        # Spice level match (0-5)
        spice_match = 5 - abs(item['spice_level'] - spice_preference)
        score += spice_match * 10
        
        # Healthy level match (0-5)
        health_match = 5 - abs(item['healthy_level'] - healthy_preference)
        score += health_match * 10
        
        # Budget match
        if item['price_category'] == budgetOptions:
            score += 20
        
        # Boost score for liked cuisines (if we had that data)
        # This would come from the swipe data potentially
        if item['name'] in user_prefs['foodType']:
            score += 50
        
        scored_items.append({
            'id': item['id'],
            'name': item['name'],
            'cuisine': item['cuisine'],
            'score': score,
            'price_category': item['price_category'],
            'dietary_tags': item['dietary_tags']
        })
    
    # Sort by score and return top recommendations
    recommendations = sorted(scored_items, key=lambda x: x['score'], reverse=True)
    return recommendations[:10]

if __name__ == '__main__':
    # For development - would use a proper WSGI server in production
    app.run(debug=True, port=5000)