const gameOverScreen = document.getElementById("game_over_screen");

function init() {
  console.log("Game over screen initialized");
}

function show() {
  gameOverScreen.style.display = "block";
}

function hide() {
  gameOverScreen.style.display = "none";
}

function update(state) {
  // Update player names
  document.getElementById("game_over_player1_name").textContent =
    state.player1.name;
  document.getElementById("game_over_player2_name").textContent =
    state.player2.name;

  // Update scores
  document.getElementById("game_over_player1_score").textContent =
    state.player1.total_score;
  document.getElementById("game_over_player2_score").textContent =
    state.player2.total_score;

  // Update timers
  document.getElementById("game_over_player1_time").textContent =
    state.player1.player_time_display || "00:00:00";
  document.getElementById("game_over_player2_time").textContent =
    state.player2.player_time_display || "00:00:00";

  // Update total time
  document.getElementById("game_over_total_time").textContent = `Total Time: ${
    state.game_timer.elapsed_display || "00:00:00"
  }`;

  // Update round
  document.getElementById(
    "game_over_round"
  ).textContent = `Round ${state.current_round}`;
}

export const gameOver = { init, show, hide, update };
