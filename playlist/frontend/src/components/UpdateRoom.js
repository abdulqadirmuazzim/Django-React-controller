import React, { useState, useEffect } from 'react'
import {useParams, useNavigate} from "react-router-dom"
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, FormControlLabel, Radio, RadioGroup} from '@mui/material'


function UpdateRoom() {

  const { roomcode }  = useParams()
    
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
  
  const handleVotesChange = (e) =>{
    setState((prevState) => ({
      ...prevState,
      votesToSkip: e.target.value
    }))
  }

  const handleGuestPause = (e) =>{
    setState({
      guestCanPause: e.target.value === "true" ? true: false,
      votesToSkip: state.votesToSkip
    });
    console.log(e.target.value)
    console.log(state.guestCanPause)

  }

  const history = useNavigate();

  const handleButtonClicked = ()=>{
    const Params = {
      method: "PATCH",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        votes_skip: state.votesToSkip,
        guest_pause: state.guestCanPause,
        code: roomcode
      })
    }
    fetch("/apis/update-room", Params).then((res)=>res.json()).then(data=>{
      history(`/room/${data.code}`)
      console.log(data)
    }).catch(err=>console.log(err))
  }
    if (isPending){
      return (
        <h1>Loading...</h1>
      )
    }else{

    return (
    <> 
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant='h4'>
          Update Room
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        {/* Form */}
        <FormControl components="fieldset">
          {/* Form text */}
          <FormHelperText>
            <div> Guest control of playback state</div>
          </FormHelperText>

            <RadioGroup row defaultValue={state.guestCanPause ? "true": "false"} onChange={handleGuestPause}>
              <FormControlLabel
               value="true"
               control={<Radio color="primary" />}
               label="play/pause"
               labelPlacement="bottom" />

              <FormControlLabel
               value="false" 
               control={<Radio color="secondary" />}
               label="no control"
               labelPlacement="bottom" />
            </RadioGroup>

        </FormControl>
      </Grid>

      <Grid item xs={12} align="center">
      <FormControl>
        <TextField 
        required={true} 
        type="number" 
        defaultValue={state.votesToSkip} 
        inputProps={{
          min: 1,
          style: {textAlign: "center"}
          }}
          onChange={handleVotesChange}/>
        <FormHelperText>
          <div align="center">
          votes Required to skip song
          </div>
        </FormHelperText>
      </FormControl>
      </Grid>

      <Grid item xs={12} align="center">
          <Button color="secondary" variant="contained" onClick={handleButtonClicked}>Update Room</Button>
      </Grid>
        
      <Grid item xs={12} align="center">
          <Button variant="contained" color="primary" onClick={()=>{history(-1)}}>
          Close Settings
          </Button>
      </Grid>

    </Grid>
    </>
    )

    }
}

export default UpdateRoom