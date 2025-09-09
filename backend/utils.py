import spotipy, time, spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import RedisCacheHandler
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE, cache
from flask import session
from collections import defaultdict, Counter

cache_handler=RedisCacheHandler(cache)
spOAuth = SpotifyOAuth(
    client_id = CLIENT_ID, 
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope=SCOPE,
    cache_handler=cache_handler,
    cache_path=None,
    show_dialog=True
)

sp = spotipy.Spotify(auth_manager=spOAuth)

def setTokenService(token):
    cache_handler.save_token_to_cache(token)
    print(cache_handler.get_cached_token())

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
    return "http://127.0.0.1:3000/profile"

def getTopSongsService(): 
    t = defaultdict(list)
    orderedTracks = []
    tracks = sp.current_user_top_tracks(limit=50, time_range='short_term')
    for track in tracks['items']:
        artistId = track['artists'][0]['id']
        artistName = track['artists'][0]['name']
        trackId = track['id']
        trackName = track['name']
        orderedTracks.append((artistId, artistName, trackId, trackName))
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
    t = defaultdict(list)
    orderedTracks = []
    tracks = sp.playlist(playlistId, fields=None, market=None, additional_types=('track',))
    for item in tracks['tracks']['items']:
        track = item['track']
        artistId = track['artists'][0]['id']
        artistName = track['artists'][0]['name']
        trackId = track['id']
        trackName = track['name']
        orderedTracks.append((artistId, artistName, trackId, trackName))
        t[artistId].append({
            'id': trackId,
            'name': trackName
        })
    return tracks['name'], t, orderedTracks

def createPlaylistService():
    pass

def addQueueToService():
    pass