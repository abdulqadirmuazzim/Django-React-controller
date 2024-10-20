import React, { useState } from 'react'
import { TextField, Button, Grid, Typography } from '@mui/material'
import { Link, useNavigate } from 'react-router-dom'

function RoomJoin() {
  const [textInfo, setText] = useState({
    roomCode: "",
    error: ""
  })

  const handleTextChange = (e) =>{
    setText({roomCode: e.target.value})
  }

  let history = useNavigate();

  const handleJoinRoom = () => {
      const Params = {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        code: textInfo.roomCode,
      })
    }
    fetch("/apis/join-room", Params).then((res)=>{
      res.ok ? history("/room/" + textInfo.roomCode) : setText({error: "Invalid Code"})
    }).catch(err=>console.log(err))

    setText({roomCode: ""})
  }

  return (
    <Grid container spacing={1 } align="center">
      <Grid item xs={12}>
        <Typography variant="h4" component="h4">
          Join a Room
        </Typography>
      </Grid>
      <Grid item xs={12}>
      <TextField
      error={textInfo.error && true}
      label="Code"
      placeholder='Enter a Room Code'
      value={ textInfo.roomCode }
      helperText={ textInfo.error }
      variant='outlined'
      onChange={handleTextChange}
       />
      </Grid>
      <Grid item xs={12} align="center">
        <Button variant='contained' color="secondary" onClick={handleJoinRoom} >Join Room</Button>
      </Grid>

      <Grid item xs={12} align="center">
        <Button variant='contained' color="primary" to='/' component={Link}>Back</Button>
      </Grid>
    </Grid>
  )
}

export default RoomJoin