from flask import request, jsonify, session, redirect
from config import app, db, cache
from utils import cache_handler, spOAuth, sp, checkTokenService, getTopSongsService, getGenresService, getPlaylistsService, getPlaylistService
# Get spotify login
@app.route("/api/login")
def login():
    redir = checkTokenService()
    return jsonify({'redirect': redir})

@app.route("/api/logout")
def logout():
    session.clear()
    return redirect("/api/login")

# Callback for spotipy
@app.route("/api/callback", methods=['GET'])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"message": "No code given"}), 400
    # getTokenService()
    spOAuth.get_access_token(code, as_dict=True)
    frontend_loc = "http://localhost:3000/profile"
    return redirect(frontend_loc)

# Get all info needed for the user's profile
@app.route("/api/profile", methods=["GET"])
def profile():
    redir = checkTokenService()
    if redir != "http://127.0.0.1:3000/profile":
        return jsonify({'error': 'Unauthorized'}), 401
    userProfile = sp.current_user()
    return jsonify({'userProfile': userProfile})

# Get 50 most played songs and their genres
@app.route('/api/playlist', methods=['GET'])
def get_playlist():
    redir = checkTokenService()
    if redir != "http://127.0.0.1:3000/profile":
        return jsonify({'message': 'Unauthorized'}), 401
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
    redir = checkTokenService()
    if redir != "http://127.0.0.1:3000/profile":
        return jsonify({'message': 'Unauthorized'}), 401
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