// Splash screen management
export function showSplashScreen(status = "Waiting for game to start...") {
  console.log("Showing splash screen with status:", status);
  document.getElementById("splash_screen").style.display = "flex";
  document.getElementById("game_screen").style.display = "none";
  document.getElementById("game_over_screen").style.display = "none";
  document.getElementById("splash_status").textContent = status;
}

export function getSplashStatus(gamePhase) {
  switch (gamePhase) {
    case "game_found":
      return "Game Found - Waiting for players...";
    case "name":
      return "Enter player names...";
    case "setup":
      return "Setting up game...";
    case "playing":
      return "Game in progress...";
    default:
      return "Waiting for game to start...";
  }
}
