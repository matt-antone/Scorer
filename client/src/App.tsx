import React, { useEffect } from 'react';
import './App.css';
import webSocketService from './services/websocket';

function App() {
  useEffect(() => {
    // Initialize the WebSocket connection when the app component mounts
    webSocketService.connect();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Scorer Client</h1>
        <p>
          Waiting for connection to server...
        </p>
      </header>
    </div>
  );
}

export default App;
