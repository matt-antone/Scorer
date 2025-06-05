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
  // Update the game state with the new phase
  if (window.currentGameState) {
    window.currentGameState.game_phase = data.phase;
    updateUI(window.currentGameState);
  }
});

// Helper function to update the entire UI
function updateUI(gameState) {
  // Store the current game state
  window.currentGameState = gameState;

  console.log("Current game phase:", gameState.game_phase);
  console.log("Full game state:", JSON.stringify(gameState, null, 2));

  // Check if game is over based on game phase or status message
  const isGameOver =
    gameState.game_phase === "game_over" ||
    (gameState.status_message &&
      gameState.status_message.toLowerCase().includes("game over"));

  // Show game screen only during active gameplay
  if (
    (gameState.game_phase === "player1_turn" ||
      gameState.game_phase === "player2_turn" ||
      (gameState.game_phase === "playing" && gameState.active_player_id)) &&
    !isGameOver
  ) {
    console.log("Showing game screen for phase:", gameState.game_phase);
    showGameScreen();

    // Update player names and active state
    const player1Name = document.getElementById("player1_name");
    const player2Name = document.getElementById("player2_name");
    const player1Panel = document.querySelector(".player_red_panel");
    const player2Panel = document.querySelector(".player_blue_panel");

    // Update active player indication based on active_player_id with text only no opacity
    if (gameState.active_player_id === 1) {
      player1Name.textContent = `${gameState.player1.name} - Active`;
      player2Name.textContent = gameState.player2.name;
      player1Panel.style.opacity = "1";
      player2Panel.style.opacity = "1";
    } else if (gameState.active_player_id === 2) {
      player1Name.textContent = gameState.player1.name;
      player2Name.textContent = `${gameState.player2.name} - Active`;
      player1Panel.style.opacity = "1";
      player2Panel.style.opacity = "1";
    } else {
      // During other phases, show both players without active indicator
      player1Name.textContent = gameState.player1.name;
      player2Name.textContent = gameState.player2.name;
      player1Panel.style.opacity = "1";
      player2Panel.style.opacity = "1";
    }

    // Update scores
    document.getElementById("player1_score").textContent =
      gameState.player1.total_score;
    document.getElementById("player2_score").textContent =
      gameState.player2.total_score;

    // Update CPs
    document.getElementById(
      "player1_cp"
    ).textContent = `Command Points: ${gameState.player1.cp}`;
    document.getElementById(
      "player2_cp"
    ).textContent = `Command Points: ${gameState.player2.cp}`;

    // Update timers
    document.getElementById("player1_time").textContent =
      gameState.player1.player_time_display || "00:00:00";
    document.getElementById("player2_time").textContent =
      gameState.player2.player_time_display || "00:00:00";
    document.getElementById("total_time").textContent = `Total Time: ${
      gameState.game_timer.elapsed_display || "00:00:00"
    }`;

    // Update round
    document.getElementById(
      "round"
    ).textContent = `Round ${gameState.current_round}`;
  } else {
    // Show splash screen for all other states
    let status = "Waiting for game to start...";
    if (isGameOver) {
      status = gameState.status_message || "Game Over";
      // Show game over data
      const gameOverData = document.getElementById("game_over_data");
      gameOverData.style.display = "block";

      // Update round
      document.querySelector(
        ".game_over_round"
      ).textContent = `Round ${gameState.current_round} Complete`;

      // Update player data
      document.querySelector(
        ".game_over_player.red .game_over_name"
      ).textContent = gameState.player1.name;
      document.querySelector(
        ".game_over_player.red .game_over_score"
      ).textContent = gameState.player1.total_score;
      document.querySelector(
        ".game_over_player.red .game_over_time"
      ).textContent = gameState.player1.player_time_display || "00:00:00";

      document.querySelector(
        ".game_over_player.blue .game_over_name"
      ).textContent = gameState.player2.name;
      document.querySelector(
        ".game_over_player.blue .game_over_score"
      ).textContent = gameState.player2.total_score;
      document.querySelector(
        ".game_over_player.blue .game_over_time"
      ).textContent = gameState.player2.player_time_display || "00:00:00";

      // Update total time
      document.querySelector(
        ".game_over_total_time"
      ).textContent = `Total Time: ${
        gameState.game_timer.elapsed_display || "00:00:00"
      }`;
    } else {
      // Hide game over data for non-game-over states
      document.getElementById("game_over_data").style.display = "none";

      if (gameState.game_phase === "game_found") {
        status = "Game Found - Waiting for players...";
      } else if (gameState.game_phase === "name") {
        status = "Enter player names...";
      } else if (gameState.game_phase === "setup") {
        status = "Setting up game...";
      } else if (
        gameState.game_phase === "playing" &&
        !gameState.active_player_id
      ) {
        status = "Game in progress...";
      }
    }
    console.log(
      "Showing splash screen with status:",
      status,
      "for phase:",
      gameState.game_phase
    );
    showSplashScreen(status);
  }
}

// Helper functions for screen management
function showSplashScreen(status = "Waiting for game to start...") {
  console.log("Showing splash screen with status:", status);
  document.getElementById("splash_screen").style.display = "flex";
  document.getElementById("game_screen").style.display = "none";
  document.getElementById("splash_status").textContent = status;
}

function showGameScreen() {
  console.log("Showing game screen");
  document.getElementById("splash_screen").style.display = "none";
  document.getElementById("game_screen").style.display = "flex";
}
