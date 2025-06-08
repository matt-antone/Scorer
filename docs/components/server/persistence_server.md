# Persistence Server

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [state_server.md](./state_server.md): State server implementation
- [game_state.md](./game_state.md): Game state management
- [../../api/state_server/state_management.md](../../api/state_server/state_management.md): State management API
- [../../api/state_server/persistence.md](../../api/state_server/persistence.md): Persistence API

# Overview

The Persistence Server is responsible for managing the storage and retrieval of game state data. It provides reliable persistence mechanisms for game states, player states, and system configurations.

# Purpose

- Store game state data
- Retrieve game state data
- Manage data persistence
- Ensure data consistency
- Handle data recovery

# Properties

- `storage`: Storage instance
- `settings`: Persistence configuration
  ```json
  {
    "storage_type": "string",
    "backup_enabled": boolean,
    "backup_interval": number,
    "max_backups": number,
    "compression_enabled": boolean,
    "encryption_enabled": boolean
  }
  ```
- `cache`: In-memory cache
  ```json
  {
    "game_states": {
      "game_id": {
        "data": "object",
        "last_updated": "ISO8601",
        "is_dirty": boolean
      }
    },
    "player_states": {
      "player_id": {
        "data": "object",
        "last_updated": "ISO8601",
        "is_dirty": boolean
      }
    }
  }
  ```

# Methods

- `initializeStorage(settings)`: Initialize storage system
- `storeGameState(gameId, state)`: Store game state
- `retrieveGameState(gameId)`: Retrieve game state
- `storePlayerState(playerId, state)`: Store player state
- `retrievePlayerState(playerId)`: Retrieve player state
- `backupData()`: Create data backup
- `restoreFromBackup(backupId)`: Restore from backup
- `cleanupOldBackups()`: Clean up old backups
- `validateData(data)`: Validate stored data
- `handleError(error)`: Handle storage errors

# Events

- `storage_initialized`: Fired when storage is initialized
- `state_stored`: Fired when state is stored
- `state_retrieved`: Fired when state is retrieved
- `backup_created`: Fired when backup is created
- `backup_restored`: Fired when backup is restored
- `backup_cleaned`: Fired when old backups are cleaned
- `data_validated`: Fired when data is validated
- `error_occurred`: Fired when error occurs

# Flow

1. Storage system is initialized
2. Data is validated before storage
3. Data is stored with backup
4. Cache is updated
5. Old backups are cleaned up

# Example Usage

```javascript
// persistence-server.js
class PersistenceServer {
  constructor() {
    this.storage = null;
    this.cache = {
      game_states: new Map(),
      player_states: new Map(),
    };
    this.settings = {
      storage_type: "file",
      backup_enabled: true,
      backup_interval: 3600000, // 1 hour
      max_backups: 24,
      compression_enabled: true,
      encryption_enabled: true,
    };
  }

  async initializeStorage(settings) {
    try {
      this.settings = { ...this.settings, ...settings };
      this.storage = await this.createStorage();
      this.emit("storage_initialized", this.settings);
      this.startBackupSchedule();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async storeGameState(gameId, state) {
    try {
      this.validateData(state);
      const data = {
        data: state,
        last_updated: new Date().toISOString(),
        is_dirty: false,
      };

      if (this.settings.encryption_enabled) {
        data.data = await this.encryptData(data.data);
      }

      if (this.settings.compression_enabled) {
        data.data = await this.compressData(data.data);
      }

      await this.storage.store(`game_states/${gameId}`, data);
      this.cache.game_states.set(gameId, data);
      this.emit("state_stored", { gameId, timestamp: data.last_updated });

      if (this.settings.backup_enabled) {
        await this.backupData();
      }
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async retrieveGameState(gameId) {
    try {
      // Check cache first
      const cached = this.cache.game_states.get(gameId);
      if (cached && !cached.is_dirty) {
        return cached.data;
      }

      // Retrieve from storage
      const data = await this.storage.retrieve(`game_states/${gameId}`);
      if (!data) {
        throw new Error("Game state not found");
      }

      if (this.settings.compression_enabled) {
        data.data = await this.decompressData(data.data);
      }

      if (this.settings.encryption_enabled) {
        data.data = await this.decryptData(data.data);
      }

      this.cache.game_states.set(gameId, data);
      this.emit("state_retrieved", { gameId, timestamp: data.last_updated });
      return data.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async backupData() {
    try {
      const backupId = generateBackupId();
      const timestamp = new Date().toISOString();
      const data = await this.storage.retrieveAll();

      const backup = {
        id: backupId,
        timestamp: timestamp,
        data: data,
      };

      await this.storage.store(`backups/${backupId}`, backup);
      this.emit("backup_created", { backupId, timestamp });

      await this.cleanupOldBackups();
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async restoreFromBackup(backupId) {
    try {
      const backup = await this.storage.retrieve(`backups/${backupId}`);
      if (!backup) {
        throw new Error("Backup not found");
      }

      await this.storage.restore(backup.data);
      this.emit("backup_restored", { backupId, timestamp: backup.timestamp });
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async cleanupOldBackups() {
    try {
      const backups = await this.storage.list("backups");
      if (backups.length > this.settings.max_backups) {
        const toDelete = backups
          .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
          .slice(this.settings.max_backups);

        for (const backup of toDelete) {
          await this.storage.delete(`backups/${backup.id}`);
        }

        this.emit("backup_cleaned", { count: toDelete.length });
      }
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  validateData(data) {
    // Implement data validation logic
    this.emit("data_validated", { timestamp: new Date().toISOString() });
  }

  handleError(error) {
    this.emit("error_occurred", {
      error: error.message,
      timestamp: new Date().toISOString(),
    });
  }
}
```

# Changelog

## 2024-03-21

- Initial documentation
- Added overview, properties, methods, and flow
- Added persistence mechanisms
- Added backup functionality
- Added data validation
- Linked related API documentation
