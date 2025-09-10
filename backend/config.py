from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_session import Session
import os, redis

# Get spotipy secrets from env file
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = os.getenv("SCOPE")
DB_URL = os.getenv('DB_URL')

# Init flask app
app = Flask(__name__)

# Init db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Redis Setup with Sessions
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url(DB_URL)
app.config['SECRET_KEY'] = os.urandom(64)

app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allows cross-origin
app.config['SESSION_COOKIE_SECURE'] = False     # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.config['SESSION_COOKIE_DOMAIN'] = None  # Let Flask handle it
app.config['SESSION_COOKIE_PATH'] = '/'

session_client = Session(app)

# Cors for app
CORS(app, 
     origins=['http://localhost:3000'],
     supports_credentials=True)
