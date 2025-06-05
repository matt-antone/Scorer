const gameScreen = document.getElementById("game_screen");

function init() {
  console.log("Game screen initialized");
}

function show() {
  gameScreen.style.display = "block";
}

function hide() {
  gameScreen.style.display = "none";
}

function update(state) {
  // Update player names and active state
  const player1Name = document.getElementById("player1_name");
  const player2Name = document.getElementById("player2_name");

  if (state.active_player_id === 1) {
    player1Name.textContent = `${state.player1.name} - Active`;
    player2Name.textContent = state.player2.name;
  } else if (state.active_player_id === 2) {
    player1Name.textContent = state.player1.name;
    player2Name.textContent = `${state.player2.name} - Active`;
  } else {
    player1Name.textContent = state.player1.name;
    player2Name.textContent = state.player2.name;
  }

  // Update scores
  document.getElementById("player1_score").textContent =
    state.player1.total_score;
  document.getElementById("player2_score").textContent =
    state.player2.total_score;

  // Update CPs
  document.getElementById(
    "player1_cp"
  ).textContent = `Command Points: ${state.player1.cp}`;
  document.getElementById(
    "player2_cp"
  ).textContent = `Command Points: ${state.player2.cp}`;

  // Update timers
  document.getElementById("player1_time").textContent =
    state.player1.player_time_display || "00:00:00";
  document.getElementById("player2_time").textContent =
    state.player2.player_time_display || "00:00:00";
  document.getElementById("total_time").textContent = `Total Time: ${
    state.game_timer.elapsed_display || "00:00:00"
  }`;

  // Update round
  document.getElementById("round").textContent = `Round ${state.current_round}`;
}

export const game = { init, show, hide, update };
