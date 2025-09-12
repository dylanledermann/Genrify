'use server'

import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { cookies } from "next/headers"
import { redirect } from "next/navigation";

export default async function logout(){
    const cookieStore = await cookies();
    const token = cookieStore.get('sessionID')?.value ?? '';
    cookieStore.delete('sessionID');

    await fetch(BASE_URL + API_PATHS.LOGOUT, {
        headers: {
            Cookie: token,
        }
    }).catch(error => console.error('Error occured: ', error));

    redirect('/');

    return {'message': 'success'};
}