'use client'
import { useContext } from "react";
import GenresPieChart from "./GenresPieChart";
import { PlaylistContext } from "@/app/contexts/PlaylistContext";
import { artistsGenres, artistsTracks } from "@/utils/types";

type Props = {
    genres: artistsGenres,
    songs: artistsTracks
}

const GenreCard = ({genres, songs}:  Props) => {
    const playlistContext = useContext(PlaylistContext);
    const sortGenres = () => {
        const genreCounts = new Map<string, number>();
        if(!genreCounts){
            return [];
        }
        if(genres === null || genres === undefined){
            return [];
        }
        Object.keys(genres).forEach((artist: string) => {
            genres[artist].genres.forEach((genre: string) => {
                if(genreCounts.has(genre)){
                    const count = genreCounts.get(genre) || 0;
                    genreCounts.set(genre, count+songs[artist].length);
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
        const t: string[][] = [];
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