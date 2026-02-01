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

## Playback Control (Universal)

These commands work universally across YouTube, Netflix, Hulu, Prime Video, Disney+, and other streaming platforms.

### Play Video
Start video playback.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/play

# Home Assistant
service: rest_command.playback_play
```

### Pause Video
Pause video playback.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/pause

# Home Assistant
service: rest_command.playback_pause
```

### Toggle Play/Pause
Toggle between play and pause states.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/play-pause

# Home Assistant
service: rest_command.playback_play_pause
```

### Stop Video
Stop video playback and exit fullscreen.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/stop

# Home Assistant
service: rest_command.playback_stop
```

### Restart Video
Restart video from the beginning.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/restart

# Home Assistant
service: rest_command.playback_restart
```

### Seek Forward (Small)
Seek forward 5 seconds.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/seek-forward-small

# Home Assistant
service: rest_command.playback_seek_forward_small
```

### Seek Backward (Small)
Seek backward 5 seconds.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/seek-backward-small

# Home Assistant
service: rest_command.playback_seek_backward_small
```

### Seek Forward (Large)
Seek forward 10 seconds.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/seek-forward-large

# Home Assistant
service: rest_command.playback_seek_forward_large
```

### Seek Backward (Large)
Seek backward 10 seconds.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/seek-backward-large

# Home Assistant
service: rest_command.playback_seek_backward_large
```

### Jump to Beginning
Jump to the start of the video.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/jump-to-beginning

# Home Assistant
service: rest_command.playback_jump_to_beginning
```

### Jump to End
Jump to the end of the video.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/jump-to-end

# Home Assistant
service: rest_command.playback_jump_to_end
```

### Next Video
Play the next video in playlist or autoplay queue.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/next-video

# Home Assistant
service: rest_command.playback_next_video
```

### Previous Video
Play the previous video in playlist.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/playback/previous-video

# Home Assistant
service: rest_command.playback_previous_video
```

## Fullscreen & View Modes

### Enter Fullscreen
Enter fullscreen mode (F11).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/fullscreen/enter

# Home Assistant
service: rest_command.fullscreen_enter
```

### Exit Fullscreen
Exit fullscreen mode (Escape).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/fullscreen/exit

# Home Assistant
service: rest_command.fullscreen_exit
```

### Toggle Fullscreen
Toggle fullscreen mode on/off (F11).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/fullscreen/toggle

# Home Assistant
service: rest_command.fullscreen_toggle
```

### Theater Mode (YouTube)
Enter YouTube theater mode (T key).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/theater-mode

# Home Assistant
service: rest_command.theater_mode
```

### Exit Theater Mode
Exit YouTube theater mode (T key again).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/theater-mode/exit

# Home Assistant
service: rest_command.theater_mode_exit
```

### Picture-in-Picture Enter
Enter picture-in-picture mode (browser-supported).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/picture-in-picture/enter

# Home Assistant
service: rest_command.picture_in_picture_enter
```

### Picture-in-Picture Exit
Exit picture-in-picture mode.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/picture-in-picture/exit

# Home Assistant
service: rest_command.picture_in_picture_exit
```

## Audio Control (OS + Browser)

### Volume Up
Increase system volume.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/volume-up

# Home Assistant
service: rest_command.audio_volume_up
```

### Volume Down
Decrease system volume.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/volume-down

# Home Assistant
service: rest_command.audio_volume_down
```

### Mute Audio
Mute system audio.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/mute

# Home Assistant
service: rest_command.audio_mute
```

### Unmute Audio
Unmute system audio.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/unmute

# Home Assistant
service: rest_command.audio_unmute
```

### Toggle Mute
Toggle mute/unmute state.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/toggle-mute

# Home Assistant
service: rest_command.audio_toggle_mute
```

### Set Volume to Predefined Levels
Set volume to specific percentage (25%, 50%, 75%, or 100%).
```bash
# REST API
curl -X POST -d "level=50" http://esp32-pc-controller.local/audio/volume-set

# Home Assistant
service: rest_command.audio_volume_set
data:
  level: 50
```

### Mute Browser Tab
Mute the video in the current browser tab (M key).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/browser-tab-mute

# Home Assistant
service: rest_command.audio_browser_tab_mute
```

### Unmute Browser Tab
Unmute the video in the current browser tab (M key again).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/browser-tab-unmute

# Home Assistant
service: rest_command.audio_browser_tab_unmute
```

### Mute All System Audio
Mute all system audio (system-wide).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/system-mute-all

# Home Assistant
service: rest_command.audio_system_mute_all
```

### Restore System Audio
Restore/unmute all system audio.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/audio/system-audio-restore

# Home Assistant
service: rest_command.audio_system_audio_restore
```

## Subtitles / Captions

### Toggle Captions On
Enable captions (C key for YouTube and many video players).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/captions/toggle-on

# Home Assistant
service: rest_command.captions_toggle_on
```

### Toggle Captions Off
Disable captions (C key again).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/captions/toggle-off

# Home Assistant
service: rest_command.captions_toggle_off
```

### Cycle Caption Languages
Open caption settings menu to cycle languages (O key on YouTube).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/captions/cycle-language

# Home Assistant
service: rest_command.captions_cycle_language
```

### Increase Caption Size
Increase caption size using browser zoom (Ctrl++).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/captions/size-increase

# Home Assistant
service: rest_command.captions_size_increase
```

### Decrease Caption Size
Decrease caption size using browser zoom (Ctrl+-).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/captions/size-decrease

# Home Assistant
service: rest_command.captions_size_decrease
```

## Common Use Cases

### Video Streaming Control
```yaml
automation:
  - alias: "Media Center Mode - YouTube"
    trigger:
      - platform: state
        entity_id: input_boolean.media_mode
        to: 'on'
    action:
      # Open YouTube and maximize
      - service: rest_command.browser_open_youtube
      - delay:
          seconds: 3
      - service: rest_command.browser_maximize
      - service: rest_command.browser_move_tv
      
  - alias: "Video Remote - Play/Pause"
    trigger:
      - platform: event
        event_type: remote_button_press
        event_data:
          button: play_pause
    action:
      - service: rest_command.playback_play_pause
      
  - alias: "Video Remote - Skip Forward"
    trigger:
      - platform: event
        event_type: remote_button_press
        event_data:
          button: forward
    action:
      - service: rest_command.playback_seek_forward_large
      
  - alias: "Video Remote - Skip Backward"
    trigger:
      - platform: event
        event_type: remote_button_press
        event_data:
          button: backward
    action:
      - service: rest_command.playback_seek_backward_large
```

### Voice Control for Streaming
```yaml
automation:
  - alias: "Voice - Play Video"
    trigger:
      - platform: conversation
        command:
          - "play video"
          - "play"
    action:
      - service: rest_command.playback_play
  
  - alias: "Voice - Pause Video"
    trigger:
      - platform: conversation
        command:
          - "pause video"
          - "pause"
    action:
      - service: rest_command.playback_pause
  
  - alias: "Voice - Next Video"
    trigger:
      - platform: conversation
        command:
          - "next video"
          - "skip video"
    action:
      - service: rest_command.playback_next_video
  
  - alias: "Voice - Restart Video"
    trigger:
      - platform: conversation
        command:
          - "restart video"
          - "start over"
    action:
      - service: rest_command.playback_restart
```

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

### Theater Mode Control
```yaml
automation:
  - alias: "Enter Theater Mode on YouTube"
    trigger:
      - platform: state
        entity_id: input_boolean.theater_mode
        to: 'on'
    action:
      - service: rest_command.browser_open_youtube
      - delay:
          seconds: 3
      - service: rest_command.theater_mode
  
  - alias: "Exit Theater Mode"
    trigger:
      - platform: state
        entity_id: input_boolean.theater_mode
        to: 'off'
    action:
      - service: rest_command.theater_mode_exit
```

### Audio Control Automations
```yaml
automation:
  - alias: "Voice - Volume Up"
    trigger:
      - platform: conversation
        command:
          - "volume up"
          - "increase volume"
    action:
      - service: rest_command.audio_volume_up
  
  - alias: "Voice - Volume Down"
    trigger:
      - platform: conversation
        command:
          - "volume down"
          - "decrease volume"
    action:
      - service: rest_command.audio_volume_down
  
  - alias: "Voice - Mute"
    trigger:
      - platform: conversation
        command:
          - "mute"
          - "mute audio"
    action:
      - service: rest_command.audio_toggle_mute
  
  - alias: "Set Volume for Movie Time"
    trigger:
      - platform: state
        entity_id: input_boolean.movie_mode
        to: 'on'
    action:
      - service: rest_command.audio_volume_set
        data:
          level: 75
```

### Caption Control
```yaml
automation:
  - alias: "Voice - Toggle Captions"
    trigger:
      - platform: conversation
        command:
          - "captions on"
          - "enable captions"
    action:
      - service: rest_command.captions_toggle_on
  
  - alias: "Auto Enable Captions for Hearing Impaired"
    trigger:
      - platform: state
        entity_id: input_boolean.accessibility_mode
        to: 'on'
    action:
      - service: rest_command.captions_toggle_on
      - service: rest_command.captions_size_increase
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
PLAYBACK_PLAY
PLAYBACK_PAUSE
PLAYBACK_PLAY_PAUSE
PLAYBACK_STOP
PLAYBACK_RESTART
PLAYBACK_SEEK_FORWARD_SMALL
PLAYBACK_SEEK_BACKWARD_SMALL
PLAYBACK_SEEK_FORWARD_LARGE
PLAYBACK_SEEK_BACKWARD_LARGE
PLAYBACK_JUMP_TO_BEGINNING
PLAYBACK_JUMP_TO_END
PLAYBACK_NEXT_VIDEO
PLAYBACK_PREVIOUS_VIDEO
FULLSCREEN_ENTER
FULLSCREEN_EXIT
FULLSCREEN_TOGGLE
THEATER_MODE
THEATER_MODE_EXIT
PICTURE_IN_PICTURE_ENTER
PICTURE_IN_PICTURE_EXIT
VOLUME_UP
VOLUME_DOWN
MUTE_AUDIO
UNMUTE_AUDIO
TOGGLE_MUTE
VOLUME_SET:50
BROWSER_TAB_MUTE
BROWSER_TAB_UNMUTE
SYSTEM_MUTE_ALL
SYSTEM_AUDIO_RESTORE
CAPTIONS_TOGGLE_ON
CAPTIONS_TOGGLE_OFF
CAPTIONS_CYCLE_LANGUAGE
CAPTIONS_SIZE_INCREASE
CAPTIONS_SIZE_DECREASE
NAV_SELECT_ELEMENT
NAV_BACK
NAV_FORWARD
NAV_EXIT_MENU
NAV_SCROLL_UP
NAV_SCROLL_DOWN
NAV_PAGE_UP
NAV_PAGE_DOWN
NAV_FOCUS_SEARCH
NAV_CLEAR_SEARCH
NAV_SUBMIT_SEARCH
NAV_TAB_FORWARD
SEARCH_YOUTUBE:query text here
SEARCH_HULU:query text here
SEARCH_CURRENT_SITE
OPEN_YOUTUBE_TRENDING
OPEN_YOUTUBE_SUBSCRIPTIONS
OPEN_HULU_WATCHLIST
OPEN_YOUTUBE_HISTORY
OPEN_NETFLIX_HOME
YOUTUBE_LIKE
YOUTUBE_DISLIKE
YOUTUBE_SUBSCRIBE
SKIP_BUTTON_ACTION
BROWSER_MOVE_MONITOR_1
BROWSER_MOVE_MONITOR_2
FOCUS_ASSIST_ENABLE
FOCUS_ASSIST_DISABLE
PREVENT_SLEEP
ALLOW_SLEEP
SMART_SHOW_SOMETHING
SMART_CONTINUE_LAST
SMART_FIND_ELSE
SMART_THATS_ENOUGH
SMART_KILL_PLAYBACK
SMART_EMERGENCY_MUTE
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
- Fullscreen and view mode commands work universally across browsers
- Audio control commands affect the entire system (volume keys) or browser tab (M key)
- Caption controls are optimized for YouTube but work on many video platforms
- Picture-in-picture support varies by browser and video platform
- Theater mode is specific to YouTube and similar platforms

### Playback Controls Compatibility

The playback control commands use universal keyboard shortcuts that work across all major streaming platforms:

**Fully Supported Platforms:**
- YouTube (all features including playlist navigation)
- Netflix (play/pause, seek, fullscreen controls)
- Hulu (play/pause, seek, fullscreen controls)
- Amazon Prime Video (play/pause, seek, fullscreen controls)
- Disney+ (play/pause, seek, fullscreen controls)
- HBO Max (play/pause, seek, fullscreen controls)
- Twitch (play/pause, seek controls)
- Vimeo (play/pause, seek controls)

**Key Mappings:**
- Play/Pause: Spacebar (universal)
- Seek ±5s: Arrow keys (universal)
- Seek ±10s: J/L keys (YouTube), Arrow keys (others)
- Jump to start/end: Home/End keys (universal)
- Next/Previous: Shift+N/P (YouTube), varies by platform
- Stop/Exit fullscreen: Escape (universal)
- Fullscreen: F11 (universal)
- Theater mode: T (YouTube)
- Captions: C (YouTube and many platforms)
- Mute video: M (YouTube and many platforms)

Some platform-specific features (like Next/Previous video) may work best on YouTube but are compatible with most platforms that support playlists or autoplay.

## Navigation Commands (Keyboard-Based)

### Select Focused Element
Press Enter to activate the currently focused element.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/select

# Home Assistant
service: rest_command.nav_select

# Serial Command
NAV_SELECT_ELEMENT
```

### Navigate Back
Go back to previous page (Alt+Left).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/back

# Home Assistant
service: rest_command.nav_back

# Serial Command
NAV_BACK
```

### Navigate Forward
Go forward to next page (Alt+Right).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/forward

# Home Assistant
service: rest_command.nav_forward

# Serial Command
NAV_FORWARD
```

### Exit Menu/Close Overlay
Close menus and overlays with Escape key.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/exit-menu

# Home Assistant
service: rest_command.nav_exit_menu

# Serial Command
NAV_EXIT_MENU
```

### Scroll Up/Down
Scroll page content with arrow keys.
```bash
# REST API - Scroll Up
curl -X POST http://esp32-pc-controller.local/nav/scroll-up
# REST API - Scroll Down
curl -X POST http://esp32-pc-controller.local/nav/scroll-down

# Home Assistant
service: rest_command.nav_scroll_up
service: rest_command.nav_scroll_down

# Serial Commands
NAV_SCROLL_UP
NAV_SCROLL_DOWN
```

### Page Up/Down
Quick page navigation with Page Up/Down keys.
```bash
# REST API - Page Up
curl -X POST http://esp32-pc-controller.local/nav/page-up
# REST API - Page Down
curl -X POST http://esp32-pc-controller.local/nav/page-down

# Home Assistant
service: rest_command.nav_page_up
service: rest_command.nav_page_down

# Serial Commands
NAV_PAGE_UP
NAV_PAGE_DOWN
```

### Focus Search Bar
Move focus to browser address/search bar (Ctrl+L).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/focus-search

# Home Assistant
service: rest_command.nav_focus_search

# Serial Command
NAV_FOCUS_SEARCH
```

### Clear Search Field
Clear current text in focused field (Ctrl+A then Delete).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/clear-search

# Home Assistant
service: rest_command.nav_clear_search

# Serial Command
NAV_CLEAR_SEARCH
```

### Submit Search
Submit search or form (Enter key).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/submit-search

# Home Assistant
service: rest_command.nav_submit_search

# Serial Command
NAV_SUBMIT_SEARCH
```

### Tab Forward
Navigate between elements with Tab key.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/nav/tab-forward

# Home Assistant
service: rest_command.nav_tab_forward

# Serial Command
NAV_TAB_FORWARD
```

## Search & Content Discovery

### Search YouTube
Search YouTube for a specific query.
```bash
# REST API
curl -X POST -d "query=funny cats" http://esp32-pc-controller.local/search/youtube

# Serial Command
SEARCH_YOUTUBE:funny cats
```

### Search Hulu
Search Hulu for a specific query.
```bash
# REST API
curl -X POST -d "query=action movies" http://esp32-pc-controller.local/search/hulu

# Serial Command
SEARCH_HULU:action movies
```

### Search Current Site
Open find-in-page dialog (Ctrl+F).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/search/current-site

# Home Assistant
service: rest_command.search_current_site

# Serial Command
SEARCH_CURRENT_SITE
```

### Open YouTube Trending
Navigate to YouTube trending page.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/content/youtube-trending

# Home Assistant
service: rest_command.content_youtube_trending

# Serial Command
OPEN_YOUTUBE_TRENDING
```

### Open YouTube Subscriptions
Navigate to YouTube subscriptions feed.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/content/youtube-subscriptions

# Home Assistant
service: rest_command.content_youtube_subscriptions

# Serial Command
OPEN_YOUTUBE_SUBSCRIPTIONS
```

### Open Hulu Watchlist
Navigate to Hulu "My Stuff" watchlist.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/content/hulu-watchlist

# Home Assistant
service: rest_command.content_hulu_watchlist

# Serial Command
OPEN_HULU_WATCHLIST
```

### Open YouTube History
Navigate to YouTube watch history.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/content/youtube-history

# Home Assistant
service: rest_command.content_youtube_history

# Serial Command
OPEN_YOUTUBE_HISTORY
```

### Open Netflix Home
Navigate to Netflix browse page.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/content/netflix-home

# Home Assistant
service: rest_command.content_netflix_home

# Serial Command
OPEN_NETFLIX_HOME
```

## User Interaction (Site-Specific)

### Like Video (YouTube)
Like the current video on YouTube (Shift+L).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/youtube/like

# Home Assistant
service: rest_command.youtube_like

# Serial Command
YOUTUBE_LIKE
```

### Dislike Video (YouTube)
Dislike the current video on YouTube (Shift+D).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/youtube/dislike

# Home Assistant
service: rest_command.youtube_dislike

# Serial Command
YOUTUBE_DISLIKE
```

### Subscribe (YouTube)
Subscribe to current channel on YouTube (Shift+S).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/youtube/subscribe

# Home Assistant
service: rest_command.youtube_subscribe

# Serial Command
YOUTUBE_SUBSCRIBE
```

### Skip Button Action
Generic skip action for Skip Ad, Skip Intro, Skip Recap buttons (Tab navigation + Enter).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/action/skip

# Home Assistant
service: rest_command.action_skip

# Serial Command
SKIP_BUTTON_ACTION
```

## Multi-Monitor Control

### Move Browser to Monitor 1
Move browser window to primary monitor.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/move-monitor-1

# Home Assistant
service: rest_command.browser_move_monitor_1

# Serial Command
BROWSER_MOVE_MONITOR_1
```

### Move Browser to Monitor 2
Move browser window to secondary monitor (TV).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/browser/move-monitor-2

# Home Assistant
service: rest_command.browser_move_monitor_2

# Serial Command
BROWSER_MOVE_MONITOR_2
```

## Focus & Distraction Control

### Enable Focus Assist
Enable Windows Focus Assist (Do Not Disturb mode).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/focus/assist-enable

# Home Assistant
service: rest_command.focus_assist_enable

# Serial Command
FOCUS_ASSIST_ENABLE
```

### Disable Focus Assist
Disable Windows Focus Assist.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/focus/assist-disable

# Home Assistant
service: rest_command.focus_assist_disable

# Serial Command
FOCUS_ASSIST_DISABLE
```

### Prevent Sleep
Prevent screen from sleeping (keeps display active).
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/sleep/prevent

# Home Assistant
service: rest_command.sleep_prevent

# Serial Command
PREVENT_SLEEP
```

### Allow Sleep
Allow screen to sleep normally.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/sleep/allow

# Home Assistant
service: rest_command.sleep_allow

# Serial Command
ALLOW_SLEEP
```

## Smart Convenience Commands

These are convenient shortcuts that combine multiple actions.

### Show Me Something
Open homepage/feed - quick way to start browsing.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/show-something

# Home Assistant
service: rest_command.smart_show_something

# Serial Command
SMART_SHOW_SOMETHING
```

### Continue Where I Left Off
Resume last browser session with all tabs.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/continue-last

# Home Assistant
service: rest_command.smart_continue_last

# Serial Command
SMART_CONTINUE_LAST
```

### Find Something Else
Reload page to refresh recommendations.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/find-else

# Home Assistant
service: rest_command.smart_find_else

# Serial Command
SMART_FIND_ELSE
```

### That's Enough
Pause video and exit fullscreen - quick stop.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/thats-enough

# Home Assistant
service: rest_command.smart_thats_enough

# Serial Command
SMART_THATS_ENOUGH
```

### Kill Playback
Stop everything - pause, exit fullscreen, and minimize browser.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/kill-playback

# Home Assistant
service: rest_command.smart_kill_playback

# Serial Command
SMART_KILL_PLAYBACK
```

### Emergency Mute
Instantly mute all system audio.
```bash
# REST API
curl -X POST http://esp32-pc-controller.local/smart/emergency-mute

# Home Assistant
service: rest_command.smart_emergency_mute

# Serial Command
SMART_EMERGENCY_MUTE
```
