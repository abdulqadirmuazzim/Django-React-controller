import React, {useEffect} from 'react'
import {Route, Routes, useNavigate} from 'react-router-dom'
import RoomJoin from './RoomJoin'
import CreateRoom from './CreateRoom'
import Room from "./Room"
import Home from './Home'
import UpdateRoom from './UpdateRoom'
import { useState } from 'react'


function HomePage() {
  
  const [isroom, setIsroom] = useState({
    room: null
  })
  const navigate = useNavigate()
  
  useEffect(()=>{
    fetch("/apis/user-in-room")
    .then((res) =>{
      if (!res.ok){
        setIsroom({room: null})
      }else{
        return res.json()
      }
    })
    .then(data=>{
      setIsroom({room: data.code})
      console.log("Data set")
    })
    .catch(err=>console.log(err))
  },
  [])

  const leaveRoom = ()=>{
        const Params = {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
    }
    fetch("/apis/leave-room", Params).then(() =>{ 
      setIsroom({room:null})
      console.log("Room closed", isroom)
      navigate("/")
    })

    
  }
  
  return (
    <div>
      <Routes>
        
        {/* Home Page here */}
        <Route exact path="/" element={<Home room={isroom.room} />} />
        {/* Join page here */}
        <Route path="/join" element={<RoomJoin/>} />
        {/* Create room page here */}
        <Route path="/create" element={<CreateRoom/>} />
        {/* Room page here */}
        <Route path="/room/:roomcode" element={<Room leaveRoom={leaveRoom} />} />
        {/* Update room page here */}
        <Route path="/update-room/:roomcode" element={<UpdateRoom />} />
        
      </Routes>
    </div>
  )
}

export default HomePage