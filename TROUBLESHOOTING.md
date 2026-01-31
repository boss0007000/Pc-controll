# Troubleshooting Guide

This guide covers common issues and their solutions.

## ESP32 Issues

### ESP32 Won't Connect to WiFi

**Symptoms:**
- Serial monitor shows "Failed to connect to WiFi"
- ESP32 keeps printing dots (...) endlessly

**Solutions:**

1. **Check WiFi Credentials**
   ```cpp
   const char* WIFI_SSID = "YourNetworkName";
   const char* WIFI_PASSWORD = "YourPassword";
   ```
   - Ensure no typos
   - Check for extra spaces
   - Password is case-sensitive

2. **Check WiFi Band**
   - ESP32 only supports 2.4 GHz WiFi
   - Disable 5 GHz on dual-band routers or separate SSIDs

3. **Check WiFi Signal**
   - Move ESP32 closer to router
   - Check for interference from metal objects

4. **Router Settings**
   - Ensure WiFi is not hidden
   - Check if MAC filtering is enabled
   - Try disabling AP isolation

### ESP32 Upload Failed

**Symptoms:**
- "Failed to connect to ESP32: Timed out"
- "Serial port not found"

**Solutions:**

1. **Driver Issues**
   - Install CP210x or CH340 drivers
   - Windows: Check Device Manager for "Unknown Device"
   - Try different USB cable

2. **Manual Boot Mode**
   - Hold BOOT button
   - Press RESET button
   - Release RESET
   - Release BOOT after upload starts

3. **Upload Settings**
   ```
   Tools → Upload Speed → 115200 (slower but more reliable)
   Tools → Flash Frequency → 40MHz
   ```

### ESP32 Keeps Rebooting

**Symptoms:**
- Constant restart loop
- "Brownout detector" messages

**Solutions:**

1. **Power Issues**
   - Use quality USB cable
   - Try different USB port
   - Use external 5V power supply

2. **Code Issues**
   - Check for infinite loops
   - Reduce WiFi transmission power
   - Add delays in loop()

### ESP32 Web Server Not Responding

**Symptoms:**
- Can't access http://esp32-pc-controller.local
- HTTP requests timeout

**Solutions:**

1. **Use IP Address Instead**
   - Check serial monitor for IP
   - Replace .local with actual IP in Home Assistant config

2. **Network Issues**
   - Ping the ESP32 IP address
   - Check firewall settings
   - Ensure same subnet as Home Assistant

3. **DNS/mDNS Issues**
   ```cpp
   // In setup(), after WiFi.begin():
   Serial.print("IP address: ");
   Serial.println(WiFi.localIP());
   ```

## Windows PC Issues

### Python Script Can't Open Serial Port

**Symptoms:**
- "Access is denied" error
- "Serial port not found"

**Solutions:**

1. **Port Already in Use**
   - Close Arduino Serial Monitor
   - Close other terminal programs
   - Check Task Manager for other Python instances

2. **Wrong COM Port**
   ```cmd
   # List available ports
   python -m serial.tools.list_ports
   ```

3. **Permissions**
   - Run command prompt as Administrator
   - Check Device Manager → Properties → Power Management

4. **USB Cable Issues**
   - Try different USB port
   - Use USB 2.0 port instead of 3.0
   - Replace USB cable

### Python Dependencies Won't Install

**Symptoms:**
- pip install fails
- Import errors in Python script

**Solutions:**

1. **Install Visual C++ Build Tools**
   - Required for pywin32
   - Download from Microsoft website

2. **Use Pre-compiled Wheels**
   ```cmd
   pip install --upgrade pip
   pip install pywin32 --upgrade
   python -m pywin32_postinstall -install
   ```

3. **Python Version**
   - Use Python 3.7-3.11 (avoid 3.12+ if issues)
   - Verify: `python --version`

### Commands Execute But Nothing Happens

**Symptoms:**
- Python script receives commands
- No error messages
- PC doesn't respond

**Solutions:**

1. **Test Individual Functions**
   ```python
   # In pc_controller.py, add at end of __init__:
   self.display_on()  # Test if display control works
   ```

2. **Windows API Issues**
   ```cmd
   # Test pywin32 installation
   python -c "import win32api; print('OK')"
   ```

3. **User Permissions**
   - Run Python script as Administrator
   - Check UAC settings

4. **Sleep/Hibernate Settings**
   - Windows Settings → Power & Sleep
   - Disable "Fast Startup"
   - Enable "Allow USB to wake PC"

### Browser Commands Don't Work

**Symptoms:**
- "Browser not found" messages
- Browser window doesn't respond

**Solutions:**

1. **Browser Not Running**
   - Open browser before testing
   - Check if browser process is visible in Task Manager

2. **Add Your Browser**
   ```python
   self.browser_process_names = [
       'chrome.exe', 
       'firefox.exe', 
       'msedge.exe', 
       'brave.exe',
       'opera.exe',  # Add your browser
   ]
   ```

3. **Multiple Browser Windows**
   - Script focuses first found window
   - Close extra browser windows
   - Modify script to find specific window by title

4. **Window Focus Issues**
   ```python
   # Add after SetForegroundWindow:
   win32gui.BringWindowToTop(hwnd)
   win32gui.SetActiveWindow(hwnd)
   ```

### Display Control Doesn't Work

**Symptoms:**
- Display stays on/off
- No response to display commands

**Solutions:**

1. **Monitor Settings**
   - Check if monitor supports DPMS
   - Try different monitor power settings
   - Some monitors ignore software commands

2. **Alternative Method**
   ```python
   # Use nircmd.exe instead
   subprocess.run(['nircmd.exe', 'monitor', 'off'])
   subprocess.run(['nircmd.exe', 'monitor', 'on'])
   ```

3. **Graphics Driver**
   - Update display drivers
   - Check power management settings

## Home Assistant Issues

### Home Assistant Can't Reach ESP32

**Symptoms:**
- Services timeout
- "Connection refused" errors

**Solutions:**

1. **Network Connectivity**
   ```bash
   # From Home Assistant terminal
   ping ESP32_IP_ADDRESS
   curl http://ESP32_IP_ADDRESS/status
   ```

2. **Firewall**
   - Check Windows Firewall
   - Allow Python script through firewall
   - Check router firewall

3. **Configuration**
   ```yaml
   # Use IP instead of mDNS
   rest_command:
     pc_wake:
       url: "http://192.168.1.100/pc/wake"  # Use actual IP
       method: POST
       timeout: 10  # Increase timeout
   ```

4. **Network Segmentation**
   - Ensure ESP32 and HA on same VLAN
   - Check if AP isolation is enabled
   - Try connecting to same WiFi network

### Services Don't Execute

**Symptoms:**
- Service calls succeed but nothing happens
- No errors in logs

**Solutions:**

1. **Check Entity Names**
   ```yaml
   # In automations:
   action:
     - action: rest_command.pc_wake  # Correct
     - service: rest_command.pc_wake  # Old syntax
   ```

2. **Configuration Validation**
   - Configuration → Server Controls → Check Configuration
   - Look for YAML errors

3. **Restart Required**
   - Restart Home Assistant after config changes
   - Clear browser cache

### Button Entities Not Showing

**Symptoms:**
- Buttons don't appear in UI
- Can't find button entities

**Solutions:**

1. **Old Home Assistant Version**
   - Button platform requires HA 2021.12+
   - Update Home Assistant
   - Or use input_boolean instead

2. **Template Format**
   ```yaml
   # Use correct template format for your HA version
   button:
     - platform: template
       buttons:  # Note the 's'
         pc_wake_button:
           # ...
   ```

## Serial Communication Issues

### Commands Not Received by PC

**Symptoms:**
- ESP32 sends commands (visible in serial monitor)
- Python script doesn't receive them

**Solutions:**

1. **Baud Rate Mismatch**
   ```cpp
   // ESP32
   Serial.begin(115200);
   ```
   ```python
   # Python
   ser = serial.Serial(args.port, 115200)
   ```

2. **Line Endings**
   - ESP32 sends `\n`
   - Python reads until `\n`
   - Match line ending settings

3. **Buffer Issues**
   ```python
   # In Python script, add:
   ser.reset_input_buffer()
   ser.reset_output_buffer()
   ```

### Garbled Serial Data

**Symptoms:**
- Random characters
- Incomplete commands

**Solutions:**

1. **Check Baud Rate**
   - Ensure match on both sides
   - Try lower baud rate (9600)

2. **USB Cable Quality**
   - Use shielded cable
   - Keep cable away from power cables
   - Try shorter cable

3. **Timing Issues**
   ```python
   # Add delays
   time.sleep(2)  # After opening serial port
   ```

## Multiple Monitor Issues

### Browser Moves to Wrong Monitor

**Symptoms:**
- Browser doesn't move to TV
- Moves to wrong display

**Solutions:**

1. **Check Monitor Index**
   ```python
   # Print available monitors
   def browser_move_tv(self):
       monitors = []
       # ... enumerate monitors ...
       print(f"Found {len(monitors)} monitors:")
       for i, m in enumerate(monitors):
           print(f"Monitor {i}: {m}")
   ```

2. **Monitor Numbers Change**
   - Windows assigns monitor IDs dynamically
   - TV must be connected and powered on
   - Check Display Settings → Identify

3. **Window Position**
   ```python
   # Debug window position
   rect = win32gui.GetWindowRect(hwnd)
   print(f"Window at: {rect}")
   ```

## Performance Issues

### Slow Response Times

**Symptoms:**
- Commands take long to execute
- Timeouts

**Solutions:**

1. **Network Latency**
   - Check WiFi signal strength
   - Move ESP32 closer to router
   - Use 5 GHz WiFi for Home Assistant (ESP32 stays on 2.4)

2. **PC Performance**
   - Close background applications
   - Check CPU/RAM usage
   - Update Windows

3. **Increase Timeouts**
   ```yaml
   # In Home Assistant
   rest_command:
     pc_wake:
       url: "http://esp32/pc/wake"
       timeout: 30  # Increase from default 10
   ```

## Debugging Tools

### Enable Debug Logging

**ESP32:**
```cpp
// Add to setup()
Serial.setDebugOutput(true);
```

**Python:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Home Assistant:**
```yaml
logger:
  default: info
  logs:
    homeassistant.components.rest_command: debug
```

### Test Commands Manually

**Test ESP32 directly:**
```bash
curl -v -X POST http://192.168.1.100/pc/wake
```

**Test serial communication:**
```python
# In Python console
import serial
ser = serial.Serial('COM3', 115200)
ser.write(b'PC_WAKE\n')
response = ser.readline()
print(response)
```

### Monitor Serial Traffic

Use a serial monitor tool:
- Arduino Serial Monitor
- PuTTY (Serial mode)
- Tera Term
- Serial Port Monitor

## Getting More Help

If issues persist:

1. **Check Logs**
   - ESP32 Serial Monitor output
   - Python script console output
   - Home Assistant logs

2. **Provide Information**
   - ESP32 board model
   - Windows version
   - Home Assistant version
   - Error messages
   - Steps to reproduce

3. **Test Incrementally**
   - Test ESP32 alone
   - Test Python script alone
   - Test Home Assistant alone
   - Combine components

4. **Open GitHub Issue**
   - Include version information
   - Attach relevant logs
   - Describe expected vs actual behavior
