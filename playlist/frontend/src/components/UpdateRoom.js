import React, { useState, useEffect } from 'react'
import {useParams, useNavigate} from "react-router-dom"
import { Button, Grid} from '@mui/material'
import CreateRoom from './CreateRoom'


function UpdateRoom() {

  const { roomcode }  = useParams()
  const csrf = document.cookie.split("; ").find(token => token.startsWith("csrftoken="))?.split("=")[1]

  const [state, setState] = useState({
    guestCanPause: null,
    votesToSkip: null
  })
  const [isPending, setPending] = useState(true)
  // Fetching data to be updated
  useEffect(()=>{
    fetch(`/apis/get-room?code=${roomcode}`).then((res) => {
      return res.json()
    }).then((data) => { 
      setState({
        guestCanPause: data.guest_pause,
        votesToSkip: data.votes_skip
      })
      setPending(false)
    }).catch(err=>console.log(err));
  }, [roomcode])
  


  const history = useNavigate();

  const handleButtonClicked = (e)=> {
    const Params = {
      method: "PATCH",
      headers: {"Content-Type" : "application/json", "X-CSRFToken": csrf},
      body: JSON.stringify({
        votes_skip: e.votesToSkip,
        guest_pause: e.guestCanPause,
        code: roomcode
      })
    }
    fetch("/apis/update-room", Params).then((res)=>res.json()).then(data=>{
      history(`/room/${data.code}`, {state: {message: "Room updated successfully!"}})
    }).catch(err=>console.log(err))
  }
    if (isPending){
      return (
        <h1>Loading...</h1>
      )
    }else{

    return (
      <>
      <CreateRoom votes={state.votesToSkip} guestPause={state.guestCanPause} handelSubmit={handleButtonClicked} task="Update"/>
       <Grid item xs={12} align="center" className='my-2'>
           <Button variant="contained" color="primary" onClick={()=>{history(-1)}}>
           Close Settings
           </Button>
       </Grid>
    </>
    )

    }
}

export default UpdateRoom