import os, collections, spotipy, time

from spotipy.oauth2 import SpotifyOAuth

# 1 1 1.2658711099647917
# 1 1 0.6618555770255625 removed enumerate

# Function to get selected genre and track IDs from Saved Albums
def tracksFromSavedAlbums():
    startTime = time.perf_counter()
    # Get Album IDs and Artist IDs from Saved Albums
    albumIds = []
    artistsIds = []
    saved_albums = spotify.current_user_saved_albums(limit=50, offset=0, market=None)
    for album in saved_albums['items']:
        albumIds.append(album['album']['id'])
        artistsIds.append(album['album']['artists'][0]['id'])
    
    # Get Genres from list of Artist IDs
    # Create list of Album Genres corresponding to Artist ID list
    # Also create overall list of Album Genres
    albumGenreList = []
    albumGenres = []
    for artistId in artistsIds:
        genreList = []
        artistData = spotify.artist(artistId)
        for item in (artistData['genres']):
            genreList.append(item)
            albumGenres.append(item)
        albumGenreList.append(genreList)

    # Sort and count overall list of Genres
    # Present list to choose Selected Genre from
    collection = collections.Counter(albumGenres)
    sortedAlbumGenres = collection.most_common(20)
    os.system('clear')
    print('Top 20 Genres from 50 most recent Saved Albums: ')
    print("")
    i = 1
    for genre in sortedAlbumGenres:
        print(f'{i}. {genre[0]} ({genre[1]} albums)')
        i+=1
    print("")
    print("Select Genre:")

    tBefore = time.perf_counter()

    selection = int((input()))-1

    tSelection = time.perf_counter() - tBefore

    selectedGenre = sortedAlbumGenres[selection][0]

    # Go through Album Genre list and add to
    # Selected Album IDs if Selected Genre is matched
    selectedAlbumIds = []
    i = 0
    for genre in albumGenreList:
        if selectedGenre in genre:
            selectedAlbumIds.append(albumIds[i])
        i+=1
    selectedArtists = []
    selectedTrackIds = []
    selectedTrackNames = []
    albumData = spotify.albums(selectedAlbumIds)
    for album in albumData['albums']:
        for track in album['tracks']['items']:
            selectedArtists.append(track['artists'][0]['name'])
            selectedTrackIds.append(track['id'])
            selectedTrackNames.append(track['name'])
    
    # Print total number of selected tracks
    os.system('clear')
    print(f'Time taken: { (time.perf_counter() - startTime - tSelection) }')
    print(f"{len(selectedTrackNames)} tracks to add for selected genre: {selectedGenre}")
    print("")

    return selectedGenre, selectedTrackIds, selectedTrackNames

# 2 1 1 Time taken: 0.9252715329930652
# 2 1 1 0.7895185029774439 removed enumerate
# Function to get Selected Genre and Track IDs from selected playlist
def tracksFromPlaylists():
    
    startTime = time.perf_counter()

    # Get list of playlists
    playlists = spotify.current_user_playlists()

    # Retrieve and store Playlist information
    playlistIds = []
    playlistNames = []
    playlistTotals = []
    for playlist in playlists['items']:
        playlistIds.append(playlist['id'])
        playlistNames.append(playlist['name'])
        playlistTotals.append(playlist['tracks']['total'])

    # Present user with available Playlist information
    os.system('clear')
    print('Available Playlists: ')
    print('')
    i = 0
    while i < len(playlistIds):
        print(f'{i+1}. {playlistNames[i]} ({playlistTotals[i]} tracks)')
        i+=1

    # Allow user to choose a Playlist for processing adn get track info from Playlist
    print("")
    print('Select Playlist:')

    tBefore = time.perf_counter()

    selection = int(input())-1

    tSelection = time.perf_counter() - tBefore

    selectedPlaylistId = playlistIds[selection]
    results = spotify.playlist(selectedPlaylistId, fields=None, market=None, additional_types=('track',))
    
    #Retrieve and store info on tracks from Playlist
    tracks = []
    trackIds = []
    artists = []
    artistIds = []
    for idx, item in enumerate(results['tracks']['items']):
        track = item['track']
        tracks.insert(idx, track['name'])
        trackIds.insert(idx, track['id'])
        artists.insert(idx, track['artists'][0]['name'])
        artistIds.insert(idx, track['artists'][0]['id'])
    
    # Get all genres for each artist in Playlist and store for processing
    genres = []
    playlistGenres = []
    i = 0
    for artistId in artistIds:
        genreList = []
        artistData = spotify.artist(artistId)
        for item in artistData['genres']:
            genreList.append(item)
            playlistGenres.append(item)
        genres.append(genreList)
        i+=1
    
    # Sort Playlist genres into most common
    c = collections.Counter(playlistGenres)
    sortedPlaylistGenres = c.most_common(20)

    # Present user with list of the 20 most common genres
    os.system('clear')
    print("Available Genres from Playlist: ")
    print("")
    i = 1
    for genre in sortedPlaylistGenres:
        print(f'{i}. {genre[0]} ({genre[1]} tracks)')
        i+=1
    
    # Allow user to choose a genre
    print("")
    print("Select genre:")

    tBefore = time.perf_counter()

    selection = int(input())-1

    tSelection += time.perf_counter() - tBefore

    print('')
    selectedGenre = sortedPlaylistGenres[selection][0]

    # Loop through all tracks in Playlist and store track
    # when selected genre matches the genre and associated with that track
    # (previously determined from the genre of the artist for that track)
    selectedTrackIds = []
    selectedTrackNames = []
    i = 0
    for genre in genres:
        if selectedGenre in genre:
            selectedTrackIds.append(trackIds[i])
            selectedTrackNames.append(tracks[i])
        i+=1
    
    # Print total number of selected tracks
    os.system('clear')
    print(f'Time taken: { (time.perf_counter()-startTime-tSelection) }')
    print(f'{len(selectedTrackNames)} tracks to add for selected genre: {selectedGenre}')
    print("")
    
    return selectedGenre, selectedTrackIds, selectedTrackNames

# 2 1 1 2 0.4597642839944456

# Function to create a playlist given the genre and track IDs
def createPlaylist(selectedGenre, selectedTrackIds):

    startTime = time.perf_counter()

    # Create Playlist and get Playlist ID
    playlistName = "[Genrify]" + selectedGenre
    playlistDescription = "Playlist automatically created for genre " + selectedGenre + " by Genrify."
    me = spotify.current_user()['id']
    playlistData = spotify.user_playlist_create(me, playlistName, public=False, collaborative=False, description=playlistDescription)
    playlistId = playlistData['id']

    # Add selected Track IDs to Playlist
    # (removing old tracks if present via 'replace')
    spotify.playlist_replace_items(playlistId, selectedTrackIds)

    print("")
    print(f'Time Taken: { (time.perf_counter() - startTime) }')
    print(f'Playlist {playlistName} created and {len(selectedTrackIds)} tracks added')

# 1 1 0.9180544260016177
# 

# Function to add to Queue
def addToQueue(selectedGenre, selectedTrackIds, selectedTrackNames):
    
    startTime = time.perf_counter()

    print("")
    print(f'Adding {len(selectedTrackIds)} {selectedGenre} tracks to Queue')
    print("")

    # Add tracks to Queue
    for trackId in selectedTrackIds:
        spotify.add_to_queue(trackId, device_id=None)

    print(f'Time Taken: { (time.perf_counter() - startTime) }')

# Spotify authorization scopes
scope = 'user-library-read playlist-read-private user-read-playback-position user-top-read user-read-recently-played playlist-read-collaborative'

# Initiate spotipy library
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Clear screen
os.system('clear')

# Select from either Saed Albums or a Playlist
print("1. Select from Saved Albums")
print("2. Select from a Playlist")
print("")
print("Choose 1 or 2:")
selection = '0'
while selection != "1" and selection != '2':
    selection = input()
if selection == "1":
    selectedGenre, selectedTrackIds, selectedTrackNames = tracksFromSavedAlbums()
elif selection == "2":
    selectedGenre, selectedTrackIds, selectedTrackNames = tracksFromPlaylists()

# Create a Playlist or add to Queue
# Limit number of tracks to 100 so as to not exceed Spotify API limit
print("1. Add to Queue")
print("2. Create Playlist")
print("")
print("Choose 1 or 2:")
selection = '0'
while selection != "1" and selection != '2':
    selection = input()
if selection == "1":
    addToQueue(selectedGenre, selectedTrackIds, selectedTrackNames)
elif selection == "2":
    createPlaylist(selectedGenre[:100], selectedTrackIds[:100])