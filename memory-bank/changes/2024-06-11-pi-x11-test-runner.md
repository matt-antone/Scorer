# 2024-06-11: Pi X11 Test Runner and Workflow Changes

## X Server Configuration

- Added `/etc/X11/xorg.conf.d/99-raspberry-pi.conf` to ensure the Pi uses the correct display driver (`modesetting`) and rotates the DSI display for graphical tests.

## Test Runner Script

- Updated `run_tests_pi.sh` to:
  - Activate the Python virtual environment.
  - Set `SDL_VIDEODRIVER=x11` and `DISPLAY=:0` for X11.
  - Set `PYTHONPATH` to the project root for reliable imports.
  - Only run from a clean, git-synced state (no local edits).

## Import Path Consistency

- Audited and documented the need for absolute import paths in both Python and KV files.
- Set the project root in `PYTHONPATH` for all test/app runs.

## Pi Workflow Rule

- Added and enforced the rule: Never edit project files directly on the Pi; all changes must be made on the dev machine and pushed via git.

# Package Structure Changes

## Changes Made

1. Moved app modules from `src/` to top level:

   - `widgets/` → `pi_client/widgets/`
   - `screens/` → `pi_client/screens/`
   - `assets/` → `pi_client/assets/`
   - `state/` → `pi_client/state/`

2. Updated import paths:
   - Removed `src.` prefix from all imports
   - Updated relative imports
   - Verified KV file references

## Impact

1. Import paths now match test expectations
2. Package structure aligns with Kivy patterns
3. Simpler Python path management
4. Cleaner project organization

## Current Status

- [x] Directory moves complete
- [x] Import updates complete
- [ ] Import verification pending
- [ ] Test suite verification pending
- [ ] App functionality testing pending

## Next Steps

1. Verify all imports work correctly
2. Run full test suite
3. Test app functionality
4. Update CI/CD paths if needed

## Notes

- Package structure now matches expected import paths
- Need to complete verification steps
- May need additional import fixes
- Screen property implementations pending
