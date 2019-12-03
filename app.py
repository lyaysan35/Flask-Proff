import os
from flask import Flask, g # stands for global and we are setting up a global 
# access to our database throughout the app
from flask_cors import CORS 
from flask_login import LoginManager
# from resources.users import user
# from resources.professionals import professional
import models 


login_manager = LoginManager()

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)



app.secret_key = 'xxxxyyi0oiu gew;i gkeirg;iqwtiq;hreirasdfjlksadlkfjalsdjzzzzz'
login_manager = LoginManager()
login_manager.init_app(app)

# Decorator that will load the user object whenver we access the session
# by import currect_user from flask_login
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None




@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'hi'


CORS(professional, origins=['http://localhost:3000'], supports_credentials=True) # adding this line
app.register_blueprint(professional, url_prefix='/api/v1/professionals') # adding this line

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/users')




# Run the app when the program starts!
if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)