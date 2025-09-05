import spotipy, time, spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE
from flask import session
from collections import defaultdict, Counter

cache_handler=FlaskSessionCacheHandler(session)
spOAuth = SpotifyOAuth(
    client_id = CLIENT_ID, 
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope=SCOPE,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = spotipy.Spotify(auth_manager=spOAuth)

def getTokenService():
    tokenInfo = cache_handler.get_cached_token()
    if not tokenInfo:
        return None
    now = int(time.time())
    isExpired = tokenInfo['expires_at'] - now < 60
    if isExpired:
        tokenInfo = spOAuth.refresh_access_token(tokenInfo['refresh_token'])
        session["token_info"] = tokenInfo
    return tokenInfo

def checkTokenService():
    if not spOAuth.validate_token(cache_handler.get_cached_token()):
        authURL = spOAuth.get_authorize_url()
        return authURL
    return None

def getTopSongsService(): 
    t = defaultdict(list)
    orderedTracks = []
    tracks = sp.current_user_top_tracks(limit=50, time_range='short_term')
    for track in tracks['items']:
        artistId = track['artists'][0]['id']
        trackId = track['id']
        trackName = track['name']
        orderedTracks.append((artistId, trackId, trackName))
        t[artistId].append({
            'id': trackId,
            'name': trackName
        })
    return t, orderedTracks
    
def getGenresService(artists):
    artistDict = {}
    artistsRes = sp.artists(artists)
    for a in artistsRes['artists']:
        artistDict[a['id']]=({
            'name': a['name'],
            'genres': a['genres']
        })
    return artistDict

def getPlaylistsService():
    playlists = []
    req = sp.current_user_playlists()
    for playlist in req['items']:
        playlists.append({
            'id': playlist['id'],
            'name': playlist['name'],
            'total': playlist['tracks']['total']
        })
    return playlists

def getPlaylistService(playlistId):
    playlist = []
    req = sp.get_playlist(playlistId, fields=None, market=None, additional_types=('track',))
    for item in req['tracks']['items']:
        track = item['track']
        playlist.append({
            'id': track['id'],
            'name': track['name'],
            'artistId': track['artists'][0]['id'],
            'artist': track['artists'][0]['name']
        })
    return playlist

def createPlaylistService():
    pass

def addQueueToService():
    pass