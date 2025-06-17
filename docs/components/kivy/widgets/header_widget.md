## Settings Button (GearButton)

- The header uses a reusable `GearButton` widget for the settings (cog) button.
- `GearButton` is a 24dp x 24dp image-based button, vertically centered in the header using `pos_hint: {'center_y': 0.5}`.
- The button uses a transparent background and a white gear icon PNG for both normal and pressed states.
- The `on_release` event of `GearButton` dispatches the `on_settings` event from the header widget.
- This approach ensures consistent styling, reusability, and proper event handling across the app.
