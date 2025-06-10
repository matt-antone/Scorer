# Kivy UI Modularization

## Summary

- All major screen and popup definitions have been removed from `scorer.kv` and moved to their own `.kv` files in `/screens` and `/widgets`.
- The `RoundedButton` template is now in `widgets/rounded_button.kv` and included via `#:include widgets/rounded_button.kv`.
- `scorer.kv` now only contains the root widget, `#:include` statements, and no component definitions.

## Benefits

- Fully modular and maintainable Kivy UI structure
- Easy to update or add new screens/widgets
- No risk of duplicate or conflicting definitions

## Migration Notes

- All UI edits should now be made in the appropriate component `.kv` files.
- If you add new widgets or screens, create a new `.kv` file and include it in `scorer.kv` as needed.
