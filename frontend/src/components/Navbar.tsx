import { BASE_URL, API_PATHS } from "@/utils/apiPaths";
import LogoutButton from "./LogoutButton";
import Link from "next/link";
import { cookies } from "next/headers";

const Navbar = async () => {

    const handleLogin = async () => {
        const cookieStore = await cookies();
        const token = cookieStore.get('sessionID')?.value ?? '';
        const authRes = await fetch(BASE_URL + API_PATHS.LOGIN, {
            headers: {
                Cookie: token
            }
        })
            .then(res => res.json())
            .catch(error => console.error("Error occured: ", error))
        let redirect = authRes.redirect;
        const auth = authRes.auth;
        let pfp = null;
        if(auth){
            const profRes = await fetch(BASE_URL + API_PATHS.PROFILE, {
                headers: {
                    Cookie: token
                }
            })
            .then(res => res.json())
            .catch(error => console.error('Error occured: ', error))
            pfp = profRes.profilePicture.length > 0 ? profRes.profilePicture[0] : profRes.userProfile[0].toUpperCase();
            redirect = '/profile'
        }
        
        return [pfp, auth, redirect]
    }
    const [pfp, auth, redirect] = await handleLogin();
    return (
        <div className='w-full'>
            <div className='flex justify-between mx-5 mb-5 p-3 border-b-2 border-tertiary'>
                <Link className='text-4xl text-button self-center' href='/'>
                    Genrify
                </Link>
                {!auth && <a className='btn-primary text-xl text-center' href={redirect}>Login</a>}
                {auth && (
                    <div className='flex'>
                        <div className="flex self-center justify-center w-[44px] h-[44px] rounded-full text-primary text-xl p-2 mr-2 bg-button cursor-pointer hover:bg-tertiary">
                            <a className='flex self-center' href={redirect}>{pfp}</a>
                        </div>
                        <LogoutButton/>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Navbar