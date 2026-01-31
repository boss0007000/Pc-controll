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
