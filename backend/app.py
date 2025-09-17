import json
from waitress import serve
from uuid import uuid4
from flask import request, jsonify, redirect
from config import app, redis_client, FRONTEND_URL
from utils import checkTokenService, getCurrentUserService, getTokenService, getTopSongsService, getGenresService, getPlaylistsService, getPlaylistService, tokenFromCode
# Get spotify login
@app.route("/api/login")
def login():
    sessionID = request.headers['Cookie']
    token = getTokenService(sessionID)
    auth, redir = checkTokenService(token)
    return jsonify({'auth': auth, 'redirect': redir})

@app.route("/api/logout")
def logout():
    sessionID = request.headers['Cookie']
    if not sessionID:
        return jsonify({'error', 'Bad Request'}), 404
    redis_client.delete(sessionID)
    return jsonify({'message': 'success'})

# Callback for spotipy
@app.route("/api/callback", methods=['GET'])
def callback():
    code = request.args.get("code")
    if not code:
        return redirect(f'{FRONTEND_URL}')
    token = tokenFromCode(code)
    id = str(uuid4())
    redis_client.setex(id, 300, json.dumps(token))
    frontend_loc = f"{FRONTEND_URL}exchange?token={id}"
    return redirect(frontend_loc)

@app.route('/api/exchange', methods=['POST'])
def exchange():
    if request.is_json:
        body = request.get_json()
        if 'token' not in body and 'token':
            return jsonify({'error': 'Bad Request'}), 400
        exchangeToken = body['token']
        token = redis_client.get(exchangeToken)
        if not token:
            return jsonify({'error': 'Token not found'}), 404
        redis_client.delete(exchangeToken)
        sessionID = str(uuid4())
        # Create sessionID and set it to expire after 1 day
        redis_client.setex(sessionID, 60*60*24, token)
        return jsonify({'sessionID': sessionID})
    else:
        return jsonify({'error': 'Request must be JSON'}), 400

# Get all info needed for the user's profile
@app.route("/api/profile", methods=["GET"])
def profile():
    sessionID = request.headers['Cookie']
    token = getTokenService(sessionID)
    auth, redir = checkTokenService(token)
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    userProfile = getCurrentUserService(token)
    return jsonify({'userProfile': userProfile['display_name'], 'profilePicture': userProfile['images']})

# Get 50 most played songs and their genres
@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    sessionID = request.headers['Cookie']
    token = getTokenService(sessionID)
    auth, redir = checkTokenService(token)
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    id = request.args.get('q')
    if id:
        playlist, tracks, orderedTracks = getPlaylistService(token, id)
    else:
        playlist = 'Top Songs'
        tracks, orderedTracks = getTopSongsService(token)
    artists = getGenresService(token, list(tracks.keys()))
    return jsonify({'playlist': playlist,'tracks': orderedTracks, 'artistsTracks': tracks, 'artistsGenres': artists})

# Get users playlists
@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    sessionID = request.headers['Cookie']
    token = getTokenService(sessionID)
    auth, redir = checkTokenService(token)
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    playlists = getPlaylistsService(token)
    return jsonify({'playlists': playlists})

# Extra endpoints that can be added
# # Create playlist from genre
# @app.route("/api/playlist", methods=['GET'])
# def create_playlist():
#     pass

# # Add songs to queue
# @app.route("/api/queue", methods=['POST'])
# def add_to_queue():
#     pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    # serve(app, host='0.0.0.0', port=5000)