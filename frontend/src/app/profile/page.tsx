import PlaylistInfo from "@/components/PlaylistInfo";
import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { redirect } from "next/navigation";


export default async function Profile({
    searchParams,
  }: {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
  }) {
    const params = await searchParams;
    const getProfile = async () => {
        const res = await fetch(BASE_URL + API_PATHS.PROFILE).then(
            res => {
                if(res.ok){
                    return res.json()
                }
                else{
                    throw new Error('Res Error');
                }
            }
        ).catch(error => console.log('An error occured'));
        return res;
    }
    const profile = await getProfile();
    if(!profile){
        redirect("/");
    }
    return (
        <div className="mx-5">
            <div className="text-2xl pb-5">
                Welcome Back, {profile?.userProfile?.display_name}
            </div>
            <PlaylistInfo search={params}/>
        </div>
    )
}