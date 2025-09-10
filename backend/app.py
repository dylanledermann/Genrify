from flask import request, jsonify, redirect
from config import app, db, redis_client
from utils import spOAuth, sp, checkTokenService, getTopSongsService, getGenresService, getPlaylistsService, getPlaylistService
# Get spotify login
@app.route("/api/login")
def login():
    auth, redir = checkTokenService()
    return jsonify({'auth': auth, 'redirect': redir})

@app.route("/api/logout")
def logout():
    redis_client.delete('flask_cache_token_info')
    return jsonify({})

# Callback for spotipy
@app.route("/api/callback", methods=['GET'])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"message": "No code given"}), 400
    spOAuth.get_access_token(code, as_dict=True)
    frontend_loc = "http://localhost:3000/profile"
    return redirect(frontend_loc)

# Get all info needed for the user's profile
@app.route("/api/profile", methods=["GET"])
def profile():
    auth, redir = checkTokenService()
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    userProfile = sp.current_user()
    return jsonify({'userProfile': userProfile['display_name'], 'profilePicture': userProfile['images']})

# Get 50 most played songs and their genres
@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    auth, redir = checkTokenService()
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    id = request.args.get('q')
    if id:
        playlist, tracks, orderedTracks = getPlaylistService(id)
    else:
        playlist = 'Top Songs'
        tracks, orderedTracks = getTopSongsService()
    artists = getGenresService(list(tracks.keys()))
    return jsonify({'playlist': playlist,'tracks': orderedTracks, 'artistsTracks': tracks, 'artistsGenres': artists})

# Get users playlists
@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    auth, redir = checkTokenService()
    if not auth:
        return jsonify({'error': 'Unauthorized'}), 401
    playlists = getPlaylistsService()
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
    with app.app_context():
        db.create_all()

    app.run(debug=True)