'use client'
import { useContext } from "react";
import GenresPieChart from "./GenresPieChart";
import { PlaylistContext } from "@/app/contexts/PlaylistContext";

type Props = {
    genres: any,
    songs: any,
    tracks: any
}

const GenreCard = ({genres, songs, tracks}:  Props) => {
    const playlistContext = useContext(PlaylistContext);
    const sortGenres = () => {
        const genreCounts = new Map()
        if(genres === null || genres === undefined){
            return [];
        }
        Object.keys(genres).forEach((artist: string) => {
            genres[artist].genres.forEach((genre: string[]) => {
                if(genreCounts.has(genre)){
                    genreCounts.set(genre, genreCounts.get(genre)+songs[artist].length);
                }
                else{
                    genreCounts.set(genre, songs[artist].length);
                }
            })
        })
        return Array.from(genreCounts.entries());
    }
    const callback = async (genre: string | null) => {
        if(!genre){
            playlistContext?.setG();
            return;
        }
        var t: string[][] = [];
        Object.keys(genres).forEach((artist) => {
            genres[artist].genres.forEach((g: string) => {
                if(g === genre){
                    songs[artist].forEach((obj: {id: string, name: string}) => {
                        t.push([artist, genres[artist].name, obj.id, obj.name])
                    })
                }
            })
        });
        playlistContext?.setG(genre, t);
    }
    const genreCounts = sortGenres();
    return (
        <div className="w-full col-span-2 p-3 mr-5 bg-secondary rounded-lg">
            <div className="text-center text-xl">
                Genres
            </div>
            <GenresPieChart genres={genreCounts} callback={callback}/>
        </div>
    );
};

export default GenreCard;