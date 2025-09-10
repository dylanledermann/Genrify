import { BASE_URL, API_PATHS } from "@/utils/apiPaths";
import LogoutButton from "./LogoutButton";


const Navbar = async () => {

    const handleLogin = async () => {
        try{
            const data = await fetch(BASE_URL + API_PATHS.LOGIN).then(res => res.json());
            var pfp = '';
            if(data.auth){
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
                if(res?.profilePicture.length === 0){
                    res.profilePicture = res.userProfile[0].toUpperCase();
                }
                pfp = res.profilePicture;
            }
            return [pfp, data.auth, data.redirect];
        } catch(error) {
            console.log('Error occured: ', error);
            return [false, ''];
        }
    }
    const [pfp, auth, redirect] = await handleLogin();
    return (
        <div className='w-full'>
            <div className='flex justify-between mx-5 mb-5 p-3 border-b-2 border-tertiary'>
                <a className='text-4xl text-button self-center' href='/'>
                    Genrify
                </a>
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