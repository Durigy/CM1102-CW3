from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
import shop.varibles as db_var

app = Flask(__name__)
app.config['SECRET_KEY'] = db_var.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = db_var.SQLALCHEMY_DATABASE_URI
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=30)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
# login_manager.init_app()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

from shop import routes
from shop.models import User
