import React from 'react'
import { useState } from 'react'
import Button from "@mui/material/Button"
import Grid from "@mui/material/Grid"
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import FormHelperText from '@mui/material/FormHelperText'
import FormControl from '@mui/material/FormControl'
import {Link} from "react-router-dom"
import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'
import FormControlLabel from '@mui/material/FormControlLabel'

function CreateRoom() {

  const defaultVotes = 2
  const [state, setState] = useState({
    guestCanPause: true,
    votesToSkip: defaultVotes
  })

  const handleVotesChange = (e) =>{
    setState({
      guestCanPause: true,
      votesToSkip: e.target.value
    })
  }

  const handleGuestPause = (e) =>{
    setState({
      guestCanPause: e.target.value === "" && true,
    })
  }

  const handleButtonClicked = ()=>{
    const Params = {
      method: "POST",
      headers: {"Content-Type" : "application/json"},
      body: JSON.stringify({
        votes_skip: state.votesToSkip,
        guest_pause: state.guestCanPause
      })
    }
    fetch("apis/create", Params).then((res)=>res.json()).then(data=>console.log(data)).catch(err=>console.log(err))
  }
  
  return (
    <>
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant='h4'>
          Create a Room here
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        {/* Form */}
        <FormControl components="fieldset">
          {/* Form text */}
          <FormHelperText>
            <div> Guest control of playback state</div>
          </FormHelperText>

            <RadioGroup row defaultValue='true' onChange={handleGuestPause}>
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
        defaultValue={defaultVotes} 
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
            <Button color="secondary" variant="contained" onClick={handleButtonClicked}>Create A Room</Button>
          </Grid>
          <Grid item xs={12} align="center">
            <Button color="primary" variant="contained" component={Link} to="/" >Back</Button>
          </Grid>
    </Grid>
    </>
  )
}

export default CreateRoom