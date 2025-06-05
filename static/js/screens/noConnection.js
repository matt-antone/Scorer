// Handles the 'No Connection' screen
const noConnectionScreen = document.getElementById("no-connection-screen");

function init() {
  console.log("No connection screen initialized");
}

function show() {
  if (noConnectionScreen) {
    noConnectionScreen.style.display = "flex";
  }
}

function hide() {
  if (noConnectionScreen) {
    noConnectionScreen.style.display = "none";
  }
}

export { init, show, hide };
