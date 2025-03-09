import React, {Component, useState} from 'react'
import { Grid, Typography, Card, IconButton, LinearProgress } from '@mui/material'
import PauseIcon from '@mui/icons-material/Pause';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';

function Player({imgUrl, title, artist, time, duration, is_playing, current_votes, required_votes}) {

    const csrfToken = document.cookie.split("; ").find(token => token.startsWith("csrftoken="))?.split("=")[1]

    // request params
    var params = {
        method: "PUT",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken}
    }

    const playSong = () =>{
        fetch("/spotify/play", params)
    }

    const pauseSong = () =>{
        fetch("/spotify/pause", params)
    }

    const skipSong = () => {
        params = {
            method: "POST",
            headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken}
        }
        fetch("/spotify/skip", params)
    }

  return (
    <Card>
        <Grid container alignItems="center">
            <Grid Item align="center" xs={4}>
                <img src={imgUrl} height="100%" width="100%" />
            </Grid>
            <Grid item align="center" xs={8}>
                <Typography component="h5" variant="h5">
                    {title}
                </Typography>

                <Typography color="textSecondary" component="h5" variant="h5">
                    {artist}
                </Typography>

                <div>
                    <IconButton onClick={() => {is_playing ? pauseSong() : playSong()}}>
                        {is_playing ? <PauseIcon /> : <PlayArrowIcon />}
                    </IconButton>
                    <IconButton>
                        <SkipNextIcon onClick={()=>skipSong()} /> 
                    </IconButton> {"Votes to skip song:"} {current_votes} / {required_votes}
                </div>
            </Grid>
        </Grid>
        {/* <LinearProgress color="secondary" variant="determinant" value={(time/duration) * 100} /> */}
        <div className='w-100' style={{"height": "7px", "backgroundColor": "aliceblue"}}>
            <div className='h-100' style={{"width": `${(time/duration) * 100}%`, "backgroundColor": "blueviolet"}}/> 
        </div>
    </Card>
  )
}

export default Player