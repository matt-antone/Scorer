const nameEntryScreen = document.getElementById("name_entry_screen");

function init() {
  console.log("Name entry screen initialized");
}

function show() {
  nameEntryScreen.style.display = "block";
}

function hide() {
  nameEntryScreen.style.display = "none";
}

function update(state) {
  // Placeholder for future logic to display player names as they are entered
}

export const nameEntry = { init, show, hide, update };
