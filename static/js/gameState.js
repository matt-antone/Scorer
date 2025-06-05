// Game state update handling
import {
  showSplashScreen,
  showGameScreen,
  showGameOverScreen,
  updateGameScreen,
  getSplashStatus,
} from "./screens/index.js";

// Helper function to update the entire UI
export function updateUI(gameState) {
  // Store the current game state
  window.currentGameState = gameState;

  console.log("Current game phase:", gameState.game_phase);
  console.log("Full game state:", JSON.stringify(gameState, null, 2));

  // Check if game is over based on game phase or status message
  const isGameOver =
    gameState.game_phase === "game_over" ||
    (gameState.status_message &&
      gameState.status_message.toLowerCase().includes("game over"));

  if (isGameOver) {
    console.log("Showing game over screen");
    showGameOverScreen(gameState);
  } else if (
    gameState.game_phase === "player1_turn" ||
    gameState.game_phase === "player2_turn" ||
    (gameState.game_phase === "playing" && gameState.active_player_id)
  ) {
    console.log("Showing game screen for phase:", gameState.game_phase);
    showGameScreen();
    updateGameScreen(gameState);
  } else {
    console.log("Showing splash screen for phase:", gameState.game_phase);
    const status = getSplashStatus(gameState.game_phase);
    showSplashScreen(status);
  }
}
