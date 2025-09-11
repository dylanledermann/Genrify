import { API_PATHS, BASE_URL } from '@/utils/apiPaths'
import GenreCard from './GenreCard'
import PlaylistCard from './PlaylistCard'
import PlaylistsCard from './PlaylistsCard'
import { redirect } from 'next/navigation'
import PlaylistProvider from '@/app/contexts/PlaylistContext'
import { playlistRes } from '@/utils/types'

type Props = {
   search: {
        [key: string]: string | string[] | undefined;
    }
}

const PlaylistInfo = async ({search}: Props) => {
    
    const getSongs = async () => {
        let query: string | string[] | undefined = ''
        if(search && 'search' in search){
            query=search['search'];
        }
        const res = await fetch(BASE_URL + API_PATHS.GET_PLAYLIST + '?q=' + query)
            .then(
                res => {
                    if(res.ok){
                        return res.json()
                    }
                    else{
                        throw new Error('Res Error');
                    }
                }
            ).catch(error => console.log('An error occured', error));
        return res;
    }

    const topSongs: playlistRes = await getSongs();
    const artistsGenres = topSongs?.artistsGenres;
    const tracks = topSongs?.tracks;
    const artistsTracks = topSongs?.artistsTracks;
    if(!topSongs){
        redirect('/');
    }
    return (
        <div className='grid grid-cols-2 lg:grid-cols-4 gap-3 justify-around'>
            <PlaylistProvider name={topSongs?.playlist} list={tracks}>
                <PlaylistsCard/>
                <GenreCard genres = {artistsGenres} songs = {artistsTracks}/>
                <PlaylistCard/>
            </PlaylistProvider>
        </div>
    )
}

export default PlaylistInfo