// WebSocket connection and event handlers
import { setGameState } from "./gameState.js";

let connectionState = "disconnected";

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
  setGameState(gameState);
});

// The 'game_phase_update' is also redundant if 'game_state_update' is comprehensive.
// A full state update is better than a partial one.
socket.on("game_phase_update", (data) => {
  console.log("Game phase update received, requesting full state:", data);
  socket.emit("request_game_state");
});

export { socket };
