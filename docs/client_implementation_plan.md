# Web Client Implementation Plan

## 1. Project Structure

```
client/
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Timer.tsx
│   │   │   └── ScoreDisplay.tsx
│   │   ├── player/
│   │   │   ├── PlayerControls.tsx
│   │   │   ├── ScoreControls.tsx
│   │   │   └── TimerControls.tsx
│   │   └── observer/
│   │       ├── GameState.tsx
│   │       └── PlayerInfo.tsx
│   ├── screens/
│   │   ├── SplashScreen.tsx
│   │   ├── GameScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── NoConnectionScreen.tsx
│   ├── services/
│   │   ├── websocket.ts
│   │   ├── gameState.ts
│   │   └── settings.ts
│   ├── hooks/
│   │   ├── useGameState.ts
│   │   ├── useWebSocket.ts
│   │   └── useSettings.ts
│   └── utils/
│       ├── validation.ts
│       ├── formatting.ts
│       └── constants.ts
├── public/
│   ├── assets/
│   └── index.html
└── package.json
```

## 2. Core Components

### WebSocket Service

```typescript
// services/websocket.ts
class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(private url: string) {}

  connect() {
    this.ws = new WebSocket(this.url);
    this.setupEventHandlers();
  }

  private setupEventHandlers() {
    this.ws?.addEventListener("open", this.handleOpen);
    this.ws?.addEventListener("message", this.handleMessage);
    this.ws?.addEventListener("close", this.handleClose);
    this.ws?.addEventListener("error", this.handleError);
  }

  sendMessage(type: string, data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          type,
          data,
          timestamp: new Date().toISOString(),
        })
      );
    }
  }
}
```

### Game State Hook

```typescript
// hooks/useGameState.ts
function useGameState() {
  const [gameState, setGameState] = useState<GameState>({
    player1: { score: 0, cp: 0 },
    player2: { score: 0, cp: 0 },
    currentTurn: 1,
    gameStatus: "active",
  });

  const updateScore = useCallback((player: number, score: number) => {
    setGameState((prev) => ({
      ...prev,
      [`player${player}`]: {
        ...prev[`player${player}`],
        score,
      },
    }));
  }, []);

  return { gameState, updateScore };
}
```

### Settings Hook

```typescript
// hooks/useSettings.ts
function useSettings() {
  const [settings, setSettings] = useState<Settings>({
    screensaver: {
      enabled: false,
      image: "default.jpg",
    },
    network: {
      currentNetwork: "",
      savedNetworks: [],
    },
  });

  const updateSetting = useCallback((key: string, value: any) => {
    setSettings((prev) => ({
      ...prev,
      [key]: value,
    }));
  }, []);

  return { settings, updateSetting };
}
```

## 3. Screen Components

### Game Screen

```typescript
// screens/GameScreen.tsx
function GameScreen() {
  const { gameState, updateScore } = useGameState();
  const { settings } = useSettings();
  const { sendMessage } = useWebSocket();

  return (
    <div className="game-screen">
      <PlayerControls
        player={1}
        score={gameState.player1.score}
        cp={gameState.player1.cp}
        onScoreChange={(score) => {
          updateScore(1, score);
          sendMessage("score_update", { player: 1, score });
        }}
      />
      <PlayerControls
        player={2}
        score={gameState.player2.score}
        cp={gameState.player2.cp}
        onScoreChange={(score) => {
          updateScore(2, score);
          sendMessage("score_update", { player: 2, score });
        }}
      />
    </div>
  );
}
```

### Settings Screen

```typescript
// screens/SettingsScreen.tsx
function SettingsScreen() {
  const { settings, updateSetting } = useSettings();
  const { sendMessage } = useWebSocket();

  return (
    <div className="settings-screen">
      <ScreensaverSettings
        enabled={settings.screensaver.enabled}
        image={settings.screensaver.image}
        onToggle={(enabled) => {
          updateSetting("screensaver.enabled", enabled);
          sendMessage("settings_update", {
            key: "screensaver.enabled",
            value: enabled,
          });
        }}
      />
      <NetworkSettings
        networks={settings.network.savedNetworks}
        currentNetwork={settings.network.currentNetwork}
        onConnect={(network) => {
          sendMessage("network_connect", { network });
        }}
      />
    </div>
  );
}
```

## 4. Styling

### Theme

```typescript
// styles/theme.ts
export const theme = {
  colors: {
    primary: "#FF0000", // Player 1 (Red)
    secondary: "#0000FF", // Player 2 (Blue)
    background: "#FFFFFF",
    text: "#000000",
    disabled: "#CCCCCC",
  },
  spacing: {
    small: "8px",
    medium: "16px",
    large: "24px",
  },
  typography: {
    fontFamily: "Inter, sans-serif",
    sizes: {
      small: "14px",
      medium: "16px",
      large: "24px",
    },
  },
};
```

### Responsive Design

```typescript
// styles/responsive.ts
export const breakpoints = {
  mobile: "320px",
  tablet: "768px",
  desktop: "1024px",
};

export const mediaQueries = {
  mobile: `@media (max-width: ${breakpoints.mobile})`,
  tablet: `@media (min-width: ${breakpoints.tablet})`,
  desktop: `@media (min-width: ${breakpoints.desktop})`,
};
```

## 5. Implementation Plan

### Phase 1: Core Setup

1. Initialize Next.js project
2. Set up WebSocket service
3. Create basic components
4. Implement state management

### Phase 2: Player Clients

1. Implement Player 1 client
2. Implement Player 2 client
3. Add score controls
4. Add timer controls

### Phase 3: Observer Client

1. Create observer interface
2. Implement game state display
3. Add player information
4. Add settings access

### Phase 4: Settings & Network

1. Implement settings screen
2. Add network management
3. Add screensaver controls
4. Add QR code display

## 6. Testing Plan

### Unit Tests

- Component rendering
- State management
- WebSocket communication
- Settings updates

### Integration Tests

- Client-server communication
- State synchronization
- Settings persistence
- Network handling

### E2E Tests

- Full game flow
- Settings changes
- Network reconnection
- Update process

## 7. Next Steps

1. Set up development environment
2. Create project structure
3. Implement core services
4. Build basic components
5. Add state management
6. Implement screens
7. Add styling
8. Test and deploy
