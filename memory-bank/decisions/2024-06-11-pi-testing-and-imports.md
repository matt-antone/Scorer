# 2024-06-11: Pi Testing and Import Path Decisions

## Display Backend Decision

- Decided to use X11 (`SDL_VIDEODRIVER=x11`) for all graphical testing on the Pi, not KMSDRM or framebuffer, to ensure compatibility with Kivy and the DSI touchscreen.

## Import Path Policy

- Decided to always use absolute package paths (`pi_app.strings.UI_STRINGS`) in both Python and KV files, and to set `PYTHONPATH` to the project root for all runs.

## Testing Validity Policy

- Decided that any tests run on the Pi are only valid if the Pi's codebase is a clean git checkout matching the dev branch—no local edits allowed.

## Documentation-Driven Testing

- Reaffirmed that all test changes must be driven by documentation, not by implementation quirks or local environment fixes.
