# Screen: Settings Screen

## 1. Purpose

The Settings Screen provides a read-only view of the global application settings and player-specific controls. All settings are controlled by the Kivy host and synchronized across all clients.

## 2. Behavior & Flow

### Navigation

- Accessible from any screen via a persistent settings button in the navigation
- Settings button is always visible in the top-right corner
- Clicking the settings button transitions to this screen
- Uses a tabbed layout for organizing settings
- Game tab is shown by default when opening settings

### UI Components & Interaction

#### Game Tab (Default)

- **Game Controls**

  - Pause/Resume Game (Large, Prominent Button)
    - Only enabled during player's turn
    - Current game state indicator
    - Pause/Resume toggle
    - Game time display when paused
  - Screen Saver
    - Show screen saver button
    - Screen saver status
  - Concede Game

- **Player Names** (Read-only)
  - Player 1 name display
  - Player 2 name display

#### Network Tab

- **Connection Status**

  - Current connection status
  - Server IP address
  - Player role (Player 1 or Player 2)
  - Connection quality indicator
  - Latency display
  - Data transfer rate
  - "Reconnect" button
  - Auto-reconnect status
  - Last connection time
  - Connection history

- **QR Codes** (Read-only)
  - Player 1 QR Code
    - "Open Player 1 URL" button
    - URL display
  - Player 2 QR Code
    - "Open Player 2 URL" button
    - URL display
  - Observer QR Code
    - "Open Observer URL" button
    - URL display
  - Last refresh time
  - Auto-refresh status

#### System Tab

- **Updates**

  - Current version display
  - Update available indicator
  - "Update Available" notification

- **Resources**
  - Link to playwarhammer40k.com
  - Open in browser button
  - Documentation link
  - GitHub repository link

### Layout

```
[Settings]                    [Back]
----------------------------------------
[Game] [Network] [System]
----------------------------------------
[Tab Content]
```

#### Game Tab Content (Default)

```
Game Controls
[PAUSE GAME]  (Large, Prominent Button)
[Game Time: 1:23:45]
[Game State: Active]
[Your Turn: Yes]

Screen Saver
[Show Screen Saver]
[Status: Active - 3 minutes remaining]

[Concede Game]

Player Names
[Player 1: John]
[Player 2: Jane]
```

#### Network Tab Content

```
Connection Status
[Status: Connected]
[Server: 192.168.1.100:6969]
[Role: Player 1]
[Quality: ▂▃▅▆█]
[Latency: 45ms]
[Transfer: 1.2 MB/s]
[Last Connected: 2m ago]

Connection History
[Home WiFi - 2h ago]
[Work WiFi - 5h ago]
[Phone Hotspot - 1d ago]

[Reconnect]
[Auto-reconnect: Enabled]

QR Codes
[Player 1 QR] [Open URL]
[URL: http://192.168.1.100:6969/player1]

[Player 2 QR] [Open URL]
[URL: http://192.168.1.100:6969/player2]

[Observer QR] [Open URL]
[URL: http://192.168.1.100:6969/observer]

[Last refreshed: 5m ago]
[Auto-refresh: Enabled]
```

#### System Tab Content

```
Updates
[Version: 1.0.0]
[Update Available: v1.0.1]

Resources
[playwarhammer40k.com]
[Open in Browser]
[Documentation]
[GitHub Repository]
```

## 3. Screen Transition

- **Back Button**: Returns to the previous screen
- **Tab Navigation**: Switches between Game, Network, and System tabs
- **External Links**: Opens in default browser

## 4. Key Implementation Details

- **File Location**: `client/src/screens/SettingsScreen.js`
- **State Management**:
  - Settings are received from the server
  - Changes are reflected immediately when received
  - No local settings storage
- **Network Handling**:
  - Connection status is monitored and updated in real-time
  - Reconnection attempts are handled locally
- **Settings Synchronization**:
  - All settings are received via WebSocket
  - UI updates immediately on receiving changes
  - No local modification of settings
