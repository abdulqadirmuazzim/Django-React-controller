import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {Grid, Button, Typography} from "@mui/material"

function Room(props) {
    const { roomcode } = useParams()
    const [room, setRoomInfo] = useState({
      votesToSkip : 2,
      guestCanPause : false,
      isHost : false
      })
    const navigate = useNavigate()

    useEffect(()=>{
        fetch(`/apis/get-room?code=${roomcode}`).then((res) => {
          if (!res.ok){
            navigate("/")
          } else {
            return res.json()
          }
        }).then((data) => {
          console.log(data)
          setRoomInfo({
            votesToSkip: data.votes_skip,
            guestCanPause: data.guest_pause,
            isHost: data.is_host
          })
        }).catch(err=>console.log(err));
      }, [roomcode])
  

      return (
      <>
     <Grid container spacing={1}>
          <Grid item xs={12} align="center">
            <Typography variant="h4" component="h3">Code: {roomcode}</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography variant="h5" component="h5">Votes: {room.votesToSkip}</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography variant="h5" component="h5">Guest can pause: {room.guestCanPause? "Yes": "No"}</Typography>
          </Grid>
          <Grid item xs={12} align="center">
            <Typography variant="h5" component="h5">Host: {room.isHost? "Yes": "No"}</Typography>
          </Grid>
          {/* Show grid button if it's the host */}
          {room.isHost && (
            <Grid item xs={12} align="center">
              <Button variant="contained" color="primary" onClick={()=>{navigate(`/update-room/${roomcode}`)}}>
                Settings
              </Button>
            </Grid>
          )}
    
          <Grid item xs={12} align="center">
            <Button variant="contained"  color="secondary" onClick={props.leaveRoom}>
                {room.isHost? "Close Room" : "Back"}
            </Button>
            
          </Grid>
        </Grid>
      </>
      )
    }

export default Room