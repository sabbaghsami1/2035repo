import os
from flask import Flask, url_for


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
import secrets

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///csc2031blog.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(
    naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)


# Add reCAPTCHA Configuration
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdgyVUqAAAAAOlpHkzRlx7dr2F0SYp3QTp5Mo96'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdgyVUqAAAAANmq8UrWlHqa4taLr7ZR8nJWh_Pd'
app.config['RECAPTCHA_USE_SSL'] = False  # Change to True if you're using https
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'dark'}  # Optional: Customize reCAPTCHA appearance


# Initialize limiter with the Flask app
limiter = Limiter(
    get_remote_address,
    app=app,  # Attach the limiter to the Flask app
    default_limits=["500/day"]  # Global rate limit
)


# Global rate limit for the entire application (500 calls per day)
app.config['DEFAULT_RATE_LIMIT'] = "500/day"
limiter.limit(app.config['DEFAULT_RATE_LIMIT'])


#DATABASE TABLES
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    user = db.relationship("User", back_populates="posts")

    def __init__(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body

    def update(self, title, body):
        self.created = datetime.now()
        self.title = title
        self.body = body
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User information
    multifactor = db.Column(db.String(100), nullable=False, default="default_mfa_key")
    multifactor_enabled = db.Column(db.Boolean, nullable=False, default=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)

    # User posts
    posts = db.relationship("Post", order_by=Post.id, back_populates="user")

    def __init__(self, email, multifactor, multifactor_enabled, firstname, lastname, phone, password):
        self.email = email
        self.multifactor = multifactor
        self.multifactor_enabled = multifactor_enabled
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = password


    def verify_password(self,password):
        return self.password == password



# DATABASE ADMINISTRATOR
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for('index')


class PostView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'userid', 'created', 'title', 'body', 'user')


class UserView(ModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'email', 'password', 'firstname', 'lastname', 'phone', 'posts')


admin = Admin(app, name='DB Admin')
admin._menu = admin._menu[1:]  # removes home tab
admin.add_link(MainIndexLink(name='Home'))
admin.add_view(PostView(Post, db.session))
admin.add_view(UserView(User, db.session))

from accounts.views import accounts_bp
from posts.views import posts_bp
from security.views import security_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(security_bp)
