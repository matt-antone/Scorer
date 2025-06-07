document.addEventListener("DOMContentLoaded", () => {
  const socket = io();

  // --- DOM Elements ---
  const elements = {
    round: document.getElementById("round"),
    totalTime: document.getElementById("total_time"),
    p1: {
      panel: document.querySelector(".red_panel"),
      name: document.getElementById("player1_name"),
      role: document.getElementById("player1_role"),
      score: document.getElementById("player1_score"),
      cp: document.getElementById("player1_cp"),
      time: document.getElementById("player1_time"),
    },
    p2: {
      panel: document.querySelector(".blue_panel"),
      name: document.getElementById("player2_name"),
      role: document.getElementById("player2_role"),
      score: document.getElementById("player2_score"),
      cp: document.getElementById("player2_cp"),
      time: document.getElementById("player2_time"),
    },
    controls: {
      primaryScoreBox: document.getElementById("primary_score_box"),
      secondaryScoreBox: document.getElementById("secondary_score_box"),
      primaryScore: document.getElementById("primary_score"),
      secondaryScore: document.getElementById("secondary_score"),
      cpButton: document.getElementById("cp_button"),
      endTurnButton: document.getElementById("end_turn_button"),
      concedeButton: document.getElementById("concede_button"),
    },
    numpad: {
      overlay: document.getElementById("numpad-overlay"),
      display: document.getElementById("numpad_display"),
      keys: document.querySelectorAll(".numpad-key"),
      confirm: document.getElementById("numpad_confirm"),
      clear: document.getElementById("numpad_clear"),
    },
  };

  // --- State ---
  let currentPlayerId = null;
  let activeNumpadTarget = null; // 'primary' or 'secondary'
  let totalTimerInterval, playerTimerInterval;

  // --- Functions ---
  function getPlayerIdFromUrl() {
    const path = window.location.pathname;
    const parts = path.split("/");
    const playerId = parseInt(parts[parts.length - 1], 10);
    if (!isNaN(playerId)) {
      currentPlayerId = playerId;
      console.log(`Current player ID set to: ${currentPlayerId}`);
      document.body.classList.add(playerId === 1 ? "player-1" : "player-2");
    } else {
      console.error("Could not determine player ID from URL.");
    }
  }

  function formatTime(totalSeconds) {
    const hours = Math.floor(totalSeconds / 3600)
      .toString()
      .padStart(2, "0");
    const minutes = Math.floor((totalSeconds % 3600) / 60)
      .toString()
      .padStart(2, "0");
    const seconds = Math.floor(totalSeconds % 60)
      .toString()
      .padStart(2, "0");
    return `${hours}:${minutes}:${seconds}`;
  }

  function updateUI(state) {
    if (!state) return;

    // Stop any existing timers before updating the UI
    clearInterval(totalTimerInterval);
    clearInterval(playerTimerInterval);

    const {
      player1,
      player2,
      active_player_id,
      deployment_attacker_id,
      current_round,
      game_timer,
    } = state;

    elements.round.textContent = `Round ${current_round}`;

    // --- Live Total Timer ---
    if (game_timer && game_timer.status === "running") {
      let totalSeconds = game_timer.elapsed_seconds;
      elements.totalTime.textContent = formatTime(totalSeconds);
      totalTimerInterval = setInterval(() => {
        totalSeconds++;
        elements.totalTime.textContent = formatTime(totalSeconds);
      }, 1000);
    } else {
      elements.totalTime.textContent = game_timer.elapsed_display || "00:00:00";
    }

    // Update P1
    elements.p1.name.textContent = player1.name;
    elements.p1.role.textContent =
      deployment_attacker_id === 1 ? "Attacker" : "Defender";
    elements.p1.score.textContent = player1.total_score;
    elements.p1.cp.textContent = `CP: ${player1.cp}`;
    elements.p1.time.textContent = player1.player_time_display || "00:00:00";

    // Update P2
    elements.p2.name.textContent = player2.name;
    elements.p2.role.textContent =
      deployment_attacker_id === 2 ? "Attacker" : "Defender";
    elements.p2.score.textContent = player2.total_score;
    elements.p2.cp.textContent = `CP: ${player2.cp}`;
    elements.p2.time.textContent = player2.player_time_display || "00:00:00";

    // --- Live Player Timer ---
    if (game_timer && game_timer.status === "running" && active_player_id) {
      const activePlayer = active_player_id === 1 ? player1 : player2;
      const activePlayerElement =
        active_player_id === 1 ? elements.p1 : elements.p2;

      if (activePlayer && activePlayer.live_elapsed_seconds !== undefined) {
        let playerSeconds = activePlayer.live_elapsed_seconds;
        activePlayerElement.time.textContent = formatTime(playerSeconds);
        playerTimerInterval = setInterval(() => {
          playerSeconds++;
          activePlayerElement.time.textContent = formatTime(playerSeconds);
        }, 1000);
      }
    }

    // Update player-specific controls
    if (currentPlayerId === 1) {
      elements.controls.primaryScore.textContent = player1.primary_score;
      elements.controls.secondaryScore.textContent = player1.secondary_score;
    } else if (currentPlayerId === 2) {
      elements.controls.primaryScore.textContent = player2.primary_score;
      elements.controls.secondaryScore.textContent = player2.secondary_score;
    }

    // Set active class
    elements.p1.panel.classList.toggle("active", active_player_id === 1);
    elements.p2.panel.classList.toggle("active", active_player_id === 2);
  }

  // --- Numpad Functions ---
  function showNumpad(target) {
    activeNumpadTarget = target;
    elements.numpad.display.textContent = "";
    elements.numpad.overlay.style.display = "flex";
  }

  function hideNumpad() {
    elements.numpad.overlay.style.display = "none";
    activeNumpadTarget = null;
  }

  function handleNumpadKeyPress(key) {
    let current_val = elements.numpad.display.textContent;
    if (current_val.length < 3) {
      elements.numpad.display.textContent += key;
    }
  }

  function handleNumpadConfirm() {
    const value = parseInt(elements.numpad.display.textContent, 10);
    if (!isNaN(value) && activeNumpadTarget) {
      socket.emit("update_score", {
        player_id: currentPlayerId,
        score_type: activeNumpadTarget,
        value: value,
      });
    }
    hideNumpad();
  }

  // --- Socket Emitters ---
  function incrementCp() {
    socket.emit("increment_cp", { player_id: currentPlayerId });
  }

  function endTurn() {
    socket.emit("end_turn", { player_id: currentPlayerId });
  }

  function concede() {
    if (confirm("Are you sure you want to concede the game?")) {
      socket.emit("concede_game", { player_id: currentPlayerId });
    }
  }

  // --- Event Listeners ---
  elements.controls.primaryScoreBox.addEventListener("click", () =>
    showNumpad("primary")
  );
  elements.controls.secondaryScoreBox.addEventListener("click", () =>
    showNumpad("secondary")
  );
  elements.controls.cpButton.addEventListener("click", incrementCp);
  elements.controls.endTurnButton.addEventListener("click", endTurn);
  elements.controls.concedeButton.addEventListener("click", concede);

  elements.numpad.keys.forEach((key) => {
    key.addEventListener("click", () => handleNumpadKeyPress(key.dataset.key));
  });
  elements.numpad.clear.addEventListener(
    "click",
    () => (elements.numpad.display.textContent = "")
  );
  elements.numpad.confirm.addEventListener("click", handleNumpadConfirm);
  window.addEventListener("click", (e) => {
    if (e.target === elements.numpad.overlay) {
      hideNumpad();
    }
  });

  // --- Socket Listeners ---
  socket.on("connect", () => {
    console.log("Player client connected to server");
    // No longer requesting state, waiting for game_start or update
  });

  socket.on("disconnect", () => {
    console.log("Player client disconnected");
  });

  socket.on("game_start", (state) => {
    console.log("Game start event received:", state);
    updateUI(state);
  });

  socket.on("game_state_update", (state) => {
    console.log("Game state update received:", state);
    updateUI(state);
  });

  // --- Initialization ---
  getPlayerIdFromUrl();
  console.log("Initialized player client");
});
