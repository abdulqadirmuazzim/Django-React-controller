import React from 'react'
import { Grid, Button, ButtonGroup, Typography } from '@mui/material'
import { Link, Navigate } from 'react-router-dom'

function Home(props) {
    console.log(props.room)
    if (props.room){
    return (<Navigate to={`/room/${props.room}`} replace={true} />)
    } else{
        
        return (
        
          <div>
              <Grid container spacing={3}>
                  <Grid item xs={12} align="center">
                      <Typography variant="h3" compact="h3">
                          House Sleep over
                      </Typography>
                  </Grid>
                  <Grid item xs={12} align="center">
                      <ButtonGroup disableElevation variant="contained" color="primary">
                          <Button color="primary" to="/join" component={Link}>Join a Room</Button>
                          <Button color="secondary" to="/create" component={Link}>Create a Room</Button>
                      </ButtonGroup>
                  </Grid>
              </Grid>
          </div>
        )
    }
}

export default Home