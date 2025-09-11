'use client'
import { createContext, useEffect, useState } from "react";

type playlistContext = {
    playlistName: string,
    playlist: string[][], 
    genre: string,
    genreList: string[][] | null,
    setG: (name?: string, list?: string[][] | null) => void, 
}

export const PlaylistContext = createContext<playlistContext | undefined>(undefined);

const PlaylistProvider = ({children, name, list}: {children: React.ReactNode, name: string, list: string[][]}) => {
    const [playlistName, setPlaylistName] = useState(name);
    const [playlist, setPlaylist] = useState<string[][]>(list);
    const [genre, setGenre] = useState('')
    const [genreList, setGenreList] = useState<string[][] | null>(null);
    
    useEffect(() => {
        setPlaylistName(name);
        setGenre('');
        setGenreList(null);
        setPlaylist(list);
    }, [name, list]);

    const setG = (name: string='', list: string[][] | null=null) => {
        setGenre(name);
        setGenreList(list);
    }

    return (
        <PlaylistContext value={{playlistName, playlist, genre, genreList, setG}}>
            {children}
        </PlaylistContext>
    )
};

export default PlaylistProvider