// Main application logic and initialization
import { socket } from "./socket.js";
import { showSplashScreen } from "./screens/index.js";

// Initialize the application
document.addEventListener("DOMContentLoaded", () => {
  console.log("Application initialized");
  showSplashScreen("Waiting for game to start...");
});
