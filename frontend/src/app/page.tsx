import Navbar from "@/components/Navbar";


export default function Home() {

  return (
    <>
      <Navbar/>
      <div className='h-full bg-secondary m-5 p-2 rounded-lg'>
        <h1 className='text-2xl pb-5'>
          Welcome to {''}
          <span className='text-transparent bg-clip-text bg-[radial-gradient(circle,_#ffffff_-25%,_#1db954_100%)] bg-[length:200%_200%] animate-text-shine'>
            Genrify
          </span>
        </h1>
        <p className="text-lg">
          This web application was built using Spotify's Web API with the Spotipy library. 
          This project was inspired and built with help from Matt Brocks <a className='text-button hover:underline' href='https://blog.cetre.co.uk/genrify-python-app-to-filter-spotify-library-based-on-genre/'>Genrify</a>.
          You can use this project to see the genres of songs in your playlist and most listened to songs.
        </p>
      </div>
    </>
  );
}
