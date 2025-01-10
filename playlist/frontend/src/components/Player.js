import React, {Component, useState} from 'react'
import { Grid, Typography, Card, IconButton, LinearProgress } from '@mui/material'
import PauseIcon from '@mui/icons-material/Pause';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';

function Player({imgUrl, title, artist, time, duration, is_playing}) {

    const [timeLeft, setTimeLeft] = useState(null)
    
    // const timeLeft = (time/duration) * 100
    // request params
    var params = {
        method: "PUT",
        headers: {"Content-Type": "application/json"}
    }

    const playSong = () =>{
        fetch("/spotify/play", params)
    }

    const pauseSong = () =>{
        fetch("/spotify/pause", params)
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
                        <SkipNextIcon />
                    </IconButton>
                </div>
            </Grid>
        </Grid>
        <LinearProgress color="secondary" variant="determinant" value={(time/duration) * 100} />
        <div className='w-100' style={{"height": "7px", "backgroundColor": "aliceblue"}}>
            <div className='h-100' style={{"width": `${(time/duration) * 100}%`, "backgroundColor": "blueviolet"}}/> 
        </div>
    </Card>
  )
}

export default Player