// WebSocket connection and event handlers
import { updateUI } from "./gameState.js";
import { showSplashScreen } from "./screens/index.js";

// Connect to WebSocket server
const socket = io("http://localhost:6969");

// Connection event handlers
socket.on("connect", () => {
  console.log("Connected to server");
  // Request initial game state when connected
  socket.emit("request_game_state");
});

socket.on("disconnect", () => {
  console.log("Disconnected from server");
  showSplashScreen("Disconnected from server");
});

// Game state update handlers
socket.on("game_state_update", (gameState) => {
  console.log(
    "Game state update received:",
    JSON.stringify(gameState, null, 2)
  );
  console.log("Game phase from update:", gameState.game_phase);
  console.log("Status message:", gameState.status_message);
  updateUI(gameState);
});

socket.on("score_update", (data) => {
  console.log("Score update received:", data);
  document.getElementById(`player${data.player_id}_score`).textContent =
    data.score;
});

socket.on("cp_update", (data) => {
  console.log("CP update received:", data);
  document.getElementById(
    `player${data.player_id}_cp`
  ).textContent = `Command Points: ${data.cp}`;
});

socket.on("timer_update", (timerData) => {
  console.log("Timer update received:", timerData);
  // Update player timers
  document.getElementById("player1_time").textContent =
    timerData.player1_time || "00:00:00";
  document.getElementById("player2_time").textContent =
    timerData.player2_time || "00:00:00";
  document.getElementById("total_time").textContent = `Total Time: ${
    timerData.elapsed_display || "00:00:00"
  }`;
});

socket.on("round_update", (data) => {
  console.log("Round update received:", data);
  document.getElementById("round").textContent = `Round ${data.round}`;
});

socket.on("game_phase_update", (data) => {
  console.log("Game phase update received:", data);
  console.log("New phase:", data.phase);
  // When the phase changes, request a full game state update
  // to ensure the client has the most consistent and up-to-date information.
  socket.emit("request_game_state");
});

export { socket };
