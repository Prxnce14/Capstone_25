import os
from . import app
from flask import render_template, request, redirect, url_for, make_response



###
# Routing for our application.
###

@app.route('/home')
def base():
    """Render website's home page."""
    return render_template('base.html')


@app.route('/locations')
def locations():
    """Render website's locations page."""
    myapi_key = os.environ.get('API_KEY')
    mymap_id = os.environ.get('MAP_ID')
    response = make_response(render_template('index.html', api_key=myapi_key, map_id=mymap_id))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    

