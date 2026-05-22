import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#1A1A25',
            color: '#fff',
            border: '1px solid #2A2A3A',
            fontFamily: 'DM Sans, sans-serif'
          }
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
)
