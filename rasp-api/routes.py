from __main__ import app
import sys, os
from datetime import timedelta, datetime, timezone
from flask import request, jsonify
#import the flask-jwt-extended interface in the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'flask-jwt-extended'))

DEBUG=True

myname = os.environ.get("ME")

# create a default route
@app.route('/')
def hello():
    ''' 
This route prints the welcome message using the myname variable passed in as an environment variable.
    '''
    return f'Welcome to CS190B Sensors Hub from {myname}\n', 200
