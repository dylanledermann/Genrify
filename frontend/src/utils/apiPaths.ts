export const BASE_URL = 'http://localhost:5000';

export const API_PATHS = {
    LOGIN: '/api/login', // Redirects to Spotify login page if the user is not logged in
    LOGOUT: '/api/logout', // Logs user out of the Spotify API
    PROFILE: '/api/profile', // User profile
    GET_PLAYLIST: '/api/playlist', // Gets a playlist if given the id, otherwise gets the top songs
    GET_PLAYLISTS: '/api/playlists', // Gets user's 50 most recent playlists
}