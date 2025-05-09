import os
from . import app, db
from flask import render_template, request, redirect, url_for, make_response, jsonify, flash
from flask_wtf.csrf import generate_csrf
from app.forms import UsersForm, DriverForm, RestaurantForm, RestaurantProduct
from app.models import Users, Driver, Restaurant, Product
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import uuid




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

                return jsonify({
                    "message": "Driver Successfully added",
                    "usernane": uname,
                })
            
            else:
                errors = form_errors(driverform)
                return jsonify({'errors': errors})
        
        except Exception as e:
            #Handle any exceptions here
            return jsonify({'error': str(e)}), 500 #Return JSON response for error


@app.route('/api/restaurant/register', methods=['POST'])
def restaurant_register():
    if request.method == 'POST':
        try:
            restaurantform = RestaurantForm()
            if restaurantform.validate_on_submit():

                print("ready to process the form")
                uname = restaurantform.username.data
                pword = restaurantform.password.data
                fname = restaurantform.firstname.data
                lname = restaurantform.lastname.data
                email = restaurantform.email.data
                phone = restaurantform.phone_number.data
                store_name = restaurantform.store_name.data
                store_addr = restaurantform.store_address.data
                new_restaurant = Restaurant(uname, pword, fname, lname, email, phone, store_name, store_addr, user_type='restaurant')

                existing_restaurant = Restaurant.query.filter_by(username=uname).first()
                if existing_restaurant:
                    return jsonify({"error": "Username already exists"}), 400
                
                existing_store = Restaurant.query.filter_by(store_name = store_name, store_address=store_addr).first()
                if existing_store:
                    return jsonify({"error": "Restaurant with this name and address already exists"}), 400
                
                db.session.add(new_restaurant)
                db.session.commit()

                return jsonify({
                    "message": "Restaurant Successfully added",
                    "username": uname,
                    "store_name": store_name
                })
            
            else:
                errors = form_errors(restaurantform)
                return jsonify({'errors': errors})
        
        except Exception as e:
            return jsonify({'errror': str(e)}), 500
                
#Add Product

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/restaurant/products', methods=['POST'])
def create_product():
    try:
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
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_name)
                form.image_file.data.save(image_path)
                image_url = f"/uploads/{unique_name}"
            
            # Create a new Product (not RestaurantProduct which is the form)
            new_product = Product(
                restaurant_id=form.restaurant_id.data,
                name=form.name.data,
                price=form.price.data,
                quantity=form.quantity.data,
                image_url=image_url,
                description=form.description.data if hasattr(form, 'description') else None,
                category=form.category.data if hasattr(form, 'category') else None,
                is_vegetarian=form.is_vegetarian.data if hasattr(form, 'is_vegetarian') else False,
                is_vegan=form.is_vegan.data if hasattr(form, 'is_vegan') else False,
                is_gluten_free=form.is_gluten_free.data if hasattr(form, 'is_gluten_free') else False,
                is_featured=form.is_featured.data if hasattr(form, 'is_featured') else False,
                discount_percentage=form.discount_percentage.data if hasattr(form, 'discount_percentage') else 0,
                minimum_stock=form.minimum_stock.data if hasattr(form, 'minimum_stock') else 0
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            return jsonify({
                'message': 'Product created successfully', 
                'product': new_product.to_dict()
            }), 201
        else:
            return jsonify({'error': 'Validation failed', 'errors': form.errors}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# DELETE A PRODUCT

@app.route('/api/restaurant/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = RestaurantProduct.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@app.route('/login', methods=['POST', 'GET'])
def login():
    """Render website's login page."""
    
    # return render_template('login.html', name="Pelican Eats")
    return render_template('about.html', name="Pelican Eats - Login")




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


# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""
#     return render_template('404.html'), 404