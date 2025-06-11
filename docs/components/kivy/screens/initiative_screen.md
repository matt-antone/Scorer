## Key Implementation Details

- All widget access is performed via `self.ids.<id>` (matching the widget's id in the .kv file). `ObjectProperty` is not used for widget binding, as per project-wide pattern.
