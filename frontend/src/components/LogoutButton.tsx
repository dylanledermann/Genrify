'use client'

import logout from "@/app/serverActions/logout";
import { API_PATHS, BASE_URL } from "@/utils/apiPaths";


const LogoutButton = () => {
    return (
        <button className="btn-primary text-xl text-center" onClick={logout}>Logout</button>
    )
}

export default LogoutButton