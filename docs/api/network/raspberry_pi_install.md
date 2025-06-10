# Raspberry Pi Installation

## Display Rotation Option

During installation, the script will prompt you:

    Do you want to rotate the display 180 degrees for upside-down mounting? (y/n):

If you answer 'y', the script will update /boot/config.txt with the appropriate setting (display_lcd_rotate=2). This rotates the display at the hardware level. A reboot is required for the change to take effect.

This is useful for kiosk or tabletop setups where the screen is mounted upside-down.
