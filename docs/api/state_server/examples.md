# State Server API Examples

# Version History

- v1.0.0 (2024-03-21): Initial version

Last Updated: 2024-03-21 14:30 UTC

# Related Files

- [endpoints.md](./endpoints.md): State server API endpoints
- [state_management.md](./state_management.md): State management documentation

## Overview

This document provides practical examples of using the State Server API in different scenarios.

## Game Management Examples

### 1. Creating a New Game

```javascript
// Client-side JavaScript
async function createGame() {
  const response = await fetch("http://localhost:8080/api/v1/games", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      settings: {
        timer_duration: 300,
        max_score: 100,
        game_type: "standard",
      },
    }),
  });

  const game = await response.json();
  return game.game_id;
}

// Example usage
const gameId = await createGame();
console.log("Game created:", gameId);
```

### 2. Getting Game Details

```javascript
// Client-side JavaScript
async function getGame(gameId) {
  const response = await fetch(`http://localhost:8080/api/v1/games/${gameId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

// Example usage
const game = await getGame("game123");
console.log("Game status:", game.status);
console.log("Current player:", game.current_player);
console.log("Scores:", game.scores);
```

## Game State Examples

### 1. Updating Game State

```javascript
// Client-side JavaScript
async function updateGameState(gameId, state) {
  const response = await fetch(
    `http://localhost:8080/api/v1/game-state/${gameId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state: {
          status: state.status,
          current_player: state.current_player,
          scores: state.scores,
          timer: state.timer,
        },
      }),
    }
  );

  return await response.json();
}

// Example usage
const newState = {
  status: "in_progress",
  current_player: "player1",
  scores: {
    player1: 10,
    player2: 5,
  },
  timer: 240,
};

await updateGameState("game123", newState);
```

### 2. Getting Game State

```javascript
// Client-side JavaScript
async function getGameState(gameId) {
  const response = await fetch(
    `http://localhost:8080/api/v1/game-state/${gameId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return await response.json();
}

// Example usage
const state = await getGameState("game123");
console.log("Game state:", state);
```

## Player Management Examples

### 1. Adding a Player

```javascript
// Client-side JavaScript
async function addPlayer(gameId, name, role) {
  const response = await fetch(
    `http://localhost:8080/api/v1/players/${gameId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        role: role,
      }),
    }
  );

  return await response.json();
}

// Example usage
const player = await addPlayer("game123", "John Doe", "player");
console.log("Player added:", player.player_id);
```

### 2. Getting Players

```javascript
// Client-side JavaScript
async function getPlayers(gameId) {
  const response = await fetch(
    `http://localhost:8080/api/v1/players/${gameId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  const data = await response.json();
  return data.players;
}

// Example usage
const players = await getPlayers("game123");
players.forEach((player) => {
  console.log(`${player.name} (${player.role}): ${player.status}`);
});
```

## Player State Examples

### 1. Updating Player State

```javascript
// Client-side JavaScript
async function updatePlayerState(playerId, state) {
  const response = await fetch(
    `http://localhost:8080/api/v1/player-state/${playerId}`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        state: {
          status: state.status,
          score: state.score,
        },
      }),
    }
  );

  return await response.json();
}

// Example usage
const newPlayerState = {
  status: "active",
  score: 10,
};

await updatePlayerState("player123", newPlayerState);
```

### 2. Getting Player State

```javascript
// Client-side JavaScript
async function getPlayerState(playerId) {
  const response = await fetch(
    `http://localhost:8080/api/v1/player-state/${playerId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );

  return await response.json();
}

// Example usage
const playerState = await getPlayerState("player123");
console.log("Player state:", playerState);
```

## System Configuration Examples

### 1. Getting Configuration

```javascript
// Client-side JavaScript
async function getConfig() {
  const response = await fetch("http://localhost:8080/api/v1/config", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

async function handleApiError(error) {
  if (error.response) {
    const data = await error.response.json();

    switch (error.response.status) {
      case 400:
        console.error("Bad request:", data.message);
        break;
      case 401:
        console.error("Unauthorized:", data.message);
        // Redirect to login
        break;
      case 404:
        console.error("Not found:", data.message);
        break;
      case 500:
        console.error("Server error:", data.message);
        break;
      default:
        console.error("Unknown error:", data.message);
    }
  } else {
    console.error("Network error:", error.message);
  }
}

// Example usage
try {
  await updateGameState("game123", newState);
} catch (error) {
  await handleApiError(error);
}
```

### 2. Retry Logic

```javascript
// Client-side JavaScript
async function retryOperation(operation, maxRetries = 3) {
  let retries = 0;

  while (retries < maxRetries) {
    try {
      return await operation();
    } catch (error) {
      retries++;

      if (retries === maxRetries) {
        throw error;
      }

      // Exponential backoff
      const delay = Math.min(1000 * Math.pow(2, retries), 10000);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
}

// Example usage
try {
  const result = await retryOperation(() =>
    updateGameState("game123", newState)
  );
  console.log("Operation succeeded:", result);
} catch (error) {
  console.error("Operation failed after retries:", error);
}
```

## Best Practices

1. **Error Handling**

   - Always use try-catch
   - Implement retry logic
   - Handle all error cases
   - Log errors appropriately

2. **State Management**

   - Keep local state in sync
   - Handle race conditions
   - Implement rollback
   - Validate state changes

3. **Performance**

   - Batch updates when possible
   - Use efficient data structures
   - Implement caching
   - Optimize network requests

4. **Security**
   - Validate all input
   - Sanitize user data
   - Use secure connections
   - Handle tokens properly

# Change Log

## 2024-03-21

- Initial documentation
- Added game state examples
- Added player management examples
- Added system configuration examples
- Added error handling examples
- Added best practices
