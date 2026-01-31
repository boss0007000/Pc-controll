# Browser Commands Quick Reference

This document provides a quick reference for all the new browser control commands added to the ESP32 PC Controller.

## Browser Application Control

### Open Chrome
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/open-chrome

# Home Assistant
service: rest_command.browser_open_chrome
```

### Open Firefox
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/open-firefox

# Home Assistant
service: rest_command.browser_open_firefox
```

### Open Edge
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/open-edge

# Home Assistant
service: rest_command.browser_open_edge
```

## Tab Management

### Open New Tab
Opens a new tab in the currently active browser window.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/new-tab

# Home Assistant
service: rest_command.browser_new_tab
```

### Close Current Tab
Closes the currently active tab.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/close-tab

# Home Assistant
service: rest_command.browser_close_tab
```

### Switch to Next Tab
Switches to the next tab (Ctrl+Tab).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/next-tab

# Home Assistant
service: rest_command.browser_next_tab
```

### Switch to Previous Tab
Switches to the previous tab (Ctrl+Shift+Tab).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/prev-tab

# Home Assistant
service: rest_command.browser_prev_tab
```

## Page Control

### Reload Page
Reloads the current page (F5).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/reload

# Home Assistant
service: rest_command.browser_reload
```

### Hard Reload Page
Reloads the current page bypassing cache (Ctrl+F5).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/hard-reload

# Home Assistant
service: rest_command.browser_hard_reload
```

### Navigate to Home Page
Navigates to the browser's home page (Alt+Home).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/home

# Home Assistant
service: rest_command.browser_home
```

## URL Navigation

### Open Specific URL
Opens any URL in the default browser.
```bash
# REST API
curl -X POST -d "url=https://www.example.com" http://esp32-pc-controller.local/browser/open-url

# Home Assistant
service: rest_command.browser_open_url
data:
  url: "https://www.example.com"
```

### Open YouTube
Quick shortcut to open YouTube.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/open-youtube

# Home Assistant
service: rest_command.browser_open_youtube
```

### Open Hulu
Quick shortcut to open Hulu.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/open-hulu

# Home Assistant
service: rest_command.browser_open_hulu
```

## Common Use Cases

### Morning Routine - Open Multiple Sites
```yaml
automation:
  - alias: "Morning News Setup"
    trigger:
      - platform: time
        at: "07:30:00"
    action:
      - service: rest_command.browser_open_chrome
      - delay:
          seconds: 3
      - service: rest_command.browser_open_url
        data:
          url: "https://news.google.com"
      - delay:
          seconds: 2
      - service: rest_command.browser_new_tab
      - delay:
          seconds: 1
      - service: rest_command.browser_open_url
        data:
          url: "https://www.weather.com"
```

### Quick Access to Streaming Services
```yaml
# YouTube
service: rest_command.browser_open_youtube

# Netflix
service: rest_command.browser_open_url
data:
  url: "https://www.netflix.com"

# Hulu
service: rest_command.browser_open_hulu

# Disney+
service: rest_command.browser_open_url
data:
  url: "https://www.disneyplus.com"

# Amazon Prime Video
service: rest_command.browser_open_url
data:
  url: "https://www.amazon.com/primevideo"
```

### Auto-Refresh Dashboard
```yaml
automation:
  - alias: "Refresh Dashboard Every 5 Minutes"
    trigger:
      - platform: time_pattern
        minutes: "/5"
    action:
      - service: rest_command.browser_reload
```

### Tab Navigation with Voice
```yaml
automation:
  - alias: "Voice - Next Tab"
    trigger:
      - platform: conversation
        command:
          - "next tab"
          - "switch tab"
    action:
      - service: rest_command.browser_next_tab
  
  - alias: "Voice - Previous Tab"
    trigger:
      - platform: conversation
        command:
          - "previous tab"
          - "go back"
    action:
      - service: rest_command.browser_prev_tab
```

### Browser Launcher
```yaml
automation:
  - alias: "Voice - Open Browser"
    trigger:
      - platform: conversation
        command:
          - "open chrome"
    action:
      - service: rest_command.browser_open_chrome
  
  - alias: "Voice - Open Firefox"
    trigger:
      - platform: conversation
        command:
          - "open firefox"
    action:
      - service: rest_command.browser_open_firefox
```

## Dashboard Buttons

Add these to your Lovelace dashboard for quick access:

```yaml
type: entities
title: Browser Control
entities:
  - button.browser_open_chrome_button
  - button.browser_open_firefox_button
  - button.browser_open_edge_button
  - button.browser_new_tab_button
  - button.browser_close_tab_button
  - button.browser_next_tab_button
  - button.browser_prev_tab_button
  - button.browser_reload_button
  - button.browser_hard_reload_button
  - button.browser_home_button
  - button.browser_open_youtube_button
  - button.browser_open_hulu_button
```

## Python Script Serial Commands

If connecting directly to the Python script via serial, use these commands:

```
BROWSER_OPEN_CHROME
BROWSER_OPEN_FIREFOX
BROWSER_OPEN_EDGE
BROWSER_NEW_TAB
BROWSER_CLOSE_TAB
BROWSER_NEXT_TAB
BROWSER_PREV_TAB
BROWSER_RELOAD
BROWSER_HARD_RELOAD
BROWSER_HOME
BROWSER_OPEN_URL:https://www.example.com
BROWSER_OPEN_YOUTUBE
BROWSER_OPEN_HULU
```

## Supported Browsers

The tab and page control commands work with any browser that's currently focused. The following browsers are detected automatically:
- Google Chrome (`chrome.exe`)
- Mozilla Firefox (`firefox.exe`)
- Microsoft Edge (`msedge.exe`)
- Brave Browser (`brave.exe`)

To add more browsers, edit the `browser_process_names` list in `pc_controller.py`.

## Notes

- Tab and page control commands require a browser to be running and focused
- URL opening commands will use the system's default browser
- Browser launching commands will fail if the browser is not installed
- Small delays (0.1-2 seconds) between commands are recommended for reliability
- All keyboard shortcuts are standard across major browsers
