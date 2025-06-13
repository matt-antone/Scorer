# 2024-06-11: Pi App Structure Change to src Layout

## Context

The current structure has a triple-nested `pi_app` directory which, while functional, is not as clear or maintainable as it could be. We need to:

1. Maintain proper Python package discovery
2. Keep imports working as documented
3. Make the structure more intuitive
4. Follow Python best practices

## Decision

Change the Pi App structure to use a `src` layout, which is a widely adopted Python project structure that:

- Clearly separates source code from project files
- Maintains proper package discovery
- Is more intuitive than nested package names
- Follows Python packaging best practices

### New Structure

```
pi_app/              # Project root
├── src/            # Source code directory
│   ├── screens/    # Kivy screen implementations
│   ├── widgets/    # Kivy widget implementations
│   ├── main.py     # Main application entry point
│   └── scorer.kv   # Main Kivy layout file
├── setup.py        # Package setup
└── launch_scorer.sh
```

### Benefits

1. **Clarity**: Clear separation between source code and project files
2. **Maintainability**: Easier to understand and navigate
3. **Standards**: Follows widely adopted Python project structure
4. **Compatibility**: Still works with our import patterns and package discovery

### Required Changes

1. **setup.py**:

   - Update package discovery to use src directory
   - Update package data paths

2. **Launch Scripts**:

   - Update PYTHONPATH to include src directory
   - Update any path references

3. **Imports**:

   - Update import statements to use new structure
   - Update KV file imports

4. **Documentation**:
   - Update project structure documentation
   - Update memory bank files
   - Update any path references in guides

## Implementation Plan

1. Create new structure alongside existing
2. Move files to new locations
3. Update configuration files
4. Test on both macOS and Pi
5. Update documentation
6. Remove old structure

## Related Changes

- Update project_structure.md
- Update techContext.md
- Update any path references in memory bank files

# PI App Structure Decision

## Context

The PI app's package structure was causing import issues in tests and app code. The modules were nested under `src/` but the code expected them at the top level.

## Decision

Move all app modules from `src/` to the top level of `pi_client`:

- `widgets/` → `pi_client/widgets/`
- `screens/` → `pi_client/screens/`
- `assets/` → `pi_client/assets/`
- `state/` → `pi_client/state/`

## Rationale

1. Tests and app code expect imports like `from pi_client.screens import ...`
2. Current structure with `src/` prefix causes import failures
3. Moving modules up simplifies import paths
4. Matches Kivy's expected package structure
5. Reduces complexity in Python path management

## Consequences

1. Positive:

   - Simpler import paths
   - No need for `src` prefix
   - Matches test expectations
   - Cleaner package structure
   - Better alignment with Kivy patterns

2. Negative:
   - Need to update all imports
   - Need to verify all KV file references
   - May need to update CI/CD paths

## Implementation Notes

1. Move directories:

   ```bash
   mv src/widgets ./widgets
   mv src/screens ./screens
   mv src/assets ./assets
   mv src/state ./state
   ```

2. Update imports:

   - Remove `src.` prefix from all imports
   - Update any relative imports
   - Verify KV file references

3. Verify:
   - Run test suite
   - Check all imports work
   - Verify KV file bindings
   - Test app functionality

## Status

- [x] Move directories
- [x] Update imports
- [ ] Verify all imports
- [ ] Run full test suite
- [ ] Test app functionality
