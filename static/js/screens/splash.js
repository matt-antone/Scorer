const splashScreen = document.getElementById("splash_screen");
const splashStatus = document.getElementById("splash_status");

function init() {
  // Can be used for one-time setup if needed
  console.log("Splash screen initialized");
}

function show() {
  splashScreen.style.display = "block";
}

function hide() {
  splashScreen.style.display = "none";
}

function update(state) {
  let statusText = "Waiting for game to start...";
  switch (state.game_phase) {
    case "setup":
      statusText = "Setting up new game...";
      break;
    case "name_entry":
      statusText = "Entering player names...";
      break;
    case "deployment":
      statusText = "Deployment phase...";
      break;
    case "first_turn":
      statusText = "Determining first turn...";
      break;
  }
  splashStatus.textContent = statusText;
}

export const splash = { init, show, hide, update };
