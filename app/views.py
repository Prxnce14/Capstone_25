import os
from . import app
from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_wtf.csrf import generate_csrf




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


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Render website's register page."""
    
    # return render_template('register.html', name="Pelican Eats")
    return render_template('about.html', name="Pelican Eats - Register")


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Render website's login page."""
    
    # return render_template('login.html', name="Pelican Eats")
    return render_template('about.html', name="Pelican Eats - Login")

# @app.route('/delivery')
# def locations():
#     """Render website's locations page."""
#     myapi_key = os.environ.get('API_KEY')
#     mymap_id = os.environ.get('MAP_ID')
#     response = make_response(render_template('index.html', api_key=myapi_key, map_id=mymap_id))
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response


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

@app.route('/api/v1/csrf-token', methods=['GET'])
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