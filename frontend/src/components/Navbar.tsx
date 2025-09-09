import { BASE_URL, API_PATHS } from "@/utils/apiPaths";


const Navbar = async () => {

    const handleLogin = async () => {
        
        try{
            const data = await fetch(BASE_URL + API_PATHS.LOGIN).then(res => res.json());
            return data.redirect;
        } catch(error) {
            console.log('Error occured: ', error);
            return "";
        }
    }
    const link = await handleLogin();

    return (
        <div className='w-full'>
            <div className='flex justify-between mx-5 mb-5 p-3 border-b-2 border-tertiary'>
                <a className='text-4xl text-button self-center' href='/'>
                    Genrify
                </a>
                <a className='btn-primary text-xl text-center' href={link}>
                    Login
                </a>
            </div>
        </div>
    )
}

export default Navbar