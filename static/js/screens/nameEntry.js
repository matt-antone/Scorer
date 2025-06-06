const elements = {
  screen: null,
  p1_qr: null,
  p2_qr: null,
  observer_qr: null,
};

function init() {
  elements.screen = document.getElementById("name_entry_screen");
  elements.p1_qr = document.getElementById("p1_qr_code");
  elements.p2_qr = document.getElementById("p2_qr_code");
  elements.observer_qr = document.getElementById("observer_qr_code");
  console.log("Name entry screen initialized");
}

function show() {
  if (elements.screen) {
    elements.screen.style.display = "block";
  }
}

function hide() {
  if (elements.screen) {
    elements.screen.style.display = "none";
  }
}

function update(state) {
  // Add a timestamp to the URL to force the browser to reload the image,
  // preventing it from showing a stale QR code from a previous session.
  const cacheBuster = `?t=${new Date().getTime()}`;

  if (state.p1_qr_path && elements.p1_qr) {
    elements.p1_qr.src = `/${state.p1_qr_path}${cacheBuster}`;
  }
  if (state.p2_qr_path && elements.p2_qr) {
    elements.p2_qr.src = `/${state.p2_qr_path}${cacheBuster}`;
  }
  if (state.observer_qr_path && elements.observer_qr) {
    elements.observer_qr.src = `/${state.observer_qr_path}${cacheBuster}`;
  }
}

export const nameEntry = { init, show, hide, update };
