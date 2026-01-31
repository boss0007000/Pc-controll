# Quick Start Guide

This guide will get you up and running in 15 minutes.

## Prerequisites Check

Before starting, ensure you have:
- ✅ ESP32 development board
- ✅ USB cable (data cable)
- ✅ Windows PC
- ✅ Arduino IDE installed
- ✅ Python 3.7+ installed
- ✅ Home Assistant running
- ✅ WiFi network (2.4 GHz)

## Step-by-Step Setup

### 1️⃣ ESP32 Setup (5 minutes)

1. **Install ESP32 Board Support**
   - Open Arduino IDE
   - Go to File → Preferences
   - Add to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Boards Manager
   - Search "esp32" and install "esp32 by Espressif Systems"

2. **Install Required Libraries**
   - Open Library Manager (Tools → Manage Libraries)
   - Install these libraries:
     - `AsyncTCP` by dvarrel (or me-no-dev)
     - `ESPAsyncWebServer` by me-no-dev  
     - `ArduinoJson` by Benoit Blanchon

3. **Configure and Upload**
   - Open `esp32_pc_controller/esp32_pc_controller.ino`
   - Edit WiFi credentials:
     ```cpp
     const char* WIFI_SSID = "YourWiFiName";
     const char* WIFI_PASSWORD = "YourPassword";
     ```
   - Connect ESP32 via USB
   - Select Tools → Board → Your ESP32 board
   - Select Tools → Port → Your COM port
   - Click Upload (→)
   - Open Serial Monitor (115200 baud)
   - **Note the IP address shown**

### 2️⃣ Windows PC Setup (3 minutes)

1. **Install Python Packages**
   ```cmd
   cd windows_companion
   pip install -r requirements.txt
   ```

2. **Find COM Port**
   - Open Device Manager
   - Expand "Ports (COM & LPT)"
   - Note the COM port (e.g., COM3)

3. **Run the Controller**
   ```cmd
   python pc_controller.py --port COM3
   ```
   Replace COM3 with your actual port.
   
   You should see:
   ```
   PC Controller starting...
   Connected to COM3
   Waiting for commands...
   ```

### 3️⃣ Home Assistant Setup (5 minutes)

1. **Add Configuration**
   - Edit Home Assistant's `configuration.yaml`
   - Add the contents from `home_assistant/configuration.yaml`
   - **Important**: Replace `esp32-pc-controller.local` with the IP address you noted in Step 1 if mDNS doesn't work

2. **Restart Home Assistant**
   - Configuration → Server Controls → Check Configuration
   - If OK, click "Restart"

3. **Test a Command**
   - Go to Developer Tools → Services
   - Select `rest_command.display_on`
   - Click "Call Service"
   - Your display should turn on!

### 4️⃣ Verify Everything Works (2 minutes)

Test each command from Home Assistant Developer Tools:
- ✅ `rest_command.display_on` - Display turns on
- ✅ `rest_command.display_off` - Display turns off
- ✅ `rest_command.pc_sleep` - PC goes to sleep
- ✅ `rest_command.pc_wake` - PC wakes up

## First-Time Configuration

### Configure TV Monitor Index

If you have multiple monitors:

1. Open `windows_companion/pc_controller.py`
2. Find this line:
   ```python
   self.tv_monitor_index = 1
   ```
3. Change to your TV's monitor index (0 = first monitor, 1 = second, etc.)

### Configure Browser

The script supports Chrome, Firefox, Edge, and Brave by default. To add more:

1. Open `windows_companion/pc_controller.py`
2. Find:
   ```python
   self.browser_process_names = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe']
   ```
3. Add your browser's executable name

## Quick Test Commands

Open a command prompt or PowerShell and test the ESP32 directly:

```bash
# Test status endpoint
curl http://YOUR-ESP32-IP/status

# Test wake command
curl -X POST http://YOUR-ESP32-IP/pc/wake

# Test browser focus
curl -X POST http://YOUR-ESP32-IP/browser/focus
```

## Common Issues & Quick Fixes

### ESP32 Won't Upload
- ❌ **Problem**: Upload fails with "Failed to connect to ESP32"
- ✅ **Solution**: Hold down BOOT button on ESP32 while clicking Upload

### Python Script Won't Start
- ❌ **Problem**: `Access is denied` on COM port
- ✅ **Solution**: Close Arduino Serial Monitor or other programs using the port

### Home Assistant Can't Reach ESP32
- ❌ **Problem**: Commands timeout or fail
- ✅ **Solution**: Use IP address instead of `esp32-pc-controller.local` in configuration

### Commands Do Nothing
- ❌ **Problem**: Commands execute but nothing happens
- ✅ **Solution**: Ensure Python script is running on Windows PC

### Browser Commands Don't Work
- ❌ **Problem**: "Browser not found" messages
- ✅ **Solution**: Open your browser first, then try again

## Auto-Start Python Script (Optional)

### Using Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Name: "ESP32 PC Controller"
4. Trigger: "When I log on"
5. Action: "Start a program"
6. Program: `C:\Python\python.exe` (your Python path)
7. Arguments: `C:\path\to\pc_controller.py --port COM3`
8. Finish

### Using Startup Folder

1. Create a `.bat` file:
   ```batch
   @echo off
   cd C:\path\to\windows_companion
   python pc_controller.py --port COM3
   pause
   ```
2. Save as `start_pc_controller.bat`
3. Press Win+R, type `shell:startup`
4. Copy the `.bat` file there

## Creating a Home Assistant Dashboard

Add this to your Lovelace dashboard:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: PC Control
    entities:
      - button.pc_wake_button
      - button.pc_sleep_button
      - button.display_on_button
      - button.display_off_button
  
  - type: entities
    title: Browser Control
    entities:
      - button.browser_focus_button
      - button.browser_tv_button
      - button.browser_maximize_button
      - button.browser_minimize_button
      - button.browser_close_button
      - button.browser_restore_button
  
  - type: sensor
    entity: sensor.pc_controller_status
```

## Example Automations

### Wake PC and Open Browser in Morning

```yaml
automation:
  - alias: "Morning PC Routine"
    trigger:
      - platform: time
        at: "07:00:00"
    condition:
      - condition: state
        entity_id: person.you
        state: 'home'
    action:
      - action: rest_command.pc_wake
      - delay: "00:00:30"
      - action: rest_command.display_on
      - delay: "00:00:05"
      - action: rest_command.browser_restore
```

### Turn Off Display When Away

```yaml
automation:
  - alias: "Turn off display when leaving"
    trigger:
      - platform: state
        entity_id: person.you
        to: 'not_home'
    action:
      - action: rest_command.display_off
```

### Movie Mode - Browser to TV

```yaml
script:
  movie_mode:
    alias: "Movie Mode"
    sequence:
      - action: rest_command.browser_focus
      - delay: "00:00:02"
      - action: rest_command.browser_move_tv
      - delay: "00:00:01"
      - action: rest_command.browser_maximize
```

## What's Next?

- 📱 Add mobile app shortcuts to Home Assistant
- 🎮 Create scenes for gaming, work, movies
- 🔊 Integrate with voice assistants (Alexa, Google Home)
- 🤖 Build complex automations
- 🔒 Add authentication to ESP32 web server
- 📊 Monitor PC status with sensors

## Need Help?

1. Check the main README.md for detailed documentation
2. Check WIRING.md for connection details
3. Open an issue on GitHub
4. Check the serial monitor output for errors

## Success Checklist

- [ ] ESP32 connects to WiFi and shows IP address
- [ ] Python script connects to serial port
- [ ] Home Assistant can reach ESP32
- [ ] At least one command works successfully
- [ ] Python script auto-starts with Windows (optional)
- [ ] Dashboard created in Home Assistant (optional)

**Congratulations! Your ESP32 PC Controller is now set up!** 🎉
