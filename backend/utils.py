import json
import time, spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPE, redis_client
from collections import defaultdict

def tokenFromCode(code):
    spOAuth = SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = REDIRECT_URI,
        scope=SCOPE,
        show_dialog=True
    )
    return spOAuth.get_access_token(code, as_dict=True)

def getTokenService(sessionID):
    token = redis_client.get(sessionID)
    if not token:
        return None
    token = json.loads(token.decode('utf-8'))
    now = int(time.time())
    isExpired = token['expires_at'] - now < 60
    if isExpired:
        spOAuth = SpotifyOAuth(
            client_id = CLIENT_ID, 
            client_secret = CLIENT_SECRET,
            redirect_uri = REDIRECT_URI,
            scope=SCOPE,
            show_dialog=True
        )
        token = spOAuth.refresh_access_token(token['refresh_token'])
        redis_client.set(sessionID, json.dumps(token))
    return token['access_token']

def checkTokenService(tokenInfo):
    if not tokenInfo:
        spOAuth = SpotifyOAuth(
            client_id = CLIENT_ID, 
            client_secret = CLIENT_SECRET,
            redirect_uri = REDIRECT_URI,
            scope=SCOPE,
            show_dialog=True
        )
        authURL = spOAuth.get_authorize_url()
        return None, authURL
    return True, "http://127.0.0.1:3000/profile"

def getCurrentUserService(token):
    sp = spotipy.Spotify(auth=token)
    return sp.current_user()

def getTopSongsService(token): 
    t = defaultdict(list)
    orderedTracks = []
    sp = spotipy.Spotify(auth=token)
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
    
def getGenresService(token, artists):
    artistDict = {}
    sp = spotipy.Spotify(auth=token)
    artistsRes = sp.artists(artists)
    for a in artistsRes['artists']:
        artistDict[a['id']]=({
            'name': a['name'],
            'genres': a['genres']
        })
    return artistDict

def getPlaylistsService(token):
    playlists = []
    sp = spotipy.Spotify(auth=token)
    req = sp.current_user_playlists()
    for playlist in req['items']:
        playlists.append({
            'id': playlist['id'],
            'name': playlist['name'],
            'total': playlist['tracks']['total']
        })
    return playlists

def getPlaylistService(token, playlistId):
    t = defaultdict(list)
    orderedTracks = []
    sp = spotipy.Spotify(auth=token)
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