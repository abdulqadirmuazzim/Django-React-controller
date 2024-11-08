import React from 'react'
import {render} from 'react-dom'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import Landing from './Landing'



function App() {
  return (
   <Router>
      <Routes>
        <Route path="/*" element={<Landing />} />
      </Routes>
    </Router>
  )
}

const appDiv = document.getElementById("app")

render(<App/>, appDiv)

export default App