from flask import request, jsonify, session, redirect
from config import app, db
from utils import spOAuth, sp, checkTokenService, getTopSongsService, getGenresService, getPlaylistsService, getPlaylistService
# Get spotify login
@app.route("/api/login")
def login():
    redir = checkTokenService()
    return redirect(redir) if redir else redirect('/api/profile')

@app.route("/api/logout", methods=['POST'])
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
    return redirect("/api/profile")

# Get all info needed for the user's profile
@app.route("/api/profile", methods=["GET"])
def profile():
    redir = checkTokenService()
    if redir:
        return redirect(redir)
    userProfile = sp.current_user()
    return jsonify({'userProfile': userProfile})

# Get 50 most played songs and their genres
@app.route('/api/top', methods=['GET'])
def get_playlists():
    redir = checkTokenService()
    if redir:
        return redirect(redir)
    tracks, orderedTracks = getTopSongsService()
    artists = getGenresService(list(tracks.keys()))
    return jsonify({'tracks': orderedTracks, 'artistsTracks': tracks, 'artistsGenres': artists})

# Get users playlists
@app.route('/api/playlists', method=['GET'])
def get_playlists():
    redir = checkTokenService()
    if redir:
        return redirect(redir)
    playlists = getPlaylistsService()
    return jsonify({'playlists': playlists})

# Search for playlist from user's spotify
@app.route("/api/search", methods=["GET"])
def get_playlist():
    id = request.args.get('q')
    playlist = getPlaylistService(id)
    return jsonify({'playlist': playlist})
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