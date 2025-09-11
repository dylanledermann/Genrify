'use client'

import { API_PATHS, BASE_URL } from "@/utils/apiPaths";


const LogoutButton = () => {
    const handleLogout = async () => {
        try{
            await fetch(BASE_URL + API_PATHS.LOGOUT);
            window.location.href='/';
        } catch(error) {
            console.log('Error occured: ', error);
            return
        }
    }
    return (
        <button className="btn-primary text-xl text-center" onClick={handleLogout}>Logout</button>
    )
}

export default LogoutButton