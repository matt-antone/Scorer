# SDL2/KMSDRM Setup Guide

## Current Status

- SDL2 compiled with KMSDRM support
- DRM subsystem properly configured
- Multiple DRM cards detected
- KMSDRM support still not working

## System Configuration

### DRM Devices

```
/dev/dri/
├── by-path/
├── card0
├── card1
├── card2
└── renderD128
```

### Permissions

- Devices owned by root
- Group: video, render
- Permissions: crw-rw----+

## Diagnostic Tools

### Test Script

Created `kivy_backend_test.py` with comprehensive diagnostics:

- DRM device verification
- User group checking
- Kernel KMS status
- SDL2/Kivy environment setup
- Window provider information

## Common Issues

1. KMSDRM Not Available

   - Status: Investigating
   - Possible Causes:
     - Kernel KMS not enabled
     - SDL2 configuration issue
     - Wrong DRM card selected
     - User permissions

2. Multiple DRM Cards
   - Status: Identified
   - Impact: May need explicit card selection
   - Solution: Consider SDL_VIDEODRIVER_DEVICE

## Setup Steps

1. System Requirements

   - User in video and render groups
   - DRM subsystem enabled
   - KMS support in kernel

2. SDL2 Configuration

   - Compiled with KMSDRM support
   - Linked against system libraries
   - Proper permissions set

3. Kivy Configuration
   - Using SDL2 window provider
   - Environment variables set
   - Debug logging enabled

## Environment Variables

```bash
SDL_VIDEODRIVER=kmsdrm
KIVY_WINDOW=sdl2
KIVY_TEXT=sdl2
KIVY_LOG_LEVEL=debug
```

## Debugging Steps

1. Verify DRM Setup

   ```bash
   ls -l /dev/dri/
   groups
   dmesg | grep drm
   ```

2. Check SDL2 Configuration

   - Review SDL2 config.log
   - Verify KMSDRM support
   - Check library linkage

3. Test Kivy Setup
   - Run diagnostic script
   - Check window provider
   - Review debug logs

## Next Steps

1. Run diagnostic tests
2. Verify kernel KMS support
3. Check SDL2 configuration
4. Consider DRM card selection
5. Review system logs

## Notes

- DRM subsystem appears properly configured
- Permissions and groups look correct
- Need to verify kernel-level support
- May need to adjust SDL2 configuration

## References

- SDL2 Documentation
- Kivy Window Provider Guide
- DRM/KMS Documentation
- Raspberry Pi Display Configuration
