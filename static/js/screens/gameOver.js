// Game over screen management
export function showGameOverScreen(gameState) {
  console.log("Showing game over screen");
  document.getElementById("splash_screen").style.display = "none";
  document.getElementById("game_screen").style.display = "none";
  document.getElementById("game_over_screen").style.display = "flex";

  // Update round/status message
  document.getElementById("game_over_round").textContent =
    gameState.status_message || "Game Over";

  const player1NameEl = document.getElementById("game_over_player1_name");
  const player2NameEl = document.getElementById("game_over_player2_name");

  // Determine winner and update names
  const p1Score = gameState.player1.total_score;
  const p2Score = gameState.player2.total_score;

  player1NameEl.textContent = gameState.player1.name;
  player2NameEl.textContent = gameState.player2.name;

  if (p1Score > p2Score) {
    player1NameEl.textContent += " - Wins!";
  } else if (p2Score > p1Score) {
    player2NameEl.textContent += " - Wins!";
  }
  // If scores are equal, no one wins

  // Update player data
  document.getElementById("game_over_player1_score").textContent = p1Score;
  document.getElementById("game_over_player1_time").textContent =
    gameState.player1.player_time_display || "00:00:00";

  document.getElementById("game_over_player2_score").textContent = p2Score;
  document.getElementById("game_over_player2_time").textContent =
    gameState.player2.player_time_display || "00:00:00";

  // Update total time
  document.getElementById("game_over_total_time").textContent = `Total Time: ${
    gameState.game_timer.elapsed_display || "00:00:00"
  }`;
}
