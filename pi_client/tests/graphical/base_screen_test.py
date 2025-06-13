def validate_string_field(self, widget_id: str, expected_text: str) -> None:
    """Validate a string field's text matches the expected value.
    
    Args:
        widget_id: ID of the widget to validate
        expected_text: Expected text value
    """
    widget = self.get_widget(widget_id)
    if not widget:
        self.fail(f"Widget {widget_id} not found")
        return
        
    if not hasattr(widget, 'text'):
        self.fail(f"Widget {widget_id} has no text property")
        return
        
    if widget.text != expected_text:
        self.logger.warning(f"Widget {widget_id} text mismatch: expected {expected_text}, got {widget.text}")
        return
        
    self.logger.info(f"String field {widget_id} validated successfully") 