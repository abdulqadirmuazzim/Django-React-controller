import React from 'react'
import { useState } from 'react'
import { Button, Grid, Typography, TextField, FormHelperText, FormControl, FormControlLabel, Radio, RadioGroup} from '@mui/material'



function CreateRoom({votes = 2, guestPause = true, handelSubmit, task = "Create"}) {
  
  const [state, setState] = useState({
    guestCanPause: guestPause,
    votesToSkip: votes
  })
  
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

  // When user clicks the button
  const handelButtonClick = () => {
    handelSubmit(state)
  }
  

  return (
    <>
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component="h4" variant='h4'>
          {task} Room here
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        {/* Form */}
        <FormControl components="fieldset">
          {/* Form text */}
          <FormHelperText>
            <div> Guest control of playback state</div>
          </FormHelperText>

            <RadioGroup row defaultValue={guestPause ? "true": "false"} onChange={handleGuestPause}>
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
        defaultValue={votes} 
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
          <Button color="secondary" variant="contained" onClick={handelButtonClick}>{task} Room</Button>
        </Grid>
        
    </Grid>
    </>
  )
}


export default CreateRoom