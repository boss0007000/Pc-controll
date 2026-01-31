/*
 * ESP32 PC Controller with Home Assistant Integration
 * 
 * This sketch allows an ESP32 to control a Windows PC through serial communication.
 * It connects to Home Assistant via WiFi and exposes control entities.
 * 
 * Configuration:
 * 1. Copy config_example.h to config.h
 * 2. Update WiFi credentials in the section below (or use config.h)
 * 
 * Commands:
 * - PC_WAKE: Wake the PC
 * - PC_SLEEP: Put PC to sleep
 * - DISPLAY_ON: Turn display on
 * - DISPLAY_OFF: Blank display
 * - BROWSER_FOCUS: Focus browser window
 * - BROWSER_MOVE_TV: Move browser to TV monitor
 * - BROWSER_MAXIMIZE: Maximize browser
 * - BROWSER_MINIMIZE: Minimize browser
 * - BROWSER_CLOSE: Close browser
 * - BROWSER_RESTORE: Restore browser session
 * - BROWSER_OPEN_CHROME: Open Chrome browser
 * - BROWSER_OPEN_FIREFOX: Open Firefox browser
 * - BROWSER_OPEN_EDGE: Open Edge browser
 * - BROWSER_NEW_TAB: Open a new tab
 * - BROWSER_CLOSE_TAB: Close current tab
 * - BROWSER_NEXT_TAB: Switch to next tab
 * - BROWSER_PREV_TAB: Switch to previous tab
 * - BROWSER_RELOAD: Reload current page
 * - BROWSER_HARD_RELOAD: Hard reload (bypass cache)
 * - BROWSER_HOME: Go to browser home page
 * - BROWSER_OPEN_URL: Open a specific URL
 * - BROWSER_OPEN_YOUTUBE: Open YouTube
 * - BROWSER_OPEN_HULU: Open Hulu
 * - PLAYBACK_PLAY: Play video
 * - PLAYBACK_PAUSE: Pause video
 * - PLAYBACK_PLAY_PAUSE: Toggle play/pause
 * - PLAYBACK_STOP: Stop video (pause + exit fullscreen)
 * - PLAYBACK_RESTART: Restart video from beginning
 * - PLAYBACK_SEEK_FORWARD_SMALL: Seek forward 5 seconds
 * - PLAYBACK_SEEK_BACKWARD_SMALL: Seek backward 5 seconds
 * - PLAYBACK_SEEK_FORWARD_LARGE: Seek forward 10 seconds
 * - PLAYBACK_SEEK_BACKWARD_LARGE: Seek backward 10 seconds
 * - PLAYBACK_JUMP_TO_BEGINNING: Jump to video start
 * - PLAYBACK_JUMP_TO_END: Jump to video end
 * - PLAYBACK_NEXT_VIDEO: Next video in playlist
 * - PLAYBACK_PREVIOUS_VIDEO: Previous video in playlist
 * - FULLSCREEN_ENTER: Enter fullscreen mode
 * - FULLSCREEN_EXIT: Exit fullscreen mode
 * - FULLSCREEN_TOGGLE: Toggle fullscreen mode
 * - THEATER_MODE: Enter theater mode (YouTube)
 * - THEATER_MODE_EXIT: Exit theater mode
 * - PICTURE_IN_PICTURE_ENTER: Enter picture-in-picture mode
 * - PICTURE_IN_PICTURE_EXIT: Exit picture-in-picture mode
 * - VOLUME_UP: Increase system volume
 * - VOLUME_DOWN: Decrease system volume
 * - MUTE_AUDIO: Mute system audio
 * - UNMUTE_AUDIO: Unmute system audio
 * - TOGGLE_MUTE: Toggle mute/unmute
 * - VOLUME_SET: Set volume to specific level (25, 50, 75, 100)
 * - BROWSER_TAB_MUTE: Mute browser tab
 * - BROWSER_TAB_UNMUTE: Unmute browser tab
 * - SYSTEM_MUTE_ALL: Mute all system audio
 * - SYSTEM_AUDIO_RESTORE: Restore system audio
 * - CAPTIONS_TOGGLE_ON: Toggle captions on
 * - CAPTIONS_TOGGLE_OFF: Toggle captions off
 * - CAPTIONS_CYCLE_LANGUAGE: Cycle caption languages
 * - CAPTIONS_SIZE_INCREASE: Increase caption size
 * - CAPTIONS_SIZE_DECREASE: Decrease caption size
 */

#include <WiFi.h>
#include <ESPmDNS.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>

// WiFi Configuration
// IMPORTANT: Update these with your WiFi credentials
// For better security, consider using config.h (see config_example.h)
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Device Configuration
const char* DEVICE_NAME = "esp32-pc-controller";
const int SERIAL_BAUD = 115200;

// Wake-on-LAN Configuration
const int WOL_PIN = 2;  // GPIO pin for WOL signal (optional)

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Status tracking
bool pcAwake = false;
bool displayOn = false;
String lastCommand = "None";
unsigned long lastCommandTime = 0;

void setup() {
  Serial.begin(SERIAL_BAUD);
  
  // Initialize WOL pin (if used)
  pinMode(WOL_PIN, OUTPUT);
  digitalWrite(WOL_PIN, LOW);
  
  // Connect to WiFi
  Serial.println("\n\nESP32 PC Controller Starting...");
  connectToWiFi();
  
  // Start mDNS
  if (MDNS.begin(DEVICE_NAME)) {
    Serial.println("mDNS responder started");
    Serial.print("Access at: http://");
    Serial.print(DEVICE_NAME);
    Serial.println(".local");
  }
  
  // Setup web server routes
  setupWebServer();
  
  // Start server
  server.begin();
  Serial.println("HTTP server started");
  Serial.println("Ready to receive commands from Home Assistant");
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connection lost. Reconnecting...");
    connectToWiFi();
  }
  
  // Check for responses from PC
  if (Serial.available()) {
    String response = Serial.readStringUntil('\n');
    response.trim();
    handlePCResponse(response);
  }
  
  delay(10);
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }
}

void setupWebServer() {
  // Root endpoint - Device info
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    String json = getStatusJSON();
    request->send(200, "application/json", json);
  });
  
  // Status endpoint
  server.on("/status", HTTP_GET, [](AsyncWebServerRequest *request) {
    String json = getStatusJSON();
    request->send(200, "application/json", json);
  });
  
  // PC Control endpoints
  server.on("/pc/wake", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PC_WAKE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PC_WAKE\"}");
  });
  
  server.on("/pc/sleep", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PC_SLEEP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PC_SLEEP\"}");
  });
  
  // Display Control endpoints
  server.on("/display/on", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("DISPLAY_ON");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"DISPLAY_ON\"}");
  });
  
  server.on("/display/off", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("DISPLAY_OFF");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"DISPLAY_OFF\"}");
  });
  
  // Browser Control endpoints
  server.on("/browser/focus", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_FOCUS");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_FOCUS\"}");
  });
  
  server.on("/browser/move-tv", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_MOVE_TV");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_MOVE_TV\"}");
  });
  
  server.on("/browser/maximize", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_MAXIMIZE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_MAXIMIZE\"}");
  });
  
  server.on("/browser/minimize", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_MINIMIZE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_MINIMIZE\"}");
  });
  
  server.on("/browser/close", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_CLOSE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_CLOSE\"}");
  });
  
  server.on("/browser/restore", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_RESTORE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_RESTORE\"}");
  });
  
  // Browser Opening endpoints
  server.on("/browser/open-chrome", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_OPEN_CHROME");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_CHROME\"}");
  });
  
  server.on("/browser/open-firefox", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_OPEN_FIREFOX");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_FIREFOX\"}");
  });
  
  server.on("/browser/open-edge", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_OPEN_EDGE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_EDGE\"}");
  });
  
  // Tab Control endpoints
  server.on("/browser/new-tab", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_NEW_TAB");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_NEW_TAB\"}");
  });
  
  server.on("/browser/close-tab", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_CLOSE_TAB");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_CLOSE_TAB\"}");
  });
  
  server.on("/browser/next-tab", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_NEXT_TAB");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_NEXT_TAB\"}");
  });
  
  server.on("/browser/prev-tab", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_PREV_TAB");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_PREV_TAB\"}");
  });
  
  // Page Control endpoints
  server.on("/browser/reload", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_RELOAD");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_RELOAD\"}");
  });
  
  server.on("/browser/hard-reload", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_HARD_RELOAD");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_HARD_RELOAD\"}");
  });
  
  server.on("/browser/home", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_HOME");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_HOME\"}");
  });
  
  // URL Opening endpoints
  server.on("/browser/open-url", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("url", true)) {
      String url = request->getParam("url", true)->value();
      String cmd = "BROWSER_OPEN_URL:" + url;
      executeCommand(cmd);
      request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_URL\",\"url\":\"" + url + "\"}");
    } else {
      request->send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing url parameter\"}");
    }
  });
  
  server.on("/browser/open-youtube", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_OPEN_YOUTUBE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_YOUTUBE\"}");
  });
  
  server.on("/browser/open-hulu", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_OPEN_HULU");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_OPEN_HULU\"}");
  });
  
  // Playback Control endpoints (Universal - works on YouTube, Netflix, Hulu, Prime Video, etc.)
  server.on("/playback/play", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_PLAY");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_PLAY\"}");
  });
  
  server.on("/playback/pause", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_PAUSE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_PAUSE\"}");
  });
  
  server.on("/playback/play-pause", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_PLAY_PAUSE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_PLAY_PAUSE\"}");
  });
  
  server.on("/playback/stop", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_STOP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_STOP\"}");
  });
  
  server.on("/playback/restart", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_RESTART");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_RESTART\"}");
  });
  
  server.on("/playback/seek-forward-small", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_SEEK_FORWARD_SMALL");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_SEEK_FORWARD_SMALL\"}");
  });
  
  server.on("/playback/seek-backward-small", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_SEEK_BACKWARD_SMALL");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_SEEK_BACKWARD_SMALL\"}");
  });
  
  server.on("/playback/seek-forward-large", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_SEEK_FORWARD_LARGE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_SEEK_FORWARD_LARGE\"}");
  });
  
  server.on("/playback/seek-backward-large", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_SEEK_BACKWARD_LARGE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_SEEK_BACKWARD_LARGE\"}");
  });
  
  server.on("/playback/jump-to-beginning", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_JUMP_TO_BEGINNING");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_JUMP_TO_BEGINNING\"}");
  });
  
  server.on("/playback/jump-to-end", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_JUMP_TO_END");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_JUMP_TO_END\"}");
  });
  
  server.on("/playback/next-video", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_NEXT_VIDEO");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_NEXT_VIDEO\"}");
  });
  
  server.on("/playback/previous-video", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PLAYBACK_PREVIOUS_VIDEO");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PLAYBACK_PREVIOUS_VIDEO\"}");
  });
  
  // Fullscreen & View Mode endpoints
  server.on("/fullscreen/enter", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("FULLSCREEN_ENTER");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"FULLSCREEN_ENTER\"}");
  });
  
  server.on("/fullscreen/exit", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("FULLSCREEN_EXIT");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"FULLSCREEN_EXIT\"}");
  });
  
  server.on("/fullscreen/toggle", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("FULLSCREEN_TOGGLE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"FULLSCREEN_TOGGLE\"}");
  });
  
  server.on("/theater-mode", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("THEATER_MODE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"THEATER_MODE\"}");
  });
  
  server.on("/theater-mode/exit", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("THEATER_MODE_EXIT");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"THEATER_MODE_EXIT\"}");
  });
  
  server.on("/picture-in-picture/enter", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PICTURE_IN_PICTURE_ENTER");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PICTURE_IN_PICTURE_ENTER\"}");
  });
  
  server.on("/picture-in-picture/exit", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PICTURE_IN_PICTURE_EXIT");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PICTURE_IN_PICTURE_EXIT\"}");
  });
  
  // Audio Control endpoints
  server.on("/audio/volume-up", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("VOLUME_UP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"VOLUME_UP\"}");
  });
  
  server.on("/audio/volume-down", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("VOLUME_DOWN");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"VOLUME_DOWN\"}");
  });
  
  server.on("/audio/mute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("MUTE_AUDIO");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"MUTE_AUDIO\"}");
  });
  
  server.on("/audio/unmute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("UNMUTE_AUDIO");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"UNMUTE_AUDIO\"}");
  });
  
  server.on("/audio/toggle-mute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("TOGGLE_MUTE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"TOGGLE_MUTE\"}");
  });
  
  server.on("/audio/volume-set", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("level", true)) {
      String level = request->getParam("level", true)->value();
      String cmd = "VOLUME_SET:" + level;
      executeCommand(cmd);
      request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"VOLUME_SET\",\"level\":\"" + level + "\"}");
    } else {
      request->send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing level parameter\"}");
    }
  });
  
  server.on("/audio/browser-tab-mute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_TAB_MUTE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_TAB_MUTE\"}");
  });
  
  server.on("/audio/browser-tab-unmute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_TAB_UNMUTE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_TAB_UNMUTE\"}");
  });
  
  server.on("/audio/system-mute-all", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SYSTEM_MUTE_ALL");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SYSTEM_MUTE_ALL\"}");
  });
  
  server.on("/audio/system-audio-restore", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SYSTEM_AUDIO_RESTORE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SYSTEM_AUDIO_RESTORE\"}");
  });
  
  // Subtitles/Captions endpoints
  server.on("/captions/toggle-on", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("CAPTIONS_TOGGLE_ON");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"CAPTIONS_TOGGLE_ON\"}");
  });
  
  server.on("/captions/toggle-off", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("CAPTIONS_TOGGLE_OFF");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"CAPTIONS_TOGGLE_OFF\"}");
  });
  
  server.on("/captions/cycle-language", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("CAPTIONS_CYCLE_LANGUAGE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"CAPTIONS_CYCLE_LANGUAGE\"}");
  });
  
  server.on("/captions/size-increase", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("CAPTIONS_SIZE_INCREASE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"CAPTIONS_SIZE_INCREASE\"}");
  });
  
  server.on("/captions/size-decrease", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("CAPTIONS_SIZE_DECREASE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"CAPTIONS_SIZE_DECREASE\"}");
  });
  
  // Navigation Control endpoints (without mouse)
  server.on("/nav/select", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_SELECT_ELEMENT");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_SELECT_ELEMENT\"}");
  });
  
  server.on("/nav/back", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_BACK");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_BACK\"}");
  });
  
  server.on("/nav/forward", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_FORWARD");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_FORWARD\"}");
  });
  
  server.on("/nav/exit-menu", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_EXIT_MENU");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_EXIT_MENU\"}");
  });
  
  server.on("/nav/scroll-up", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_SCROLL_UP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_SCROLL_UP\"}");
  });
  
  server.on("/nav/scroll-down", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_SCROLL_DOWN");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_SCROLL_DOWN\"}");
  });
  
  server.on("/nav/page-up", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_PAGE_UP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_PAGE_UP\"}");
  });
  
  server.on("/nav/page-down", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_PAGE_DOWN");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_PAGE_DOWN\"}");
  });
  
  server.on("/nav/focus-search", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_FOCUS_SEARCH");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_FOCUS_SEARCH\"}");
  });
  
  server.on("/nav/clear-search", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_CLEAR_SEARCH");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_CLEAR_SEARCH\"}");
  });
  
  server.on("/nav/submit-search", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_SUBMIT_SEARCH");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_SUBMIT_SEARCH\"}");
  });
  
  server.on("/nav/tab-forward", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("NAV_TAB_FORWARD");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"NAV_TAB_FORWARD\"}");
  });
  
  // Search & Content Discovery endpoints
  server.on("/search/youtube", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("query", true)) {
      String query = request->getParam("query", true)->value();
      executeCommand("SEARCH_YOUTUBE:" + query);
      request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SEARCH_YOUTUBE\"}");
    } else {
      request->send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing query parameter\"}");
    }
  });
  
  server.on("/search/hulu", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("query", true)) {
      String query = request->getParam("query", true)->value();
      executeCommand("SEARCH_HULU:" + query);
      request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SEARCH_HULU\"}");
    } else {
      request->send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing query parameter\"}");
    }
  });
  
  server.on("/search/current-site", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SEARCH_CURRENT_SITE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SEARCH_CURRENT_SITE\"}");
  });
  
  server.on("/content/youtube-trending", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("OPEN_YOUTUBE_TRENDING");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"OPEN_YOUTUBE_TRENDING\"}");
  });
  
  server.on("/content/youtube-subscriptions", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("OPEN_YOUTUBE_SUBSCRIPTIONS");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"OPEN_YOUTUBE_SUBSCRIPTIONS\"}");
  });
  
  server.on("/content/hulu-watchlist", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("OPEN_HULU_WATCHLIST");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"OPEN_HULU_WATCHLIST\"}");
  });
  
  server.on("/content/youtube-history", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("OPEN_YOUTUBE_HISTORY");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"OPEN_YOUTUBE_HISTORY\"}");
  });
  
  server.on("/content/netflix-home", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("OPEN_NETFLIX_HOME");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"OPEN_NETFLIX_HOME\"}");
  });
  
  // User Interaction endpoints (site-specific)
  server.on("/youtube/like", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("YOUTUBE_LIKE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"YOUTUBE_LIKE\"}");
  });
  
  server.on("/youtube/dislike", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("YOUTUBE_DISLIKE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"YOUTUBE_DISLIKE\"}");
  });
  
  server.on("/youtube/subscribe", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("YOUTUBE_SUBSCRIBE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"YOUTUBE_SUBSCRIBE\"}");
  });
  
  server.on("/action/skip", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SKIP_BUTTON_ACTION");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SKIP_BUTTON_ACTION\"}");
  });
  
  // Multi-Monitor Control endpoints
  server.on("/browser/move-monitor-1", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_MOVE_MONITOR_1");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_MOVE_MONITOR_1\"}");
  });
  
  server.on("/browser/move-monitor-2", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("BROWSER_MOVE_MONITOR_2");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"BROWSER_MOVE_MONITOR_2\"}");
  });
  
  // Focus & Distraction Control endpoints
  server.on("/focus/assist-enable", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("FOCUS_ASSIST_ENABLE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"FOCUS_ASSIST_ENABLE\"}");
  });
  
  server.on("/focus/assist-disable", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("FOCUS_ASSIST_DISABLE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"FOCUS_ASSIST_DISABLE\"}");
  });
  
  server.on("/sleep/prevent", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("PREVENT_SLEEP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"PREVENT_SLEEP\"}");
  });
  
  server.on("/sleep/allow", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("ALLOW_SLEEP");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"ALLOW_SLEEP\"}");
  });
  
  // Smart Convenience endpoints
  server.on("/smart/show-something", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_SHOW_SOMETHING");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_SHOW_SOMETHING\"}");
  });
  
  server.on("/smart/continue-last", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_CONTINUE_LAST");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_CONTINUE_LAST\"}");
  });
  
  server.on("/smart/find-else", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_FIND_ELSE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_FIND_ELSE\"}");
  });
  
  server.on("/smart/thats-enough", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_THATS_ENOUGH");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_THATS_ENOUGH\"}");
  });
  
  server.on("/smart/kill-playback", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_KILL_PLAYBACK");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_KILL_PLAYBACK\"}");
  });
  
  server.on("/smart/emergency-mute", HTTP_POST, [](AsyncWebServerRequest *request) {
    executeCommand("SMART_EMERGENCY_MUTE");
    request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"SMART_EMERGENCY_MUTE\"}");
  });
  
  // Generic command endpoint
  server.on("/command", HTTP_POST, [](AsyncWebServerRequest *request) {
    if (request->hasParam("cmd", true)) {
      String cmd = request->getParam("cmd", true)->value();
      executeCommand(cmd);
      request->send(200, "application/json", "{\"status\":\"ok\",\"command\":\"" + cmd + "\"}");
    } else {
      request->send(400, "application/json", "{\"status\":\"error\",\"message\":\"Missing cmd parameter\"}");
    }
  });
}

void executeCommand(String command) {
  Serial.println(command);  // Send command to PC via serial
  lastCommand = command;
  lastCommandTime = millis();
  
  Serial.print("Executed command: ");
  Serial.println(command);
}

void handlePCResponse(String response) {
  Serial.print("PC Response: ");
  Serial.println(response);
  
  // Parse status updates from PC
  if (response.startsWith("STATUS:")) {
    // Handle status updates
    if (response.indexOf("PC_AWAKE") >= 0) {
      pcAwake = true;
    } else if (response.indexOf("PC_ASLEEP") >= 0) {
      pcAwake = false;
    }
    
    if (response.indexOf("DISPLAY_ON") >= 0) {
      displayOn = true;
    } else if (response.indexOf("DISPLAY_OFF") >= 0) {
      displayOn = false;
    }
  }
}

String getStatusJSON() {
  StaticJsonDocument<512> doc;
  
  doc["device"] = DEVICE_NAME;
  doc["ip"] = WiFi.localIP().toString();
  doc["mac"] = WiFi.macAddress();
  doc["uptime"] = millis() / 1000;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["pc_awake"] = pcAwake;
  doc["display_on"] = displayOn;
  doc["last_command"] = lastCommand;
  doc["last_command_time"] = lastCommandTime / 1000;
  
  String output;
  serializeJson(doc, output);
  return output;
}
