# Features & Capabilities

## Core Features

### ✅ PC Power Management
- **Wake PC** - Wake from sleep/hibernation mode
- **Sleep PC** - Put PC into sleep state
- Remote power control from anywhere in your home

### ✅ Display Control
- **Turn Display On** - Wake monitors from power-saving mode
- **Turn Display Off** - Blank screen/power-saving mode
- Supports single and multi-monitor setups

### ✅ Browser Window Management
- **Focus Browser** - Bring browser window to foreground
- **Move to TV Monitor** - Relocate browser to specific display
- **Maximize** - Full-screen browser window
- **Minimize** - Minimize browser to taskbar
- **Close Browser** - Close browser application
- **Restore Session** - Reopen browser with last tabs

### ✅ Browser Application Control
- **Open Chrome** - Launch Chrome browser
- **Open Firefox** - Launch Firefox browser
- **Open Edge** - Launch Edge browser

### ✅ Tab Management
- **New Tab** - Open a new tab in active browser
- **Close Tab** - Close current tab
- **Next Tab** - Switch to next tab (Ctrl+Tab)
- **Previous Tab** - Switch to previous tab (Ctrl+Shift+Tab)

### ✅ Page Control
- **Reload Page** - Refresh current page (F5)
- **Hard Reload** - Refresh page bypassing cache (Ctrl+F5)
- **Home Page** - Navigate to browser home page (Alt+Home)

### ✅ URL Navigation
- **Open URL** - Open any specific URL in default browser
- **Open YouTube** - Quick access to YouTube
- **Open Hulu** - Quick access to Hulu
- **Open Custom Sites** - Configurable for any website

### ✅ Playback Control (Universal)
Works seamlessly on YouTube, Netflix, Hulu, Prime Video, Disney+, and other streaming platforms:
- **Play** - Start video playback
- **Pause** - Pause video playback
- **Toggle Play/Pause** - Switch between play and pause states
- **Stop** - Stop playback and exit fullscreen
- **Restart** - Jump to beginning and restart video
- **Seek Forward (Small)** - Skip ahead 5 seconds
- **Seek Backward (Small)** - Skip back 5 seconds
- **Seek Forward (Large)** - Skip ahead 10 seconds
- **Seek Backward (Large)** - Skip back 10 seconds
- **Jump to Beginning** - Instant jump to video start
- **Jump to End** - Instant jump to video end
- **Next Video** - Play next video in playlist/queue
- **Previous Video** - Play previous video in playlist

### ✅ Fullscreen & View Modes
- **Enter Fullscreen** - Enter fullscreen mode (F11)
- **Exit Fullscreen** - Exit fullscreen mode (Escape)
- **Toggle Fullscreen** - Toggle fullscreen on/off
- **Theater Mode** - Enter YouTube theater mode
- **Exit Theater Mode** - Exit YouTube theater mode
- **Picture-in-Picture Enter** - Enter PiP mode
- **Picture-in-Picture Exit** - Exit PiP mode

### ✅ Audio Control (OS + Browser)
System-wide and browser-specific audio controls:
- **Volume Up** - Increase system volume
- **Volume Down** - Decrease system volume
- **Mute Audio** - Mute system audio
- **Unmute Audio** - Unmute system audio
- **Toggle Mute** - Toggle mute/unmute state
- **Set Volume** - Set volume to predefined levels (25%, 50%, 75%, 100%)
- **Mute Browser Tab** - Mute video in browser tab (M key)
- **Unmute Browser Tab** - Unmute video in browser tab
- **Mute System Audio** - Mute all system audio
- **Restore System Audio** - Restore/unmute all system audio

### ✅ Subtitles & Captions
- **Toggle Captions On** - Enable captions (C key)
- **Toggle Captions Off** - Disable captions
- **Cycle Caption Language** - Open caption settings menu
- **Increase Caption Size** - Zoom in to make captions larger
- **Decrease Caption Size** - Zoom out to make captions smaller

### ✅ Navigation Control (Keyboard-Based)
- **Select Element** - Activate focused element (Enter key)
- **Navigate Back** - Go to previous page (Alt+Left)
- **Navigate Forward** - Go to next page (Alt+Right)
- **Exit Menu** - Close menus and overlays (Escape)
- **Scroll Up/Down** - Scroll page content (Arrow keys)
- **Page Up/Down** - Quick page navigation
- **Focus Search** - Move to address/search bar (Ctrl+L)
- **Clear Search** - Clear text in search field
- **Submit Search** - Submit search or form (Enter)
- **Tab Forward** - Navigate between elements (Tab key)

### ✅ Search & Content Discovery
- **Search YouTube** - Search YouTube for any query
- **Search Hulu** - Search Hulu for any query
- **Search Current Site** - Find in page (Ctrl+F)
- **Open YouTube Trending** - Browse trending videos
- **Open YouTube Subscriptions** - View subscription feed
- **Open Hulu Watchlist** - Access "My Stuff" watchlist
- **Open YouTube History** - View watch history
- **Open Netflix Home** - Navigate to Netflix browse

### ✅ User Interaction (Site-Specific)
- **Like Video** - Like YouTube videos (Shift+L)
- **Dislike Video** - Dislike YouTube videos (Shift+D)
- **Subscribe** - Subscribe to YouTube channels (Shift+S)
- **Skip Button Action** - Skip ads, intros, and recaps (Tab + Enter)

### ✅ Multi-Monitor Control
- **Move to Monitor 1** - Move browser to primary monitor
- **Move to Monitor 2** - Move browser to secondary monitor/TV
- Dual monitor support for dedicated viewing experiences

### ✅ Focus & Distraction Control
- **Enable Focus Assist** - Turn on Do Not Disturb mode
- **Disable Focus Assist** - Turn off Do Not Disturb mode
- **Prevent Sleep** - Keep screen active (no sleep)
- **Allow Sleep** - Allow normal screen sleep behavior

### ✅ Smart Convenience Commands
Pre-configured sequences for common tasks:
- **Show Me Something** - Open homepage/feed
- **Continue Last** - Resume previous session
- **Find Else** - Reload recommendations
- **That's Enough** - Pause and exit fullscreen
- **Kill Playback** - Stop, exit fullscreen, minimize
- **Emergency Mute** - Instant system-wide mute

### ✅ Home Assistant Integration
- REST API endpoints for all commands
- Button entities for dashboard control
- Status sensor with real-time monitoring
- Full automation support
- Voice assistant compatible

## Technical Capabilities

### ESP32 Features
- **WiFi Connectivity** - 2.4 GHz WiFi support
- **Web Server** - Async HTTP server for low latency
- **mDNS Support** - Easy discovery (esp32-pc-controller.local)
- **Status Reporting** - Real-time device status
- **Auto-Reconnect** - Automatic WiFi reconnection
- **Serial Communication** - 115200 baud reliable communication

### Windows Integration
- **Windows API** - Native Windows power and window management
- **Multi-Browser Support** - Chrome, Firefox, Edge, Brave
- **Process Detection** - Smart browser window finding
- **Multi-Monitor Support** - Configurable monitor targeting
- **Error Handling** - Graceful failure with status reporting
- **Background Operation** - Runs as system service

### Network Features
- **HTTP REST API** - Standard REST endpoints
- **JSON Responses** - Structured data format
- **Status Monitoring** - Device health and connectivity
- **Low Latency** - Fast command execution (<100ms typical)
- **Local Network** - No cloud dependency

## Use Cases

### 🏠 Home Automation
```yaml
Morning Routine:
  - Wake PC at 7 AM
  - Turn on display
  - Open browser with news tabs

Evening Routine:
  - Close browser at 11 PM
  - Put PC to sleep
```

### 🎬 Media Control
```yaml
Movie Mode:
  - Focus browser
  - Move to TV display
  - Enter fullscreen mode
  - Maximize for full-screen
  - Perfect for streaming

Video Playback:
  - Play/pause with one command
  - Seek forward/backward
  - Jump to beginning or end
  - Navigate playlists
  - Stop and exit fullscreen
  - Enter/exit theater mode
  - Picture-in-picture mode
  
Audio Control:
  - Volume up/down
  - Mute/unmute system audio
  - Mute browser tab for videos
  - Set volume to specific levels
  - Toggle mute quickly
  
Accessibility:
  - Enable/disable captions
  - Cycle caption languages
  - Adjust caption size
  - Better viewing experience
  
Quick Access:
  - Open YouTube with one click
  - Open Hulu for shows
  - Open Netflix/Prime/Disney+ via URL
  - Control playback universally
  - Navigate with tab controls
```

### 💼 Work From Home
```yaml
Work Start:
  - Wake PC when home
  - Display on when motion detected
  - Focus browser for video calls

Work End:
  - Minimize browser when done
  - Display off after inactivity
```

### 🎮 Gaming
```yaml
Gaming Session:
  - Close browser (free resources)
  - Display on
  - Ready for gaming

Post-Gaming:
  - Restore browser
  - Normal desktop mode
```

### 🔋 Energy Saving
```yaml
Presence Detection:
  - Display off when away
  - Sleep PC when no one home
  - Auto wake on arrival

Scheduled:
  - Sleep at night
  - Wake in morning
```

### 🗣️ Voice Control
```
"Hey Google, wake my PC"
"Alexa, turn off my display"
"Hey Google, open browser on TV"
```

## Automation Examples

### Presence-Based
- Display on when motion detected
- Display off after 30 min inactivity
- Sleep PC when leaving home
- Wake PC when arriving home

### Time-Based
- Wake PC weekday mornings
- Sleep PC every night
- Display off during lunch
- Close browser at bedtime

### Event-Based
- Focus browser for video meetings
- Move browser to TV for movie time
- Minimize browser during gaming
- Wake display for doorbell alerts

### Condition-Based
- Only wake if someone home
- Sleep only if no motion
- Display off only during day
- Browser control only if running

## Monitoring & Status

### Real-Time Status
- PC power state (awake/asleep)
- Display state (on/off)
- Last command executed
- Command execution time
- WiFi connection strength
- Device uptime
- ESP32 IP address

### Debugging
- Serial monitor output
- HTTP status codes
- Error messages
- Command acknowledgments

## Supported Browsers

### Out of the Box
- ✅ Google Chrome
- ✅ Mozilla Firefox
- ✅ Microsoft Edge
- ✅ Brave Browser

### Easy to Add
- Opera (add 'opera.exe')
- Vivaldi (add 'vivaldi.exe')
- Any Chromium-based browser

## Platform Support

### Required
- ✅ Windows 10/11
- ✅ ESP32 (any variant)
- ✅ Home Assistant

### Optional
- 🔲 Linux (adaptable with modifications)
- 🔲 macOS (adaptable with modifications)

## Hardware Requirements

### Minimum
- ESP32 development board (any)
- USB cable (data capable)
- Windows PC with USB port
- WiFi network (2.4 GHz)

### Optional
- Multiple monitors for TV feature
- USB power supply (for standalone ESP32)
- Status LED for visual feedback

## Software Dependencies

### ESP32
- Arduino IDE or PlatformIO
- WiFi library (built-in)
- ESPmDNS (built-in)
- AsyncTCP
- ESPAsyncWebServer
- ArduinoJson

### Windows
- Python 3.7+
- pyserial
- pywin32
- psutil

### Home Assistant
- Core (any recent version)
- RESTful Command integration (built-in)

## Performance Metrics

### Response Times
- Command execution: <100ms (local network)
- Serial communication: <10ms
- Browser window operations: <500ms
- Display on/off: <200ms
- PC sleep/wake: 1-3 seconds

### Reliability
- WiFi auto-reconnect
- Serial error handling
- Command retry on failure
- Status verification

### Resource Usage
- ESP32 memory: ~200KB
- Python script: ~30MB RAM
- Network bandwidth: <1KB per command
- No cloud dependencies

## Security Features

### Current
- Local network only
- No internet exposure
- USB serial communication
- Network isolation compatible

### Recommended
- VLAN isolation
- Firewall rules
- MAC address filtering
- Disable when not needed

### Future Enhancements
- API key authentication
- HTTPS/TLS encryption
- Rate limiting
- Access logging

## Extensibility

### Easy to Add
- Additional commands
- New browser support
- Custom automations
- Status indicators
- Multi-PC support

### Possible Extensions
- MQTT integration
- Wake-on-LAN (true power on)
- Keyboard/mouse control
- Screenshot capture
- Audio volume control
- Monitor input switching
- RGB lighting control
- Temperature monitoring

## Limitations

### Current Constraints
- Windows only (PC script)
- 2.4 GHz WiFi only (ESP32)
- Single PC per ESP32
- No authentication built-in
- Requires PC to be on for some features

### Workarounds
- Wake-on-LAN for true power on
- External power for ESP32
- Multiple ESP32 for multiple PCs
- Add authentication if needed

## Community

### Getting Help
- GitHub Issues
- Documentation
- Example code
- Troubleshooting guide

### Contributing
- Bug reports welcome
- Feature requests accepted
- Pull requests encouraged
- Documentation improvements

## Future Roadmap

### Planned Features
- MQTT support
- True Wake-on-LAN
- Multi-PC support
- Authentication
- HTTPS support

### Possible Features
- Mobile app
- Web interface
- Advanced scheduling
- Backup/restore config
- Over-the-air updates

### Community Requests
- Linux support
- macOS support
- Additional browser controls
- Gaming integration
- Smart lighting sync
