'use client'

import logout from "@/app/serverActions/logout";


const LogoutButton = () => {
    return (
        <button className="btn-primary text-xl text-center" onClick={logout}>Logout</button>
    )
}

export default LogoutButton