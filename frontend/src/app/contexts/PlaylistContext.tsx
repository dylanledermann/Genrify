'use client'
import { createContext, useEffect, useState } from "react";

type playlistContext = {
    playlistName: string,
    playlist: String[][], 
    genre: string,
    genreList: String[][] | null,
    setG: (name?: string, list?: String[][] | null) => void, 
}

export const PlaylistContext = createContext<playlistContext | undefined>(undefined);

const PlaylistProvider = ({children, name, list}: {children: React.ReactNode, name: string, list: String[][]}) => {
    const [playlistName, setPlaylistName] = useState(name);
    const [playlist, setPlaylist] = useState<String[][]>(list);
    const [genre, setGenre] = useState('')
    const [genreList, setGenreList] = useState<String[][] | null>(null);
    
    useEffect(() => {
        setPlaylistName(name);
    }, [name]);

    useEffect(() => {
        setPlaylist(list);
    }, [list]);

    const setG = (name: string='', list: String[][] | null=null) => {
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