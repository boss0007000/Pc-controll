# ESP32 PC Controller for Home Assistant

A complete system that allows you to control your Windows PC and browser through Home Assistant using an ESP32 connected via USB serial.

## Features

### PC Control
- **Wake PC** - Wake from sleep/hibernation
- **Sleep PC** - Put PC to sleep
- **Display On** - Turn monitor on
- **Display Off** - Blank screen/turn monitor off

### Browser Control
- **Focus Browser** - Bring browser window to front
- **Move to TV** - Move browser window to TV monitor
- **Maximize** - Maximize browser window
- **Minimize** - Minimize browser window
- **Close** - Close browser window
- **Restore Session** - Restore last browser session
- **Open Chrome** - Launch Chrome browser
- **Open Firefox** - Launch Firefox browser
- **Open Edge** - Launch Edge browser
- **New Tab** - Open a new tab in active browser
- **Close Tab** - Close current tab
- **Next Tab** - Switch to next tab
- **Previous Tab** - Switch to previous tab
- **Reload Page** - Refresh current page
- **Hard Reload** - Refresh page bypassing cache
- **Home** - Navigate to browser home page
- **Open YouTube** - Open YouTube in default browser
- **Open Hulu** - Open Hulu in default browser
- **Open URL** - Open any specific URL

### Playback Control (Universal)
Works on YouTube, Hulu, Netflix, Prime Video, and other streaming platforms:
- **Play** - Play video
- **Pause** - Pause video
- **Toggle Play/Pause** - Toggle between play and pause
- **Stop** - Stop video (pause + exit fullscreen)
- **Restart Video** - Jump to beginning and restart
- **Seek Forward (Small)** - Seek forward 5 seconds
- **Seek Backward (Small)** - Seek backward 5 seconds
- **Seek Forward (Large)** - Seek forward 10 seconds
- **Seek Backward (Large)** - Seek backward 10 seconds
- **Jump to Beginning** - Jump to start of video
- **Jump to End** - Jump to end of video
- **Next Video** - Next video in playlist/autoplay
- **Previous Video** - Previous video in playlist

### Fullscreen & View Modes
- **Enter Fullscreen** - Enter fullscreen mode (F11)
- **Exit Fullscreen** - Exit fullscreen mode (Escape)
- **Toggle Fullscreen** - Toggle fullscreen on/off (F11)
- **Theater Mode** - Enter YouTube theater mode (T key)
- **Exit Theater Mode** - Exit YouTube theater mode
- **Picture-in-Picture Enter** - Enter PiP mode
- **Picture-in-Picture Exit** - Exit PiP mode

### Audio Control
System and browser audio controls:
- **Volume Up** - Increase system volume
- **Volume Down** - Decrease system volume
- **Mute Audio** - Mute system audio
- **Unmute Audio** - Unmute system audio
- **Toggle Mute** - Toggle mute/unmute
- **Set Volume** - Set volume to 25%, 50%, 75%, or 100%
- **Mute Browser Tab** - Mute video in browser (M key)
- **Unmute Browser Tab** - Unmute video in browser
- **Mute System Audio** - Mute all system audio
- **Restore System Audio** - Unmute all system audio

### Subtitles & Captions
- **Toggle Captions On** - Enable captions (C key)
- **Toggle Captions Off** - Disable captions
- **Cycle Caption Language** - Open caption settings (YouTube O key)
- **Increase Caption Size** - Zoom in to make captions larger
- **Decrease Caption Size** - Zoom out to make captions smaller

## Hardware Requirements

- ESP32 development board (any variant)
- USB cable to connect ESP32 to Windows PC
- Windows PC

## Software Requirements

### ESP32
- Arduino IDE (1.8.x or 2.x)
- ESP32 Board Support (via Board Manager)
- Required Libraries:
  - WiFi (built-in)
  - ESPmDNS (built-in)
  - AsyncTCP ([https://github.com/me-no-dev/AsyncTCP](https://github.com/me-no-dev/AsyncTCP))
  - ESPAsyncWebServer ([https://github.com/me-no-dev/ESPAsyncWebServer](https://github.com/me-no-dev/ESPAsyncWebServer))
  - ArduinoJson ([https://arduinojson.org/](https://arduinojson.org/))

### Windows PC
- Python 3.7 or higher
- Required Python packages (see `windows_companion/requirements.txt`):
  - pyserial
  - pywin32
  - psutil

### Home Assistant
- Home Assistant (any recent version)
- RESTful Command integration (built-in)

## Installation

### Step 1: Setup ESP32

1. **Install Arduino IDE** and ESP32 board support if not already installed.

2. **Install Required Libraries** via Arduino Library Manager:
   - AsyncTCP
   - ESPAsyncWebServer
   - ArduinoJson

3. **Configure WiFi Settings**:
   - Open `esp32_pc_controller/esp32_pc_controller.ino`
   - Update these lines with your WiFi credentials:
     ```cpp
     const char* WIFI_SSID = "YOUR_WIFI_SSID";
     const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
     ```

4. **Upload to ESP32**:
   - Connect ESP32 to your computer
   - Select the correct board and port in Arduino IDE
   - Upload the sketch

5. **Note the IP Address**:
   - Open Serial Monitor (115200 baud)
   - Note the IP address displayed after connection

### Step 2: Setup Windows PC

1. **Install Python Dependencies**:
   ```bash
   cd windows_companion
   pip install -r requirements.txt
   ```

2. **Find Serial Port**:
   - Connect ESP32 to Windows PC via USB
   - Open Device Manager → Ports (COM & LPT)
   - Note the COM port (e.g., COM3, COM4)

3. **Configure Monitor Index** (if using multiple monitors):
   - Open `windows_companion/pc_controller.py`
   - Modify `self.tv_monitor_index` to your TV monitor's index (0-based)
   - Monitor 0 is usually the primary monitor, Monitor 1 is the second, etc.

4. **Run the Controller**:
   ```bash
   python pc_controller.py --port COM3 --baud 115200
   ```
   Replace `COM3` with your actual COM port.

5. **Setup Auto-Start** (Optional):
   - Create a Windows Task Scheduler task to run the script at startup
   - Or create a shortcut in the Startup folder

### Step 3: Setup Home Assistant

1. **Add Configuration**:
   - Copy the contents of `home_assistant/configuration.yaml`
   - Add to your Home Assistant `configuration.yaml`
   - Update the URL if not using mDNS (replace `esp32-pc-controller.local` with the ESP32's IP address)

2. **Restart Home Assistant**:
   - Configuration → Server Controls → Restart

3. **Test Commands**:
   - Go to Developer Tools → Services
   - Try calling services like `rest_command.pc_wake`

4. **Add to Dashboard** (Optional):
   - Add a new card to your Lovelace dashboard
   - Use the example configuration at the end of `home_assistant/configuration.yaml`

## Usage

### Via Home Assistant UI
Use the button entities in your dashboard or automation editor.

### Via Home Assistant Automations
Example automation to turn on display when you get home:
```yaml
automation:
  - alias: "Turn on PC display when home"
    trigger:
      - platform: state
        entity_id: person.you
        to: 'home'
    action:
      - action: rest_command.display_on
```

### Via REST API
Send HTTP POST requests directly to the ESP32:
```bash
curl -X POST http://esp32-pc-controller.local/pc/wake
curl -X POST http://esp32-pc-controller.local/browser/maximize
curl -X POST http://esp32-pc-controller.local/browser/new-tab
curl -X POST http://esp32-pc-controller.local/browser/open-youtube
curl -X POST -d "url=https://www.netflix.com" http://esp32-pc-controller.local/browser/open-url
```

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Device status (JSON) |
| `/status` | GET | Device status (JSON) |
| `/pc/wake` | POST | Wake PC |
| `/pc/sleep` | POST | Sleep PC |
| `/display/on` | POST | Turn display on |
| `/display/off` | POST | Turn display off |
| `/browser/focus` | POST | Focus browser window |
| `/browser/move-tv` | POST | Move browser to TV monitor |
| `/browser/maximize` | POST | Maximize browser |
| `/browser/minimize` | POST | Minimize browser |
| `/browser/close` | POST | Close browser |
| `/browser/restore` | POST | Restore browser session |
| `/browser/open-chrome` | POST | Open Chrome browser |
| `/browser/open-firefox` | POST | Open Firefox browser |
| `/browser/open-edge` | POST | Open Edge browser |
| `/browser/new-tab` | POST | Open new tab |
| `/browser/close-tab` | POST | Close current tab |
| `/browser/next-tab` | POST | Switch to next tab |
| `/browser/prev-tab` | POST | Switch to previous tab |
| `/browser/reload` | POST | Reload current page |
| `/browser/hard-reload` | POST | Hard reload (bypass cache) |
| `/browser/home` | POST | Navigate to home page |
| `/browser/open-url` | POST | Open specific URL (param: `url`) |
| `/browser/open-youtube` | POST | Open YouTube |
| `/browser/open-hulu` | POST | Open Hulu |
| `/playback/play` | POST | Play video |
| `/playback/pause` | POST | Pause video |
| `/playback/play-pause` | POST | Toggle play/pause |
| `/playback/stop` | POST | Stop video (pause + exit fullscreen) |
| `/playback/restart` | POST | Restart video from beginning |
| `/playback/seek-forward-small` | POST | Seek forward 5 seconds |
| `/playback/seek-backward-small` | POST | Seek backward 5 seconds |
| `/playback/seek-forward-large` | POST | Seek forward 10 seconds |
| `/playback/seek-backward-large` | POST | Seek backward 10 seconds |
| `/playback/jump-to-beginning` | POST | Jump to video start |
| `/playback/jump-to-end` | POST | Jump to video end |
| `/playback/next-video` | POST | Next video in playlist |
| `/playback/previous-video` | POST | Previous video in playlist |
| `/fullscreen/enter` | POST | Enter fullscreen mode |
| `/fullscreen/exit` | POST | Exit fullscreen mode |
| `/fullscreen/toggle` | POST | Toggle fullscreen |
| `/theater-mode` | POST | Enter theater mode (YouTube) |
| `/theater-mode/exit` | POST | Exit theater mode |
| `/picture-in-picture/enter` | POST | Enter picture-in-picture |
| `/picture-in-picture/exit` | POST | Exit picture-in-picture |
| `/audio/volume-up` | POST | Increase system volume |
| `/audio/volume-down` | POST | Decrease system volume |
| `/audio/mute` | POST | Mute system audio |
| `/audio/unmute` | POST | Unmute system audio |
| `/audio/toggle-mute` | POST | Toggle mute/unmute |
| `/audio/volume-set` | POST | Set volume level (param: `level`) |
| `/audio/browser-tab-mute` | POST | Mute browser tab |
| `/audio/browser-tab-unmute` | POST | Unmute browser tab |
| `/audio/system-mute-all` | POST | Mute all system audio |
| `/audio/system-audio-restore` | POST | Restore system audio |
| `/captions/toggle-on` | POST | Toggle captions on |
| `/captions/toggle-off` | POST | Toggle captions off |
| `/captions/cycle-language` | POST | Cycle caption languages |
| `/captions/size-increase` | POST | Increase caption size |
| `/captions/size-decrease` | POST | Decrease caption size |
| `/command` | POST | Send custom command (param: `cmd`) |

## Architecture

```
Home Assistant
    ↓ (WiFi - HTTP POST)
ESP32 (Web Server)
    ↓ (USB Serial)
Windows PC (Python Script)
    ↓ (Windows API)
PC/Display/Browser
```

1. Home Assistant sends HTTP POST requests to ESP32 over WiFi
2. ESP32 receives request and sends command via Serial to Windows PC
3. Python script on Windows receives command and executes via Windows API
4. Python script sends status response back to ESP32 via Serial
5. ESP32 can report status back to Home Assistant

## Troubleshooting

### ESP32 Won't Connect to WiFi
- Check SSID and password in the sketch
- Ensure WiFi network is 2.4GHz (ESP32 doesn't support 5GHz)
- Check Serial Monitor for error messages

### Python Script Can't Open Serial Port
- Verify correct COM port in Device Manager
- Close any other programs using the serial port (Arduino IDE Serial Monitor, etc.)
- Try different USB cable or USB port

### Commands Not Working on Windows
- Ensure Python script is running with proper permissions
- Check if pywin32 is properly installed: `python -c "import win32api"`
- For display control, some systems may need additional drivers

### Browser Commands Not Finding Browser
- Make sure browser is running
- Check supported browsers in `pc_controller.py`
- Add your browser's process name to `self.browser_process_names`

### Home Assistant Can't Reach ESP32
- Check if ESP32 IP is correct
- Try using IP address instead of mDNS name
- Ensure Home Assistant and ESP32 are on same network/VLAN

## Customization

### Adding More Commands
1. Add new endpoint in ESP32 sketch (`setupWebServer()`)
2. Add new command handler in `pc_controller.py`
3. Update command mapping in `pc_controller.py`'s `main()`
4. Add corresponding Home Assistant configuration

### Changing Browser
Edit `self.browser_process_names` in `pc_controller.py` to add/remove browsers.

### Wake-on-LAN
For true Wake-on-LAN (waking from powered off state):
- Enable WOL in BIOS
- Enable WOL in Network Adapter settings
- Implement WOL magic packet sending in ESP32 sketch

## Security Notes

- This system operates on your local network only
- Consider adding authentication to ESP32 web server for production use
- The serial communication is not encrypted
- Be cautious with sleep/wake commands in automations

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions welcome! Please submit pull requests or open issues for bugs and feature requests.