let splashScreen;
let splashStatus;

function init() {
  splashScreen = document.getElementById("splash_screen");
  splashStatus = document.getElementById("splash_status");
  console.log("Splash screen initialized");
}

function show() {
  if (splashScreen) {
    splashScreen.style.display = "block";
  }
}

function hide() {
  if (splashScreen) {
    splashScreen.style.display = "none";
  }
}

function update(state) {
  if (!splashStatus) return;

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
