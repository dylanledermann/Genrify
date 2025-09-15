from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flask_session import Session
import os, redis, time

# Get spotipy secrets from docker

def getDockerSecret(secretName):
     try:
          with open(f'/run/secrets/{secretName}', 'r') as secret_file:
               return secret_file.read().strip()
     except IOError:
        print('IOError occured')
        return None

CLIENT_ID = getDockerSecret('spotipy_client_id')
CLIENT_SECRET = getDockerSecret("spotipy_client_secret")
REDIRECT_URI = getDockerSecret("spotipy_redirect_uri")
SCOPE = getDockerSecret("scope")
DB_URL = getDockerSecret('db_url')
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
print(DB_URL)
# Retry to connect for 1 minute with 10 second intervals
for _ in range(6):
     redis_client = redis.from_url(DB_URL)

     try:
          redis_client.ping()
          print("Connected to Redis!")
          break
     except redis.ConnectionError:
          print("Failed to connect to Redis")
     time.sleep(10)

# Cors for app
CORS(app, 
     origins=['http://genrify-frontend:3000'],
     supports_credentials=True)
