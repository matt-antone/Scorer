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
  elements.screen = document.getElementById("game_screen");
  elements.round = document.getElementById("round");
  elements.totalTime = document.getElementById("total_time");
  elements.p1.name = document.getElementById("player1_name");
  elements.p1.role = document.getElementById("player1_role");
  elements.p1.score = document.getElementById("player1_score");
  elements.p1.cp = document.getElementById("player1_cp");
  elements.p1.time = document.getElementById("player1_time");
  elements.p2.name = document.getElementById("player2_name");
  elements.p2.role = document.getElementById("player2_role");
  elements.p2.score = document.getElementById("player2_score");
  elements.p2.cp = document.getElementById("player2_cp");
  elements.p2.time = document.getElementById("player2_time");
  console.log("Game screen initialized");
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
    active_player_id,
    deployment_attacker_id,
    current_round,
    game_timer,
  } = state;

  // Update player names and active state
  elements.p1.name.textContent =
    active_player_id === 1 ? `${player1.name} - Active` : player1.name;
  elements.p2.name.textContent =
    active_player_id === 2 ? `${player2.name} - Active` : player2.name;

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
  elements.totalTime.textContent = `Total Time: ${
    game_timer.elapsed_display || "00:00:00"
  }`;

  // Update round
  elements.round.textContent = `Round ${current_round}`;
}

export const game = { init, show, hide, update };
