import Navbar from "@/components/Navbar";
import PlaylistInfo from "@/components/PlaylistInfo";
import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { profileRes } from "@/utils/types";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";


export default async function Profile({
    searchParams,
  }: {
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>
  }) {
    const params = await searchParams;
    const cookieStore = await cookies();
    const token = cookieStore.get('sessionID')?.value ?? '';
    const getProfile = async () => {
        const res = await fetch(BASE_URL + API_PATHS.PROFILE, {
            headers: {
                Cookie: token,
            },
            credentials: 'include',
        }).then(
            res => {
                if(res.ok){
                    return res.json();
                }
                else{
                    throw new Error('Res Error');
                }
            }
        ).catch(error => console.log('An error occured', error));
        if(res?.profilePicture.length === 0){
            res.profilePicture = res.userProfile[0].toUpperCase();
        }
        return res;
    }
    const profile: profileRes = await getProfile();
    if(!profile){
        redirect("/");
    }
    return (
        <>
            <Navbar/>
            <div className="mx-5">
                <div className="text-2xl pb-5">
                    Welcome Back, {profile?.userProfile}
                </div>
                <PlaylistInfo search={params}/>
            </div>
        </>
    )
}