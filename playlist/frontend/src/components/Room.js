import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

function Room() {
    const { roomcode } = useParams()
    const [room, setRoomInfo] = useState({
      votesToSkip : 2,
      guestCanPause : false,
      isHost : false
    })

    useEffect(()=>{
        fetch(`/apis/get-room?code=${roomcode}`).then((res) => res.json()).then((data) => {
          setRoomInfo({
            votesToSkip: data.votes_skip,
            guestCanPause: data.guest_pause,
            isHost: data.is_host
          })
        }).catch(err=>console.log(err))
      }, [roomcode])
    
  return (
    
    <div>
        <p> {roomcode} </p>
        <p>Votes: {room.votesToSkip}</p>
        <p>Guest can pause: {room.guestCanPause? "Yes": "No"}</p>
        <p>Host: {room.isHost? "Yes": "No"}</p>
    </div>
  )
}

export default Room