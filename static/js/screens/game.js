// Game screen management
export function showGameScreen() {
  console.log("Showing game screen");
  document.getElementById("splash_screen").style.display = "none";
  document.getElementById("game_screen").style.display = "flex";
  document.getElementById("game_over_screen").style.display = "none";
}

export function updateGameScreen(gameState) {
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
}
