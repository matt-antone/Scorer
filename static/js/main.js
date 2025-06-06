// Main application logic and initialization
import { socket } from "./socket.js";
import { getGameState } from "./gameState.js";
import screens from "./screens/index.js";

let isConnected = true;
let hasInitialStateBeenSet = false;

const screenMappings = {
  splash: screens.splash,
  setup: screens.splash,
  name_entry: screens.nameEntry,
  deployment_setup: screens.splash,
  first_turn_setup: screens.splash,
  game_play: screens.game,
  game_over: screens.gameOver,
  default: screens.splash,
};

export function setInitialState() {
  hasInitialStateBeenSet = true;
  handleGameStateChange();
}

function handleConnectionStatusChange(event) {
  const { status } = event.detail;
  isConnected = status === "connected";

  if (isConnected) {
    screens.noConnection.hide();
    // When reconnected, refresh the main view by fetching the latest game state
    handleGameStateChange();
  } else {
    // Hide all other screens and show the no-connection screen
    Object.values(screens).forEach((screen) => {
      if (
        screen &&
        typeof screen.hide === "function" &&
        screen !== screens.noConnection
      ) {
        screen.hide();
      }
    });
    screens.noConnection.show();
  }
}

function handleGameStateChange() {
  // Do not change screens if the connection is lost OR if we haven't received the first state
  if (!isConnected || !hasInitialStateBeenSet) {
    return;
  }

  const state = getGameState();
  const gamePhase = state.game_phase || "default";
  const nextScreen = screenMappings[gamePhase] || screenMappings.default;

  // Hide all screens to ensure a clean slate
  Object.values(screens).forEach((screen) => {
    if (screen && typeof screen.hide === "function") {
      screen.hide();
    }
  });

  // Show and update the one correct screen
  if (nextScreen) {
    nextScreen.show();
    if (typeof nextScreen.update === "function") {
      nextScreen.update(state);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  console.log("Application Initialized");

  // Initialize all screen modules
  Object.values(screens).forEach((screen) => {
    if (screen && typeof screen.init === "function") {
      screen.init();
    }
  });

  // Listen for game state changes
  document.addEventListener("gameStateChanged", handleGameStateChange);

  // Set the initial screen state (defaults to splash)
  // This will be triggered by setInitialState after the first game state is received
  // handleGameStateChange();

  document.addEventListener(
    "connectionStatusChanged",
    handleConnectionStatusChange
  );
});
