// WebSocket connection and event handlers
import { setGameState } from "./gameState.js";
import { setInitialState } from "./main.js";

let connectionState = "disconnected";
let isFirstUpdate = true;

// Connect to WebSocket server
const socket = io("http://localhost:6969");

function dispatchConnectionStatusEvent() {
  const event = new CustomEvent("connectionStatusChanged", {
    detail: { status: connectionState },
  });
  document.dispatchEvent(event);
}

// Connection event handlers
socket.on("connect", () => {
  console.log("Connected to server");
  connectionState = "connected";
  dispatchConnectionStatusEvent();
  // Request initial game state when connected
  socket.emit("request_game_state");
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
  connectionState = "disconnected";
  dispatchConnectionStatusEvent();
  // The main controller will handle showing the splash screen
});

// Game state update handlers
socket.on("game_state_update", (gameState) => {
  console.log(
    "Game state update received:",
    JSON.stringify(gameState, null, 2)
  );

  // Set the state first, so that the initial render has data
  setGameState(gameState);

  if (isFirstUpdate) {
    isFirstUpdate = false;
    // Now trigger the first render
    setInitialState();
  }
});

// The 'game_phase_update' is also redundant if 'game_state_update' is comprehensive.
// A full state update is better than a partial one.
socket.on("game_phase_update", (data) => {
  console.log("Game phase update received, requesting full state:", data);
  socket.emit("request_game_state");
});

export { socket };
