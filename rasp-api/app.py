import os, sys, dotenv, random
from datetime import datetime, timedelta
from flask import Flask

#import the flask-jwt-extended interface in the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '.', 'flask-jwt-extended'))
from flask_jwt_extended import JWTManager

def main():
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == "__main__":
    app = Flask(__name__)
    #set up the app's context 
    with app.app_context():
        dotenv.load_dotenv()
        myname = os.environ.get("ME")
    
    import routes

    #start the server app
    main()
