import React, {Component} from 'react'
import {BrowserRouter as Router, Route, Routes, Link, redirect} from 'react-router-dom'
import RoomJoin from './RoomJoin'
import CreateRoom from './CreateRoom'

function HomePage() {
  return (
    <Router>
      <Routes>

        {/* Home Page here */}
        <Route exact path="/" element={<p>This is the home page</p>} />
        {/* Join page here */}
        <Route path="/join" element={<RoomJoin/>} />
        {/* Create page here */}
        <Route path="/create" element={<CreateRoom/>} />

      </Routes>
    </Router>
  )
}

export default HomePage