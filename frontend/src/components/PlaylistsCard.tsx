import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { playlistsRes } from "@/utils/types";
import Link from "next/link";


const PlaylistsCard = async () => {
    const getPlaylists = async () => {
        const res = await fetch(BASE_URL + API_PATHS.GET_PLAYLISTS).then(
            res => {
                if(res.ok){
                    return res.json()
                }
                else{
                    throw new Error('Res Error');
                }
            }
        ).catch(error => console.log('An error occured', error));
        return res.playlists;
    }

    const Playlists: playlistsRes[] = await getPlaylists();

    return (
        <div className="col-span-2 lg:col-span-1 p-3 text-center bg-secondary rounded-lg">
            <div className="text-xl">
            Recent Playlists
            </div>
            <div className="flex text-tertiary m-2">
                    <div className="w-full self-center ">Playlist</div>
                    <div className="w-fit p-2 self-center ">tracks</div>
                </div>
                <div className="h-220 overflow-scroll">
                    {Playlists.map((obj: {id:string, name:string, total:number}, index: number) => (
                        <Link key={index} className="hover:cursor-pointer" href={`/profile?search=${obj.id}`}>
                            <div className="flex bg-tertiary rounded-lg p-2 m-2">
                                <div className="w-full self-center">{obj.name}</div>
                                <div className="w-fit mx-2 px-2 self-center">{obj.total}</div>
                            </div>
                        </Link>
                    ))}
                </div>
        </div>
    );
};

export default PlaylistsCard