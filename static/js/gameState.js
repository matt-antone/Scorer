// Game state management
let currentGameState = {};

export function getGameState() {
  return currentGameState;
}

export function setGameState(newState) {
  currentGameState = newState;
  // Dispatch a custom event to notify other modules of the state change
  document.dispatchEvent(new CustomEvent("gameStateChanged"));
}

/**
 * Returns true if the game is in an active, playable state.
 */
export function isGameActive() {
  return (
    currentGameState &&
    currentGameState.game_phase === "game_play" &&
    currentGameState.active_player_id
  );
}
