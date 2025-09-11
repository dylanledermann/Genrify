export type profileRes = {
    userProfile: string,
    profilePicture: string
};

export type artistsTracks = {
    [artistId: string]: {
        'id': string,
        'name': string
    }[]
};

export type artistsGenres = {
    [artistId: string]: {
        'name': string,
        'genres': string[]
    }
}

export type playlistRes = {
    'playlist': string,
    'tracks': string[][],
    'artistsTracks': artistsTracks,
    'artistsGenres': artistsGenres
};

export type playlistsRes = {
    id: string,
    name: string,
    total: number
};