import React, {Component} from 'react'
import {BrowserRouter as Router, Route, Routes, Link, redirect} from 'react-router-dom'
import RoomJoin from './RoomJoin'
import CreateRoom from './CreateRoom'
import Room from "./Room"
// import "bootstrap/dist/css/bootstrap.css"

function HomePage() {
  return (
    <Router>
      <Routes>

        {/* Home Page here */}
        <Route exact path="/" element={<p>This is the home page</p>} />
        {/* Join page here */}
        <Route path="/join" element={<RoomJoin/>} />
        {/* Create room page here */}
        <Route path="/create" element={<CreateRoom/>} />
        {/* Room page here */}
        <Route path="/room/:roomcode" element={<Room/>} />

      </Routes>
    </Router>
  )
}

export default HomePage