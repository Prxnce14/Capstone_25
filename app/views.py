import os
import logging
from logging.handlers import RotatingFileHandler
from app import app, db, login_manager, log_security_event
from flask import render_template, request, redirect, url_for, make_response, jsonify, flash, session
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UsersForm, DriverForm, RestaurantForm, LoginForm, MapForm
from app.models import Users
from datetime import datetime, timedelta
from app.models import Users, Driver, Restaurant
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.helpers import convert_to_geojson, get_node_from_location, get_route_segment, haversine, get_nearby_intersections
from app.helpers import get_traffic_factor, current_time
from app.locations import a_star



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



#Registration route for general users
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
                    log_security_event(
                        app.security_logger, 
                        request, 
                        'registration_failure', 
                        username=uname,
                        message=f"Existing username: {uname}",
                        level=logging.WARNING
                    )

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

                # log Users form validation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'user_form_validation_failed',
                    message=str(errors), 
                    level=logging.WARNING
                )

                return jsonify({'errors': errors})

        except Exception as e:
            # Handle any exceptions here

            # Log the exception
            log_security_event(
                app.security_logger, 
                request, 
                'registration_error', 
                username=uname if 'uname' in locals() else None,
                message=f"Error during user registration: {str(e)}",
                level=logging.ERROR
            )
            return jsonify({'error': str(e)}), 500  # Return JSON response for error
    
    
@app.route('/api/driver/register', methods=['POST'])
def driver_register():
    if request.method =='POST':
        try:
            driverform = DriverForm()
            if driverform.validate_on_submit():

                print("ready to process the form")
                uname = driverform.username.data
                pword = driverform.password.data
                fname = driverform.firstname.data
                lname = driverform.lastname.data
                email = driverform.email.data
                phone = driverform.phone_number.data
                new_driver = Driver(uname, pword, fname, lname, email, phone, user_type='driver')
                # Check if the username already exists
                existing_driver = Driver.query.filter_by(username=uname).first()
                if existing_driver:
                    return jsonify({"error": "Username already exists"}),400
                
                db.session.add(new_driver)
                db.session.commit()

                # Log registration event
                log_security_event(
                    app.security_logger, 
                    request, 
                    'registration_success', 
                    user_id=new_driver.get_id(), 
                    username=uname,
                    message="Driver successfully registered"
                )

                return jsonify({
                    "message": "Driver Successfully added",
                    "username": uname,
                })
            
            else:
                errors = form_errors(driverform)

                #log driver form validation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'driver_form_validation_failed',
                    message=str(errors), 
                    level=logging.WARNING
                )
                return jsonify({'errors': errors})
        
        except Exception as e:
            #Handle any exceptions here

            # Log the exception
            log_security_event(
                app.security_logger, 
                request, 
                'registration_error', 
                username=uname if 'uname' in locals() else None,
                message=f"Error during driver registration: {str(e)}",
                level=logging.ERROR
            )
                
            return jsonify({'error': str(e)}), 500 #Return JSON response for error


@app.route('/api/restaurant/register', methods=['POST'])
def restaurant_register():
    if request.method == 'POST':
        try:
            restaurantform = RestaurantForm()
            if restaurantform.validate_on_submit():

                print("ready to process the form")
                disp_name = restaurantform.display_name.data
                pword = restaurantform.password.data
                email = restaurantform.email.data
                phone = restaurantform.phone_number.data
                store_name = restaurantform.store_name.data
                store_addr = restaurantform.store_address.data
                new_restaurant = Restaurant(disp_name, pword, email, phone, store_name, store_addr, user_type='restaurant')

                existing_restaurant = Restaurant.query.filter_by(display_name=disp_name).first()
                if existing_restaurant:
                    return jsonify({"error": "Display name already exists"}), 400
                
                existing_store = Restaurant.query.filter_by(store_name = store_name, store_address=store_addr).first()
                if existing_store:
                    return jsonify({"error": "Restauramy with this name and address already exists"}), 400
                
                db.session.add(new_restaurant)
                db.session.commit()

                # Log registration event
                log_security_event(
                    app.security_logger, 
                    request, 
                    'registration_success', 
                    user_id=new_restaurant.get_id(), 
                    username=new_restaurant.get_username(),
                    message="restaurant successfully registered"
                )

                return jsonify({
                    "message": "Restaurant Successfully added",
                    "Public name": new_restaurant.get_username(),
                    "store_name": store_name
                })
            
            else:
                errors = form_errors(restaurantform)

                # log restaurant form validation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'registration_form_validation_failed',
                    message=str(errors), 
                    level=logging.WARNING
                )
                return jsonify({'errors': errors})
        
        except Exception as e:

            #log the exception

            log_security_event(
                app.security_logger, 
                request, 
                'registration_error', 
                username=disp_name if 'disp_name' in locals() else None,
                message=f"Error during restaurant registration: {str(e)}",
                level=logging.ERROR
            )

            return jsonify({'error': str(e)}), 500
                


#Login route for all users
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
                
                # Log login attempt
                log_security_event(
                    app.security_logger, 
                    request, 
                    'login_attempt', 
                    username=uname,
                    message="Login attempt initiated"
                )
                
                # Query the database for the user across all user types
                user = Users.query.filter_by(username=uname).first()
                driver = Driver.query.filter_by(username=uname).first()
                restaurant = Restaurant.query.filter_by(display_name=uname).first()
                
                # Check if user exists in any of the tables and verify password
                if user is not None and check_password_hash(user.password, password):
                    authenticated_user = user
                elif driver is not None and check_password_hash(driver.password, password):
                    authenticated_user = driver
                elif restaurant is not None and check_password_hash(restaurant.password, password):
                    authenticated_user = restaurant
                else:
                    authenticated_user = None
                
                if authenticated_user is not None:
                    # User found and password matches
                    print(f"{authenticated_user.user_type} found")
                    login_user(authenticated_user)
                    
                    # Log successful login
                    log_security_event(
                        app.security_logger, 
                        request, 
                        'login_success', 
                        user_id=authenticated_user.get_id(), 
                        username=authenticated_user.get_username(),
                        message=f"{authenticated_user.user_type.capitalize()} successfully logged in"
                    )

                    # Generate expiration time
                    timestamp = datetime.utcnow()
                    exp = timestamp + timedelta(hours=24)
                    
                    # Create payload
                    payload = {
                        "id": authenticated_user.get_id(),
                        "name": authenticated_user.get_username(),
                        "user_type": authenticated_user.user_type,
                        "exp": exp
                    }

                    # Generate JWT token
                    access_token = create_access_token(identity=authenticated_user.get_id(), additional_claims=payload)

                    response = {
                        'message': f'{authenticated_user.get_username()} Successfully logged in',
                        'id': authenticated_user.get_id(),
                        'user_type': authenticated_user.user_type,
                        'access_token': access_token,
                        'redirect': get_redirect_url(authenticated_user.user_type)
                    }

                    # Return the token to the client
                    return jsonify(response), 200
                
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

                # Log form validation failure
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

            # Log the exception
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



# Route to rendeer the map page
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
    

# Route for the map form
@app.route('/api/map-form', methods=['POST'])
def map_form():
    """Handle the map form submission."""
    if request.method == 'POST':
        try:
            map_form = MapForm()
            if map_form.validate_on_submit():
                print("ready to process the map form")
                
                # Process the form data here
                cur_location = map_form.cur_location.data
                dest_location = map_form.dest_location.data

                # log the attempt of a trip
                log_security_event(
                    app.security_logger, 
                    request, 
                    'trip_attempt', 
                    user_id=current_user.get_id() if current_user.is_authenticated else None,
                    message=f"Trip from {cur_location} to {dest_location} initiated"
                )


                #The functionality of the route rendering can be added here
                # Convert to node format
                start_node = get_node_from_location(cur_location)
                goal_node = get_node_from_location(dest_location)
                
                # Run A* algorithm
                optimal_path = a_star(
                    start_node, 
                    goal_node, 
                    get_map_neighbors, 
                    map_based_heuristic
                )

                # Get alternative route by slightly modifying the heuristic
                alt_path = a_star(
                    start_node,
                    goal_node,
                    get_map_neighbors,
                    lambda n: map_based_heuristic(n, goal_node) * 1.2
                )


                 # Return paths as GeoJSON for frontend rendering
                return jsonify({
                    'main_route': convert_to_geojson(optimal_path),
                    'alternative_route': convert_to_geojson(alt_path)
                })
            
            else:
                errors = form_errors(map_form)
                
                # Log form validation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'map_form_validation_failed', 
                    message=str(errors), 
                    level=logging.WARNING
                )
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500



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



# function for heurisctic
def map_based_heuristic(node, goal):
    """
    Calculate heuristic based on straight-line distance plus traffic factor
    """
    # Calculate straight-line distance using haversine formula
    distance = haversine(
        (node['latitude'], node['longitude']),
        (goal['latitude'], goal['longitude'])
    )
    
    # Apply traffic factor based on time of day and historical data
    traffic_multiplier = get_traffic_factor(node, current_time())
    
    return distance * traffic_multiplier



#fucntion for map neighbors
def get_map_neighbors(node):
    """
    Get neighboring intersections from current position
    """
    # Query Google Maps Roads API or cached network data
    nearby_intersections = get_nearby_intersections(
        node['latitude'], 
        node['longitude'],
        radius=500  # meters
    )
    
    neighbors = []
    for intersection in nearby_intersections:
        # Calculate actual road distance/time between points
        route_info = get_route_segment(node, intersection)
        cost = route_info['duration']  # or distance
        neighbors.append((intersection, cost))
        
    return neighbors