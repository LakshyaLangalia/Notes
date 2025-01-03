# init.py initializes the web app

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# creates an SQLAlchemy instance
db = SQLAlchemy()
DB_NAME = "database.db"

# this function initializes and returns the Flask application
def create_app():

    # Initializes the flask application
    app = Flask(__name__)

    # stores the secret key which secures sessions and stores cookies
    # for each specific user
    app.config['SECRET_KEY'] = 'secretkey'

    # Configures the app to use an SQLite db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # binds the SQLAlchemy instance to the Flask app
    db.init_app(app)

    # Imports the views and auth blueprints and registers the 
    # blueprints with the application
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #imports the User and Note classes from models.py
    from .models import User, Note

    # creates the database if not done so already
    create_database(app)

    # Takes advantage of the flask_login module to manage logins
    # sets the route to auth.login, and binds the Login Manager
    # to the Flask app
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Retrieves a user using their ID
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# creates the database if it doesn't already exist
def create_database(app):
    if not path.exists('Website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database created.")
