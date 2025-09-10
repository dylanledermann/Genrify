'use client'

import { useContext } from "react";
import SongCard from "./SongCard";
import { PlaylistContext } from "@/app/contexts/PlaylistContext";

type Props = {
    playlist: String[][],
    playlistName: string
}

const PlaylistCard = () => {
    const playlistContext = useContext(PlaylistContext);
    return(
        <div className="lg:col-span-1 col-span-2 flex flex-col p-3 bg-secondary rounded-lg">
            <div className="text-center w-full">
                <div className="text-xl">
                    {playlistContext?.genre || playlistContext?.playlistName}
                </div>
                <div className="flex p-5 justify-around text-tertiary">
                    <div>#</div>
                    <div className="w-full">Title</div>
                    <div className="w-full">Artist</div>
                </div>
                <div className="h-140 overflow-scroll">
                    {playlistContext?.genreList && playlistContext?.genreList.map((track: String[], index: number) => (
                        <SongCard key={index} number={index+1} artist={track[1]} track={track[3]} />
                    ))}
                    {!playlistContext?.genreList && playlistContext?.playlist.map((track: String[], index: number) => (
                        <SongCard key={index} number={index+1} artist={track[1]} track={track[3]} />
                    ))}
                </div>
            </div>
        </div>
    )
};

export default PlaylistCard