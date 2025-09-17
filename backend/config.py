from flask import Flask
from flask_cors import CORS
import redis, time

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
FRONTEND_URL = getDockerSecret('frontend_url')
# Init flask app
app = Flask(__name__)

# Init redis client connection
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

# CORS for app
CORS(app, 
     origins=['http://genrify-frontend:3000'],
     supports_credentials=True)
