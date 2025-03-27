import os
from . import app
from flask import render_template, request, redirect, url_for


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
    return render_template('index.html')