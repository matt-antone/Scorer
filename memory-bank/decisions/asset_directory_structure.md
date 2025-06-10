# Decision: Asset Directory Structure

## Context

- Need to share assets across multiple components (pi_app, state_server, phone_clients)
- Current structure has assets duplicated or scattered across components
- Need to ensure consistent access to fonts, images, and other resources
- Must maintain proper relative paths for all components

## Alternatives Considered

1. **Keep Assets in pi_app**

   - Pros:
     - Maintains current structure
     - No immediate changes needed
   - Cons:
     - Duplicates assets across components
     - Harder to maintain consistency
     - More storage space used
     - Components can't easily share assets

2. **Create Shared Library**

   - Pros:
     - Clear separation of concerns
     - Could version assets independently
   - Cons:
     - Adds complexity
     - Overkill for current needs
     - More difficult to deploy
     - Unnecessary abstraction

3. **Move to Root Level (Chosen)**
   - Pros:
     - Single source of truth for assets
     - Easy to maintain and update
     - Clear relative paths for all components
     - Simpler deployment
   - Cons:
     - Requires updating all file references
     - Need to ensure proper access from all components

## Decision

Move all assets to the root level of the project, creating a shared `assets/` directory accessible to all components.

### Implementation Details

1. Directory Structure:

   ```
   assets/
   ├── fonts/        # Font files
   ├── billboards/   # Screensaver images
   ├── qr_codes/     # Generated QR codes
   └── icons/        # Application icons
   ```

2. Path References:

   - pi_app: Use `../assets/` (one level up)
   - state_server: Use `../assets/` (one level up)
   - phone_clients: Use `../assets/` (one level up)

3. Required Updates:
   - Update all Kivy file references
   - Update documentation
   - Update memory bank files
   - Verify all components can access assets

## Related Changes

- [Asset Directory Move](../changes/2024-05-20-asset-directory-move.md)
- [File Reference Updates](../changes/2024-05-20-file-reference-updates.md)

## Verification

- [x] All Kivy files updated with correct paths
- [x] Documentation reflects new structure
- [x] Memory bank files updated
- [x] All components can access assets
- [x] No broken references found

## Impact

- Improved asset management
- Reduced duplication
- Clearer project structure
- Better maintainability

## Future Considerations

- Consider adding asset versioning if needed
- May need to implement asset caching for web clients
- Could add asset validation in the future
- Might need to implement asset compression for deployment
