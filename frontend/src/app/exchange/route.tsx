'use server'

import { API_PATHS, BASE_URL } from "@/utils/apiPaths";
import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";



export async function GET(request: NextRequest) {
    const { searchParams } = new URL(request.url)
    const token = searchParams.get('token');
    const error = searchParams.get('error');
    const protocol = request.headers.get('x-forwarded-proto') || 'https';
    const host = request.headers.get('x-forwarded-host') || request.headers.get('host');
    if(error){
        const redirectUrl = `${protocol}://${host}/`;
        console.error('Error occured: ', error);
        return NextResponse.redirect(redirectUrl);
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
        const redirectUrl = `${protocol}://${host}/profile`;

        return NextResponse.redirect(redirectUrl);
    }
    const redirectUrl = `${protocol}://${host}/`;
    return NextResponse.redirect(redirectUrl);
}