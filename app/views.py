import os
import logging
from logging.handlers import RotatingFileHandler
from app import app, db, login_manager, log_security_event
from flask import render_template, request, redirect, url_for, make_response, jsonify, flash, session
from flask_wtf.csrf import generate_csrf
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import UsersForm, DriverForm, RestaurantForm, LoginForm, MapForm,RestaurantProduct
from datetime import datetime, timedelta
from app.models import Users, Driver, Restaurant, Product
from app.forms import UsersForm, DriverForm, RestaurantForm, LoginForm, MapForm, OnboardingForm
from datetime import datetime, timedelta
from app.models import Users, Driver, Restaurant, UserPreferences
from functools import wraps
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.helpers import convert_to_geojson, get_node_from_location, get_route_segment, haversine, get_nearby_intersections
from app.helpers import get_traffic_factor, current_time
from app.locations import a_star
from werkzeug.utils import secure_filename
import uuid
from app.recommendation_helper import get_user_food_recommendations



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
    

# Registration route for drivers   
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


# Registration route for restaurants
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
                    return jsonify({"error": "Restaurant with this name and address already exists"}), 400
                
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
        
#Get Product 
@app.route('/api/restaurant/products', methods=['GET'])
@jwt_required()
def get_restaurant_products():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Ensure only restaurant users can access this endpoint
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        # Get all products for this restaurant
        products = Product.query.filter_by(restaurant_id=current_user_id).all()
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting restaurant products: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


#Add Product

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/restaurant/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Ensure only restaurant users can create products
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can create products'}), 403
        
        # Get restaurant user
        restaurant = Restaurant.query.get(current_user_id)
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Use WTForms to validate the form data
        form = RestaurantProduct(request.form)
        
        # For file uploads, we need to add it manually since it's not part of request.form
        if 'image' in request.files:
            form.image_file.data = request.files['image']
        
        if form.validate():
            # Handle image upload
            image_url = form.image_url.data
            
            if form.image_file.data and allowed_file(form.image_file.data.filename):
                filename = secure_filename(form.image_file.data.filename)
                unique_name = f"{uuid.uuid4().hex}_{filename}"
                
                # Get the full path to the uploads directory
                uploads_path = os.path.join(app.static_folder, 'uploads')
                image_path = os.path.join(uploads_path, unique_name)
                
                # Make sure directory exists
                os.makedirs(uploads_path, exist_ok=True)
                
                app.logger.debug(f"Saving image to: {image_path}")
                form.image_file.data.save(image_path)
                
                # Use a URL that will work with static files
                image_url = f"/static/uploads/{unique_name}"
                app.logger.debug(f"Image URL saved to database: {image_url}")
            
            # Create product with the image URL
            new_product = Product(
                restaurant_id=current_user_id,
                name=form.name.data,
                price=form.price.data,
                quantity=form.quantity.data,
                image_url=image_url,
                description=form.description.data,
                category=form.category.data,
                is_vegetarian=form.is_vegetarian.data,
                is_vegan=form.is_vegan.data,
                is_gluten_free=form.is_gluten_free.data,
                is_featured=form.is_featured.data,
                discount_percentage=form.discount_percentage.data or 0,
                minimum_stock=form.minimum_stock.data or 0
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            # Log the created product details
            app.logger.info(f"Product created: {new_product.name}, image URL: {new_product.image_url}")
            
            return jsonify({
                'message': 'Product created successfully', 
                'product': new_product.to_dict()
            }), 201
        else:
            app.logger.warning(f"Product validation failed: {form.errors}")
            return jsonify({'error': 'Validation failed', 'errors': form.errors}), 400
            
    except Exception as e:
        db.session.rollback()
        # Get detailed error information including stack trace
        import traceback
        error_trace = traceback.format_exc()
        app.logger.error(f"Error creating product: {str(e)}\n{error_trace}")
        return jsonify({'error': 'Internal server error'}), 500

#  delete_product endpoint
@app.route('/api/restaurant/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Ensure only restaurant users can delete products
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can delete products'}), 403
        
        # Get the product
        product = Product.query.get_or_404(product_id)
        
        # Ensure only the restaurant that owns the product can delete it
        if str(product.restaurant_id) != str(current_user_id):
            return jsonify({'error': 'You can only delete your own products'}), 403
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Edit Product endpoint 

@app.route('/api/restaurant/products/<int:product_id>', methods=['GET', 'PUT'])
@jwt_required()
def product_details(product_id):
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Get the product
        product = Product.query.get_or_404(product_id)
        
        if request.method == 'GET':
            # Anyone can view product details
            return jsonify({'product': product.to_dict()}), 200
            
        elif request.method == 'PUT':
            # Only restaurant owners can update their own products
            if user_type != 'restaurant':
                return jsonify({'error': 'Only restaurant accounts can update products'}), 403
                
            if str(product.restaurant_id) != str(current_user_id):
                return jsonify({'error': 'You can only update your own products'}), 403
            
            # Use WTForms to validate the form data
            form = RestaurantProduct(request.form)
            
            # For file uploads, we need to add it manually since it's not part of request.form
            if 'image' in request.files:
                form.image_file.data = request.files['image']
            
            if form.validate():
                # Update product fields
                product.name = form.name.data
                product.price = form.price.data
                product.quantity = form.quantity.data
                
                # Handle image update
                if form.image_file.data and allowed_file(form.image_file.data.filename):
                    filename = secure_filename(form.image_file.data.filename)
                    unique_name = f"{uuid.uuid4().hex}_{filename}"
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                    form.image_file.data.save(image_path)
                    product.image_url = f"/uploads/{unique_name}"
                elif form.image_url.data:
                    product.image_url = form.image_url.data
                
                product.description = form.description.data
                product.category = form.category.data
                product.is_vegetarian = form.is_vegetarian.data
                product.is_vegan = form.is_vegan.data
                product.is_gluten_free = form.is_gluten_free.data
                product.is_featured = form.is_featured.data
                product.discount_percentage = form.discount_percentage.data or 0
                product.minimum_stock = form.minimum_stock.data or 0
                
                db.session.commit()
                
                return jsonify({
                    'message': 'Product updated successfully', 
                    'product': product.to_dict()
                }), 200
            else:
                return jsonify({'error': 'Validation failed', 'errors': form.errors}), 400
                
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error handling product: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
# General user view all products

@app.route('/api/menu/products', methods=['GET'])
def get_menu_products():
    try:
        # Get all products (or filter by restaurant ID if provided in query params)
        restaurant_id = request.args.get('restaurant_id')
        
        if restaurant_id:
            products = Product.query.filter_by(restaurant_id=restaurant_id).all()
        else:
            # Get all products from all restaurants if no specific restaurant requested
            products = Product.query.all()
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
    except Exception as e:
        app.logger.error(f"Error getting menu products: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/current-user', methods=['GET'])
@jwt_required()
def get_current_user():
    """Return the current logged-in user information using JWT."""
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Find user based on type from JWT claims
        if user_type == 'restaurant':
            user = Restaurant.query.get(current_user_id)
        elif user_type == 'driver':
            user = Driver.query.get(current_user_id)
        else:
            user = Users.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user_data = {
            'id': current_user_id,
            'user_type': user_type,
            'username': user.get_username()
        }
        
        # Add specific data based on user type
        if user_type == 'restaurant':
            user_data.update({
                'store_name': user.store_name,
                'store_address': user.store_address,
                'email': user.email,
                'phone_number': user.phone_number
            })
        else:
            user_data.update({
                'firstname': user.firstname,
                'lastname': user.lastname,
                'email': user.email,
                'phone_number': user.phone_number
            })
        
        return jsonify({'user': user_data}), 200
    except Exception as e:
        app.logger.error(f"Error getting current user: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Dashboard Stats Route
@app.route('/api/restaurant/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        # Calculate today's stats (you'll need to implement these based on your Order model)
        today = datetime.now().date()
        
        # Mock data for now - replace with actual database queries
        stats = {
            'todayOrders': 0,
            'todayRevenue': 0.0,
        }
        
        # Add actual database queries here when you have Order model
        # orders_today = Order.query.filter(
        #     Order.restaurant_id == current_user_id,
        #     func.date(Order.created_at) == today
        # ).all()
        # 
        # stats['todayOrders'] = len(orders_today)
        # stats['todayRevenue'] = sum(order.total for order in orders_today)
        
        return jsonify(stats), 200
    except Exception as e:
        app.logger.error(f"Error getting dashboard stats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Restaurant Orders Route
@app.route('/api/restaurant/orders', methods=['GET'])
@jwt_required()
def get_restaurant_orders():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        # Mock data for now - replace with actual database queries
        orders = []
        
        # Add actual database queries here when you have Order model
        # orders = Order.query.filter_by(restaurant_id=current_user_id).all()
        # orders_data = [order.to_dict() for order in orders]
        
        # For now, return empty orders array
        return jsonify({'orders': orders}), 200
    except Exception as e:
        app.logger.error(f"Error getting restaurant orders: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Update Order Status Route
@app.route('/api/restaurant/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
            
        # Add actual database queries here when you have Order model
        # order = Order.query.get_or_404(order_id)
        # 
        # if order.restaurant_id != current_user_id:
        #     return jsonify({'error': 'You can only update your own orders'}), 403
        # 
        # order.status = data['status']
        # db.session.commit()
        
        return jsonify({'message': 'Order status updated successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error updating order status: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Restaurant Sales Route
@app.route('/api/restaurant/sales', methods=['GET'])
@jwt_required()
def get_restaurant_sales():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        # Get date range from query params
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Mock data for now - replace with actual database queries
        sales_data = {
            'totalRevenue': 0,
            'totalOrders': 0,
            'averageOrderValue': 0,
            'topItem': '',
            'topItems': [],
            'recentOrders': []
        }
        
        # Add actual database queries here when you have Order model
        # sales_data = calculate_sales_data(current_user_id, start_date, end_date)
        
        return jsonify(sales_data), 200
    except Exception as e:
        app.logger.error(f"Error getting restaurant sales: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Restaurant Profile Route
@app.route('/api/restaurant/profile', methods=['GET', 'PUT'])
@jwt_required()
def restaurant_profile():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        restaurant = Restaurant.query.get(current_user_id)
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        if request.method == 'GET':
            # Return restaurant profile data
            profile_data = {
                'id': restaurant.id,
                'name': restaurant.store_name,
                'display_name': restaurant.display_name,
                'email': restaurant.email,
                'phone': restaurant.phone_number,
                'address': restaurant.store_address,
                # Add other fields as needed
            }
            return jsonify({'profile': profile_data}), 200
        
        elif request.method == 'PUT':
            # Update restaurant profile
            data = request.get_json()
            
            if 'name' in data:
                restaurant.store_name = data['name']
            if 'display_name' in data:
                restaurant.display_name = data['display_name']
            if 'email' in data:
                restaurant.email = data['email']
            if 'phone' in data:
                restaurant.phone_number = data['phone']
            if 'address' in data:
                restaurant.store_address = data['address']
            
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200
            
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error handling restaurant profile: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Restaurant Settings Route
@app.route('/api/restaurant/settings', methods=['GET', 'PUT'])
@jwt_required()
def restaurant_settings():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        if user_type != 'restaurant':
            return jsonify({'error': 'Only restaurant accounts can access this endpoint'}), 403
        
        restaurant = Restaurant.query.get(current_user_id)
        if not restaurant:
            return jsonify({'error': 'Restaurant not found'}), 404
        
        if request.method == 'GET':
            # Return restaurant settings (you'll need to add settings fields to your Restaurant model)
            settings_data = {
                # Add settings fields here
                'notifications': {},
                'payment': {},
                'ordering': {},
                # etc.
            }
            return jsonify({'settings': settings_data}), 200
        
        elif request.method == 'PUT':
            # Update restaurant settings
            data = request.get_json()
            
            # Update settings based on data
            # You'll need to add logic to update specific settings
            
            db.session.commit()
            return jsonify({'message': 'Settings updated successfully'}), 200
            
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error handling restaurant settings: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500 

@app.route('/login', methods=['POST', 'GET'])
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



# Add logout endpoint
@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        current_user_id = get_jwt_identity()
        jwt_claims = get_jwt()
        user_type = jwt_claims.get('user_type')
        
        # Log the logout event
        log_security_event(
            app.security_logger, 
            request, 
            'logout', 
            user_id=current_user_id,
            username=jwt_claims.get('name', 'Unknown'),
            message=f"{user_type} logged out"
        )
        
        # In a more advanced setup, you would add the JWT to a blacklist here
        # For now, we'll just return success
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        app.logger.error(f"Error during logout: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

# Redirect URL based on user type
def get_redirect_url(user_type):
    """Return the appropriate redirect URL based on user type"""
    if user_type == 'gen_user':
        return '/gen/onboarding'
        #return 'gen/dashboard'
    elif user_type == 'driver':
        return '/driver/dashboard'
    elif user_type == 'restaurant':
        return '/restaurant'



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



# Food perferences onbarding function and route

def create_user_preferences_from_form(user_id, form):
    """Convert form data to UserPreferences model instance"""
    
    # Extract data from nested forms
    food_prefs = form.food_preferences
    delivery_prefs = form.delivery_preferences
    comm_prefs = form.communication_preferences
    
    # Build the preferences dictionary
    prefs_data = {
        'user_id': user_id,
        
        # JSON fields (dynamic lists)
        'liked_foods': food_prefs.liked_foods.data,
        'dietary_restrictions': food_prefs.dietary_restrictions.data,
        'order_times': food_prefs.order_times.data,
        
        # Flavor preferences
        'spice_level': food_prefs.flavor_preferences.spice_level.data,
        'healthy_level': food_prefs.flavor_preferences.healthy_level.data,
        'sweet_preference': food_prefs.flavor_preferences.sweet_preference.data,
        
        # Meat preferences
        'chicken': food_prefs.meat_preferences.chicken.data,
        'fish': food_prefs.meat_preferences.fish.data,
        'pork': food_prefs.meat_preferences.pork.data,
        'goat': food_prefs.meat_preferences.goat.data,
        'beef': food_prefs.meat_preferences.beef.data,
        'no_meat': food_prefs.meat_preferences.no_meat.data,
        'other_meat': food_prefs.meat_preferences.other_meat.data,
        
        # Budget
        'budget': food_prefs.budget.data,
        'additional_notes': food_prefs.additional_notes.data,
        
        # Delivery preferences
        'default_address': delivery_prefs.default_address.data,
        'delivery_instructions': delivery_prefs.delivery_instructions.data,
        'preferred_delivery_time': delivery_prefs.preferred_delivery_time.data,
        
        # Communication preferences
        'email_notifications': comm_prefs.email_notifications.data,
        'sms_notifications': comm_prefs.sms_notifications.data,
        'promotional_emails': comm_prefs.promotional_emails.data
    }
    
    # Add all the boolean preferences (breakfast, lunch, cooking styles, etc.)
    boolean_mappings = {
        # Cooking styles
        'cooking_jamaican': food_prefs.cooking_styles.jamaican.data,
        'cooking_indian': food_prefs.cooking_styles.indian.data,
        'cooking_chinese': food_prefs.cooking_styles.chinese.data,
        'cooking_african': food_prefs.cooking_styles.african.data,
        'cooking_vegan_ital': food_prefs.cooking_styles.vegan_ital.data,
        'cooking_italian': food_prefs.cooking_styles.italian.data,
        
        # Breakfast items
        'porridge': food_prefs.breakfast_preferences.porridge.data,
        'scrambled_eggs': food_prefs.breakfast_preferences.scrambled_eggs.data,
        'pancakes': food_prefs.breakfast_preferences.pancakes.data,
        'french_toast': food_prefs.breakfast_preferences.french_toast.data,
        'waffles': food_prefs.breakfast_preferences.waffles.data,
        'bacon': food_prefs.breakfast_preferences.bacon.data,
        'sausage': food_prefs.breakfast_preferences.sausage.data,
        'sandwich': food_prefs.breakfast_preferences.sandwich.data,
        
        # Lunch preferences
        'fry_chicken': food_prefs.lunch_preferences.fry_chicken.data,
        'bake_chicken': food_prefs.lunch_preferences.bake_chicken.data,
        'curry_goat': food_prefs.lunch_preferences.curry_goat.data,
        'soups': food_prefs.lunch_preferences.soups.data,
        'steamed_fish': food_prefs.lunch_preferences.steamed_fish.data,
        'escovitch_fish': food_prefs.lunch_preferences.escovitch_fish.data,
        'patty': food_prefs.lunch_preferences.patty.data,
        'sandwiches': food_prefs.lunch_preferences.sandwiches.data,
        'pasta': food_prefs.lunch_preferences.pasta.data,
        
        # Juice preferences
        'pine_ginger': food_prefs.juice_preferences.pine_ginger.data,
        'callallo_juice': food_prefs.juice_preferences.callallo.data,
        'june_plum': food_prefs.juice_preferences.june_plum.data,
        'guava_pine': food_prefs.juice_preferences.guava_pine.data,
        'beet_root': food_prefs.juice_preferences.beet_root.data,
        'orange_juice': food_prefs.juice_preferences.orange.data,
    }
    
    # Handle popular Jamaican breakfast items (FieldList)
    if food_prefs.popular_preferences and len(food_prefs.popular_preferences) > 0:
        popular_form = food_prefs.popular_preferences[0]
        popular_mappings = {
            'ackee_saltfish': popular_form.ackee_saltfish.data,
            'callaloo': popular_form.callaloo.data,
            'cooked_saltfish': popular_form.cooked_saltfish.data,
            'kidney': popular_form.kidney.data,
            'liver': popular_form.liver.data,
            'fried_plantain': popular_form.fried_plantain.data,
            'dumplings': popular_form.dumplings.data,
            'festival': popular_form.festival.data,
            'breadfruit': popular_form.breadfruit.data,
            'other_breakfast_items': popular_form.other_breakfast_items.data if hasattr(popular_form, 'other_breakfast_items') else None
        }
        boolean_mappings.update(popular_mappings)
    
    # Add string fields
    string_mappings = {
        'other_cooking_style': food_prefs.cooking_styles.other_style.data,
        'other_breakfast': food_prefs.breakfast_preferences.other_breakfast.data,
        'other_lunch': food_prefs.lunch_preferences.other_lunch.data,
        'other_juice': food_prefs.juice_preferences.other_juice.data,
    }
    
    # Combine all mappings
    prefs_data.update(boolean_mappings)
    prefs_data.update(string_mappings)
    
    # Create and return the UserPreferences instance
    return UserPreferences(**prefs_data)




@app.route('/api/gen/onboarding', methods=['POST'])
@login_required
def onboarding_clean():
    """Render the onboarding form for general users."""

    if request.method == 'POST':
        try:

            form = OnboardingForm()
            
            if form.validate_on_submit():
                # Get user ID
                user_id = current_user.get_id()
                user_name = current_user.get_username()
                print("ready to process the onboarding form")

                log_security_event(
                    app.security_logger, 
                    request, 
                    'process_onboarding', 
                    username=current_user.get_username(),
                    message=f"Starting onboarding process for user_id: {user_id}",
                    level=logging.INFO
                )

                # Use helper function
                user_prefs = create_user_preferences_from_form(user_id, form)
                
                # Save to database
                db.session.add(user_prefs)
                db.session.commit()

                # Log successful onboarding
                # Log registration event
                log_security_event(
                    app.security_logger, 
                    request, 
                    'onboarding_success', 
                    user_id, 
                    username=user_name,
                    message=f"{user_name} successfully completed onboarding",
                )

                return jsonify({
                    "message": f"{user_name}Successfully completed onboarding",
                })
                
                
            else:
                errors = form_errors(form)

                # Log form validation failure
                log_security_event(
                    app.security_logger, 
                    request, 
                    'onboarding_form_validation_failed',
                    message=str(errors), 
                    level=logging.WARNING
                )
                return jsonify({'errors': errors}), 400
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Endpoint for user reccoommendations
@app.route('/api/gen/recommendations', methods=['GET'])
@login_required
def get_food_recommendations():
    """Get personalized food recommendations based on user's stored preferences"""
    try:
        # Get current user ID
        user_id = current_user.get_id()
        username = current_user.get_username()
        
        # Get number of recommendations per category
        count = request.args.get('count', 3, type=int)
        
        # Get recommendations using our helper function
        recommendations = get_user_food_recommendations(user_id, n=count)
        
        # Log successful recommendation retrieval
        log_security_event(
            app.security_logger,
            request,
            'recommendations_retrieved',
            username=username,
            message=f"Retrieved food recommendations for user_id: {user_id}",
            level=logging.INFO
        )
        
        return jsonify({
            "user_id": user_id,
            "username": username,
            "recommendations": recommendations
        })
        
    except Exception as e:
        # Log error
        log_security_event(
            app.security_logger,
            request,
            'recommendations_error',
            message=str(e),
            level=logging.ERROR
        )
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