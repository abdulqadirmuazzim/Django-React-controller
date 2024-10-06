import React from 'react'
import {render} from 'react-dom'
import HomePage from './HomePage'



function App() {
  return (
  <div>
    <HomePage/>
  </div>
  )
}

const appDiv = document.getElementById("app")

render(<App/>, appDiv)

export default App