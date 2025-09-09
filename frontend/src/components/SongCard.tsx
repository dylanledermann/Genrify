import React from 'react'
type Props = {
    number: number,
    artist: String,
    track: String
}
const SongCard = ({number, artist, track}: Props) => {
  return (
    <div className="flex bg-tertiary p-3 m-2 justify-around rounded-lg">
        <div className="mr-2 self-center">{number}</div>
        <div className="w-full">{track}</div>
        <div className="w-full self-center">{artist}</div>
    </div>
  )
}

export default SongCard