# Screen: Settings Screen

## 1. Purpose

The Settings Screen provides global application settings that affect all connected clients. Changes made here are synchronized across the Kivy host and all web clients.

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
    - Current game state indicator
    - Pause/Resume toggle
    - Game time display when paused
  - Screen Saver
    - Enable/Disable toggle
    - Upload custom picture button
    - Current picture preview
  - Reset Game
  - Clear Game State

- **Player Names**
  - Player 1 name input
  - Player 2 name input
  - Apply names button

#### Network Tab

- **WiFi Connection**

  - Available Networks List
    - Network name
    - Signal strength indicator
    - Security type (WPA2, WPA, Open)
    - One-click connect button
  - Current Connection
    - Network name
    - Signal strength
    - IP address
    - Connection status
  - Saved Networks
    - Quick connect buttons
    - "Forget" option
  - Manual Connection
    - Network name input
    - Password input (with show/hide)
    - "Connect" button
  - Network Tools
    - "Scan for Networks" button
    - "Advanced Settings" button
      - Static IP configuration
      - DNS settings
      - Network priority

- **QR Codes**
  - Player 1 QR Code
    - "Open Player 1 URL" button
    - URL display
  - Player 2 QR Code
    - "Open Player 2 URL" button
    - URL display
  - Observer QR Code
    - "Open Observer URL" button
    - URL display
  - Auto-refresh on network change
  - Manual refresh button (if needed)
  - Last refresh time

#### System Tab

- **Updates**

  - Current version display
  - Check for updates button
  - Update available indicator
  - Install update button

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

Screen Saver
[Enable Screen Saver]
[Current Picture: default.jpg]
[Upload New Picture]

[Reset Game]
[Clear Game State]

Player Names
[Player 1: _____________]
[Player 2: _____________]
[Apply Names]
```

#### Network Tab Content

```
Available Networks
[Home WiFi]     [▂▃▅▆█] [WPA2] [Connect]
[Work WiFi]     [▂▃▅▆█] [WPA2] [Connect]
[Guest WiFi]    [▂▃▅▆█] [Open] [Connect]
[Neighbor WiFi] [▂▃▅▆█] [WPA] [Connect]
[Phone Hotspot] [▂▃▅▆█] [WPA2] [Connect]
[Public WiFi]   [▂▃▅▆█] [Open] [Connect]

Current Connection
[Network: Home WiFi]
[Signal: ▂▃▅▆█]
[IP: 192.168.1.100]
[Status: Connected]

Saved Networks
[Home WiFi] [Connect] [Forget]
[Work WiFi] [Connect] [Forget]

[Scan for Networks]
[Advanced Settings]

Manual Connection
[Network Name: _____________]
[Password: ********] [Show]
[Connect]

QR Codes
[Player 1 QR] [Open URL]
[URL: http://192.168.1.100:6969/player1]

[Player 2 QR] [Open URL]
[URL: http://192.168.1.100:6969/player2]

[Observer QR] [Open URL]
[URL: http://192.168.1.100:6969/observer]

[Last refreshed: 5m ago]
[Refresh QR Codes] (if needed)
```

#### System Tab Content

```
Updates
[Version: 1.0.0]
[Check for Updates]
[Update Available: v1.0.1]
[Install Update]

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

- **File Location**: `screens/settings_screen.py`
- **State Management**:
  - Settings are persisted in `settings.json`
  - Changes are broadcast to all connected clients
  - All clients maintain synchronized settings
- **Network Handling**:
  - WiFi connection management
  - QR code generation and display
  - Network status monitoring
- **Update System**:
  - Checks GitHub releases on startup
  - Downloads and installs updates
  - Maintains version information
- **Settings Synchronization**:
  - All settings changes are broadcast via WebSocket
  - Clients update their UI immediately on receiving changes
  - Settings are enforced consistently across all clients
