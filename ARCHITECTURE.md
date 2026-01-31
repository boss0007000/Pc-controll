# System Architecture

## High-Level Overview

```
┌────────────────────────────────────────────────────────────────┐
│                        User Interface                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ HA Dashboard │  │ Voice Control│  │  Automation  │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Home Assistant  │
                    │   (REST API)    │
                    └────────┬────────┘
                             │
                  WiFi (HTTP POST Requests)
                             │
                    ┌────────▼────────┐
                    │     ESP32       │
                    │  Web Server     │
                    │  (AsyncWeb)     │
                    └────────┬────────┘
                             │
                  USB Serial (115200 baud)
                             │
                    ┌────────▼────────┐
                    │  Windows PC     │
                    │ Python Script   │
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
        ┌───────▼─────┐  ┌──▼────┐  ┌───▼────────┐
        │   Display   │  │  PC   │  │  Browser   │
        │   Control   │  │ Power │  │  Control   │
        └─────────────┘  └───────┘  └────────────┘
```

## Detailed Component Architecture

### ESP32 Module

```
┌─────────────────────────────────────────┐
│           ESP32 Firmware                │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │       WiFi Connection            │  │
│  │  - Connects to home network      │  │
│  │  - Auto-reconnect on failure     │  │
│  │  - mDNS for easy discovery       │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │      Web Server (AsyncWeb)       │  │
│  │  Endpoints:                      │  │
│  │  - /status (GET)                 │  │
│  │  - /pc/wake (POST)               │  │
│  │  - /pc/sleep (POST)              │  │
│  │  - /display/on (POST)            │  │
│  │  - /display/off (POST)           │  │
│  │  - /browser/* (POST)             │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    Serial Communication          │  │
│  │  - TX: Send commands to PC       │  │
│  │  - RX: Receive status from PC    │  │
│  │  - 115200 baud, 8N1              │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │      Status Tracking             │  │
│  │  - PC awake state                │  │
│  │  - Display state                 │  │
│  │  - Last command executed         │  │
│  │  - WiFi signal strength          │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Windows PC Module

```
┌─────────────────────────────────────────┐
│      Windows Companion Script           │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Serial Port Listener           │  │
│  │  - Monitors COM port             │  │
│  │  - Parses incoming commands      │  │
│  │  - Sends status responses        │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Command Handlers               │  │
│  │                                  │  │
│  │  PC Control:                     │  │
│  │  - wake_pc()                     │  │
│  │  - sleep_pc()                    │  │
│  │                                  │  │
│  │  Display Control:                │  │
│  │  - display_on()                  │  │
│  │  - display_off()                 │  │
│  │                                  │  │
│  │  Browser Control:                │  │
│  │  - browser_focus()               │  │
│  │  - browser_move_tv()             │  │
│  │  - browser_maximize()            │  │
│  │  - browser_minimize()            │  │
│  │  - browser_close()               │  │
│  │  - browser_restore()             │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │   Windows API Integration        │  │
│  │  - win32api (Power control)      │  │
│  │  - win32gui (Window management)  │  │
│  │  - psutil (Process detection)    │  │
│  │  - ctypes (Low-level APIs)       │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Home Assistant Integration

```
┌─────────────────────────────────────────┐
│        Home Assistant Config            │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    RESTful Commands              │  │
│  │  - rest_command.pc_wake          │  │
│  │  - rest_command.pc_sleep         │  │
│  │  - rest_command.display_on       │  │
│  │  - rest_command.display_off      │  │
│  │  - rest_command.browser_*        │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    Sensors                       │  │
│  │  - sensor.pc_controller_status   │  │
│  │    (JSON attributes: IP, uptime, │  │
│  │     WiFi RSSI, states, etc.)     │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    Button Entities               │  │
│  │  - button.pc_wake_button         │  │
│  │  - button.pc_sleep_button        │  │
│  │  - button.display_*_button       │  │
│  │  - button.browser_*_button       │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │    Automations (Examples)        │  │
│  │  - Morning routine               │  │
│  │  - Bedtime routine               │  │
│  │  - Presence detection            │  │
│  │  - Movie mode                    │  │
│  │  - Voice commands                │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Data Flow

### Example: Wake PC Command

```
1. User Action
   ├─> Dashboard button click
   ├─> Voice command "Wake my PC"
   ├─> Automation trigger
   └─> Manual service call

2. Home Assistant
   ├─> Receives action
   ├─> Calls rest_command.pc_wake
   └─> Sends HTTP POST to ESP32
       URL: http://esp32-pc-controller.local/pc/wake

3. ESP32
   ├─> Web server receives POST request
   ├─> Executes executeCommand("PC_WAKE")
   ├─> Sends "PC_WAKE\n" via Serial TX
   ├─> Returns HTTP 200 {"status":"ok"}
   └─> Updates lastCommand state

4. Windows PC
   ├─> Python script reads from Serial
   ├─> Parses command: "PC_WAKE"
   ├─> Calls controller.wake_pc()
   ├─> Executes Windows API calls
   │   ├─> Move mouse cursor
   │   └─> Trigger mouse event
   ├─> Sends response via Serial
   └─> "STATUS:PC_WAKE executed\n"

5. ESP32
   ├─> Receives status response
   ├─> Updates pcAwake state
   └─> Available via /status endpoint

6. Result
   └─> PC wakes from sleep
```

### Example: Move Browser to TV

```
1. User triggers "Movie Mode" automation

2. Home Assistant
   ├─> Calls rest_command.browser_focus
   ├─> Waits 2 seconds
   ├─> Calls rest_command.browser_move_tv
   ├─> Waits 1 second
   └─> Calls rest_command.browser_maximize

3. ESP32 (for each command)
   ├─> Receives HTTP POST
   ├─> Forwards to PC via Serial
   └─> Returns success

4. Windows PC
   ├─> Receives BROWSER_FOCUS
   │   ├─> Finds browser windows
   │   ├─> Restores if minimized
   │   └─> Brings to foreground
   │
   ├─> Receives BROWSER_MOVE_TV
   │   ├─> Enumerates displays
   │   ├─> Gets TV monitor coordinates
   │   ├─> Moves window to TV
   │   └─> Resizes to fit screen
   │
   └─> Receives BROWSER_MAXIMIZE
       └─> Maximizes browser window

5. Result
   └─> Browser is now fullscreen on TV
```

## Communication Protocol

### Serial Commands (ESP32 → PC)

```
Command Format: COMMAND_NAME\n

Available Commands:
- PC_WAKE
- PC_SLEEP
- DISPLAY_ON
- DISPLAY_OFF
- BROWSER_FOCUS
- BROWSER_MOVE_TV
- BROWSER_MAXIMIZE
- BROWSER_MINIMIZE
- BROWSER_CLOSE
- BROWSER_RESTORE
```

### Serial Responses (PC → ESP32)

```
Response Format: STATUS:message\n or ERROR:message\n

Examples:
STATUS:PC_WAKE executed
STATUS:BROWSER_FOCUS executed on chrome.exe
ERROR:BROWSER_CLOSE failed - no browser found
```

### HTTP API (Home Assistant → ESP32)

```
Endpoints:
GET  /                 → Device status JSON
GET  /status           → Device status JSON
POST /pc/wake          → Execute PC_WAKE
POST /pc/sleep         → Execute PC_SLEEP
POST /display/on       → Execute DISPLAY_ON
POST /display/off      → Execute DISPLAY_OFF
POST /browser/focus    → Execute BROWSER_FOCUS
POST /browser/move-tv  → Execute BROWSER_MOVE_TV
POST /browser/maximize → Execute BROWSER_MAXIMIZE
POST /browser/minimize → Execute BROWSER_MINIMIZE
POST /browser/close    → Execute BROWSER_CLOSE
POST /browser/restore  → Execute BROWSER_RESTORE
POST /command?cmd=XXX  → Execute custom command

Response Format (JSON):
{
  "status": "ok",
  "command": "PC_WAKE"
}

Status Response (JSON):
{
  "device": "esp32-pc-controller",
  "ip": "192.168.1.100",
  "mac": "AA:BB:CC:DD:EE:FF",
  "uptime": 12345,
  "wifi_rssi": -65,
  "pc_awake": true,
  "display_on": true,
  "last_command": "PC_WAKE",
  "last_command_time": 12340
}
```

## Security Considerations

```
┌─────────────────────────────────────────┐
│          Security Layers                │
├─────────────────────────────────────────┤
│                                         │
│  Network Layer:                         │
│  - Local network only                   │
│  - No internet exposure                 │
│  - WiFi encryption (WPA2/WPA3)          │
│                                         │
│  Application Layer:                     │
│  - No authentication (local trust)      │
│  - Could add API keys if needed         │
│  - Could add HTTPS/TLS                  │
│                                         │
│  Physical Layer:                        │
│  - USB serial (PC must be accessible)   │
│  - ESP32 must be plugged into PC        │
│                                         │
│  Recommendations:                       │
│  - Isolate on trusted VLAN              │
│  - Use firewall rules                   │
│  - Add authentication for production    │
│  - Monitor access logs                  │
└─────────────────────────────────────────┘
```

## Scalability & Extensions

### Multiple PC Support

```
┌─────────────┐
│ Home        │
│ Assistant   │
└──────┬──────┘
       │
       ├──────────┬──────────┬
       │          │          │
   ┌───▼────┐ ┌──▼────┐ ┌───▼────┐
   │ ESP32  │ │ESP32  │ │ ESP32  │
   │   #1   │ │  #2   │ │   #3   │
   └───┬────┘ └──┬────┘ └───┬────┘
       │         │           │
   ┌───▼────┐ ┌──▼────┐ ┌───▼────┐
   │  PC 1  │ │ PC 2  │ │  PC 3  │
   │(Office)│ │(Living)│ │(Bedroom)│
   └────────┘ └───────┘ └────────┘
```

Use different device names:
- esp32-office-pc
- esp32-living-pc
- esp32-bedroom-pc

### Additional Features to Add

- MQTT support for better HA integration
- Wake-on-LAN for true power-on
- Keyboard/mouse control
- Screenshot capture
- Audio control
- Monitor input switching
- Multi-monitor management
- Gaming profile switching
- Scheduled tasks
- Notification support
