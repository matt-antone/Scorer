const elements = {
  screen: null,
  round: null,
  totalTime: null,
  p1: {
    name: null,
    role: null,
    score: null,
    cp: null,
    time: null,
  },
  p2: {
    name: null,
    role: null,
    score: null,
    cp: null,
    time: null,
  },
};

function init() {
  elements.screen = document.getElementById("game_over_screen");
  elements.round = document.getElementById("game_over_round");
  elements.totalTime = document.getElementById("game_over_total_time");
  elements.p1.name = document.getElementById("game_over_player1_name");
  elements.p1.role = document.getElementById("game_over_player1_role");
  elements.p1.score = document.getElementById("game_over_player1_score");
  elements.p1.cp = document.getElementById("game_over_player1_cp");
  elements.p1.time = document.getElementById("game_over_player1_time");
  elements.p2.name = document.getElementById("game_over_player2_name");
  elements.p2.role = document.getElementById("game_over_player2_role");
  elements.p2.score = document.getElementById("game_over_player2_score");
  elements.p2.cp = document.getElementById("game_over_player2_cp");
  elements.p2.time = document.getElementById("game_over_player2_time");
  console.log("Game over screen initialized");
}

function show() {
  if (elements.screen) {
    elements.screen.style.display = "block";
  }
}

function hide() {
  if (elements.screen) {
    elements.screen.style.display = "none";
  }
}

function update(state) {
  const {
    player1,
    player2,
    deployment_attacker_id,
    last_round_played,
    game_timer,
  } = state;

  // Update player names
  elements.p1.name.textContent = player1.name;
  elements.p2.name.textContent = player2.name;

  // Update roles
  elements.p1.role.textContent =
    deployment_attacker_id === 1 ? "Attacker" : "Defender";
  elements.p2.role.textContent =
    deployment_attacker_id === 2 ? "Attacker" : "Defender";

  // Update scores
  elements.p1.score.textContent = player1.total_score;
  elements.p2.score.textContent = player2.total_score;

  // Update CPs
  elements.p1.cp.textContent = `Command Points: ${player1.cp}`;
  elements.p2.cp.textContent = `Command Points: ${player2.cp}`;

  // Update timers
  elements.p1.time.textContent = player1.player_time_display || "00:00:00";
  elements.p2.time.textContent = player2.player_time_display || "00:00:00";

  // Update total time
  elements.totalTime.textContent = `Total Time: ${
    game_timer.elapsed_display || "00:00:00"
  }`;

  // Update round
  elements.round.textContent = `Game Over - Round ${last_round_played}`;
}

export const gameOver = { init, show, hide, update };
