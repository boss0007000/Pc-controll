/*
 * Configuration Template for ESP32 PC Controller
 * 
 * Copy this file and rename to config.h
 * Fill in your settings below
 */

#ifndef CONFIG_H
#define CONFIG_H

// ========================================
// WiFi Configuration
// ========================================
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ========================================
// Device Configuration
// ========================================
#define DEVICE_NAME "esp32-pc-controller"
#define SERIAL_BAUD 115200

// ========================================
// Optional: Static IP Configuration
// ========================================
// Uncomment and configure if you want to use static IP
// #define USE_STATIC_IP
// #define STATIC_IP 192, 168, 1, 100
// #define GATEWAY 192, 168, 1, 1
// #define SUBNET 255, 255, 255, 0
// #define DNS1 8, 8, 8, 8
// #define DNS2 8, 8, 4, 4

// ========================================
// Optional: Wake-on-LAN GPIO
// ========================================
#define WOL_PIN 2  // GPIO pin for WOL signal (optional)

// ========================================
// Optional: Status LED
// ========================================
#define STATUS_LED_PIN 2  // Built-in LED for status indication
#define LED_ACTIVE_LOW true  // Set to true if LED is active-low

// ========================================
// Advanced Settings
// ========================================
#define WIFI_TIMEOUT_SECONDS 30
#define RECONNECT_DELAY_MS 5000
#define COMMAND_TIMEOUT_MS 5000

#endif // CONFIG_H
