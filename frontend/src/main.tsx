import React from 'react'
import ReactDOM from 'react-dom/client'
// Ensure THREE is available globally for any legacy deps that expect window.THREE
import * as THREE from 'three'
(window as any).THREE = THREE

import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
