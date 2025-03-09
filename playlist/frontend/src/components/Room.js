import React, { useEffect, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import {Grid, Button, Typography} from "@mui/material"
import { Collapse } from "@mui/material"
import Player from './Player'


function Room(props) {
    const { roomcode } = useParams()
    const [room, setRoomInfo] = useState({
      votesToSkip : 2,
      guestCanPause : false,
      isHost : false,
      song: {}
      })
    const [pending, setPending] = useState(true)
    const [message, setMessage] = useState("")
    const navigate = useNavigate()
    const location = useLocation()
    const [spotifyAuth, setSpotifyAuth] = useState(false)
    const [intervalId, setIntervalId] = useState(null)
    
    const csrf = document.cookie.split("; ").find(token => token.startsWith("csrftoken="))?.split("=")[1]
    const handleLeaving = ()=>{
      props.leaveRoom(csrf)
    }
    
    // spotify authentication logic
    function spotifyAuthenticate(){
      console.log("Running Authentication")
      if (room.isHost){
        fetch("/spotify/is-authenticated")
        .then(res => res.json())
        .then(data => {
          console.log(data.status)
          setSpotifyAuth(data.status)
          
          if (!data.status){
            console.log("Not authenticated")
            fetch("/spotify/get-auth-url")
            .then(res => res.json())
            .then(data=>{
              window.location.replace(data.url)
            }).catch(err => console.log(err))
          }
        })
      }
    }
    // Get the song info
    function getSong(){
        fetch("/spotify/current-song").then((res)=>{
         if (res.ok){
          return res.json()
         }else{
          navigate("/")
          return {"error" : "There was an error fetching song"}
        }
        }).then(data => {
          setRoomInfo((prevInfo) => ({...prevInfo, song: data}))
          console.log(data)
        })
    }
    // function to clear the interval
    function clear(interval){
      clearInterval(interval)
    }

    useEffect(()=>{
      // Get room details
        fetch(`/apis/get-room?code=${roomcode}`).then((res) => {
          if (!res.ok){
            navigate("/")
          } else {
            return res.json()
          }
        }).then((data) => {
          // For making the pop up message disappear
          if (location.state && location.state.message){
            setMessage(location.state.message)
            setTimeout(() => setMessage(""), 3000)
            window.history.replaceState({}, document.title);
          }
          setRoomInfo({
            votesToSkip: data.votes_skip,
            guestCanPause: data.guest_pause,
            isHost: data.is_host
          })
          // After getting the room data we authenticate our user
          spotifyAuthenticate()

          // Then we set the pending to false
          setPending(false)
          // get the song info
          const interval = setInterval(() => {
            getSong()
            console.log("Song retrieved")
          }, 3000)
          roomcode && setIntervalId(interval)
        }).catch(err=>{
          console.log(err)
        });

        return clear(intervalId)

      }, [room.isHost])
      

      // preloader
      if (pending){
        return (
          <div className='d-flex align-items-center justify-content-center'>
          <h1>Loading...</h1>
            <div className="spinner-grow text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        )
      }
      return (
     <Grid container spacing={1}>
          <Grid item xs={12} align="center">
            <Collapse in={message != null}>
            {message}
            </Collapse>
            <Typography variant="h4" component="h3">Code: {roomcode}</Typography>
          </Grid>

          {room.song && ( <Player imgUrl={room.song.image_url}
                title={room.song.item}
               artist={room.song.artists}
               time={room.song.time}
               duration={room.song.duration}
               is_playing={room.song.is_playing}
               current_votes={room.song.votes}
               required_votes={room.song.required_votes} />)}

          {/* Show grid button if it's the host */}
          {room.isHost && (
            <Grid item xs={12} align="center">
              <Button variant="contained" color="primary" onClick={()=>{navigate(`/update-room/${roomcode}`)}}>
                Settings
              </Button>
            </Grid>
          )}
    
          <Grid item xs={12} align="center">
            <Button variant="contained"  color="secondary" onClick={handleLeaving}>
                {room.isHost? "Close Room" : "Back"}
            </Button>
            
          </Grid>
        </Grid>
      )
    }

export default Room



          // <Grid item xs={12} align="center">
          //   <Typography variant="h5" component="h5">Votes: {room.votesToSkip}</Typography>
          // </Grid>
          // <Grid item xs={12} align="center">
          //   <Typography variant="h5" component="h5">Guest can pause: {room.guestCanPause? "Yes": "No"}</Typography>
          // </Grid>
          // <Grid item xs={12} align="center">
          //   <Typography variant="h5" component="h5">Host: {room.isHost? "Yes": "No"}</Typography>
          // </Grid>