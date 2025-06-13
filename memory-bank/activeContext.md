# Active Context

## Current Focus

- Restructuring package layout to match expected import paths
- Implementing missing screen functionality
- Fixing import and property issues in screens

## Recent Changes

- Moved `widgets`, `screens`, `assets`, and `state` directories from `src/` to top level of `pi_client`
- Updated import paths to match new structure
- Identified missing properties in `DeploymentSetupScreen`

## Active Decisions

1. Package Structure

   - All app modules (`widgets`, `screens`, `assets`, `state`) now at top level of `pi_client`
   - This matches the import paths expected by tests and app code
   - Removes need for `src` prefix in imports

2. Screen Implementation
   - Four screens need property/method fixes:
     - DeploymentSetupScreen
     - GameOverScreen
     - InitiativeScreen
     - NameEntryScreen
   - Current blocker: Missing properties in DeploymentSetupScreen (p1_name, p2_name)

## Next Steps

1. Complete property implementations in screens
2. Fix KV file bindings
3. Run full test suite
4. Verify screen functionality

## Current Blockers

- Missing properties in screens causing KV binding errors
- Need to verify all screen properties match KV file references

## Notes

- Package structure changes complete
- Screen implementation in progress
- Test suite partially running
- Need to complete property implementations

## 2024-06-12 Progress Update

- All InitiativeScreen tests now pass after fixing:
  - Initiative winner/loser logic
  - Tie handling
  - Added reset_rolls for test compatibility
- All NameEntryScreen tests now pass after fixing:
  - Validation and state properties
  - Ensuring player_names, qr_code, qr_code_valid, qr_code_error, and name_validation are always set in game state
- Next: Proceed to DeploymentSetupScreen and GameOverScreen to fix remaining test failures.
