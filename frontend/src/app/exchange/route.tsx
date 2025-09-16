'use server'

import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { cookies } from "next/headers";
import { NextResponse } from "next/server";



export async function GET(request: { url: string | URL; }) {
    const { searchParams } = new URL(request.url)
    const token = searchParams.get('token');
    const error = searchParams.get('error');

    if(error){
        console.error('Error occured: ', error);
        return NextResponse.redirect('/', {status:302});
    }

    if(token){
        const response = await fetch(BASE_URL + API_PATHS.EXCHANGE_TOKEN, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({token})
        }).then(res => res.json()).catch(error => console.error('Error occured: ', error));
        const sessionID = response.sessionID;
        const cookieStore = await cookies();
        cookieStore.set('sessionID', sessionID, {
            httpOnly: true,
            secure: true,
            maxAge: 60 * 60 * 24
        });
        return NextResponse.redirect('/profile', {status:302});
    }
    return NextResponse.redirect('/', {status:302});
}