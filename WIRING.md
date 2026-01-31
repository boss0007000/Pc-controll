# Wiring Diagram

## Connection Overview

```
┌─────────────────┐                    ┌──────────────────┐
│                 │                    │                  │
│   Windows PC    │◄──USB Serial──────►│     ESP32        │
│                 │    (115200 baud)   │                  │
└─────────────────┘                    └──────────────────┘
                                              │
                                              │ WiFi
                                              │
                                              ▼
                                       ┌──────────────────┐
                                       │                  │
                                       │ Home Assistant   │
                                       │                  │
                                       └──────────────────┘
```

## Physical Connections

### ESP32 to PC Connection

**Standard USB Connection (Recommended)**
```
ESP32 Board          Windows PC
┌─────────┐         ┌──────────┐
│         │         │          │
│  USB    │◄───────►│USB Port  │
│  Port   │  USB    │          │
│         │  Cable  │          │
└─────────┘         └──────────┘
```

This is the simplest method:
1. Connect ESP32 to Windows PC using a USB cable (data cable, not power-only)
2. ESP32 will be powered by the PC USB port
3. Serial communication happens automatically over USB
4. No additional wiring needed

### Optional: External Power

If you want to power ESP32 separately:

```
ESP32 Board
┌─────────────────┐
│              VIN├──── 5V Power Supply (+)
│              GND├──── Power Supply Ground (-)
│                 │
│              TX ├──── PC RX (via USB-to-Serial adapter)
│              RX ├──── PC TX (via USB-to-Serial adapter)
│              GND├──── Common Ground with PC
└─────────────────┘
```

### Optional: Wake-on-LAN GPIO

If you want to use a GPIO for hardware WOL triggering:

```
ESP32                PC Motherboard
┌─────────┐         ┌──────────────┐
│         │         │              │
│  GPIO2  ├────────►│ WOL Header   │
│         │         │  (Pin 1)     │
│  GND    ├────────►│ GND          │
│         │         │  (Pin 2)     │
└─────────┘         └──────────────┘

Note: Add a 1kΩ resistor in series for protection
```

## Pin Configuration

### ESP32 Default Pins Used

| Pin | Function | Direction | Description |
|-----|----------|-----------|-------------|
| TX (GPIO1) | Serial TX | Output | Sends commands to PC |
| RX (GPIO3) | Serial RX | Input | Receives responses from PC |
| GPIO2 | WOL Signal (Optional) | Output | Can trigger hardware wake |
| 3.3V | Power | Output | Powers ESP32 (from USB) |
| GND | Ground | - | Common ground |

### ESP32 Built-in LED

The built-in LED (usually GPIO2) can be used as a status indicator:
- Modify the sketch to blink on command execution
- Shows WiFi connection status

## Cable Requirements

### USB Cable (Recommended)
- **Type**: USB-A to Micro-USB or USB-C (depending on your ESP32 board)
- **Requirement**: Must be a data cable (not power-only)
- **Length**: Up to 5 meters (16 feet) for reliable communication
- **Note**: Use shielded cable for better EMI protection

### Alternative: USB-to-Serial Adapter
If not using direct USB connection:
- FTDI FT232RL or similar
- CP2102 or CH340G based adapter
- Connect TX to RX and RX to TX (crossover)

## Power Requirements

### ESP32 Power Consumption
- **Typical**: 80-260 mA (depending on WiFi activity)
- **Peak**: Up to 500 mA during WiFi transmission
- **USB Port Supply**: Standard USB 2.0 port provides 500 mA (sufficient)

### USB Port Considerations
1. Use a USB port that remains powered when PC is in sleep mode if you want ESP32 to wake the PC
2. Check BIOS settings for "USB Power in S3/S4/S5" states
3. Rear panel USB ports typically better than front panel

## Multiple Monitor Setup

For the "Move to TV" feature with multiple monitors:

```
┌────────────┐         ┌────────────┐
│  Monitor 0 │         │  Monitor 1 │
│  (Primary) │         │    (TV)    │
└─────┬──────┘         └──────┬─────┘
      │                       │
      └───────┬───────────────┘
              │
        ┌─────┴──────┐
        │  Graphics  │
        │    Card    │
        └────────────┘
```

Configure `tv_monitor_index` in `pc_controller.py`:
- `0` = First monitor (usually primary)
- `1` = Second monitor (typically TV)
- `2` = Third monitor, etc.

## Network Topology

```
┌─────────────┐
│   Router    │
│   (WiFi)    │
└──────┬──────┘
       │
       ├──────────┬──────────────┬
       │          │              │
   ┌───▼────┐  ┌──▼───────┐  ┌──▼──────┐
   │ ESP32  │  │ Home     │  │ Other   │
   │        │  │ Assist.  │  │ Devices │
   └───┬────┘  └──────────┘  └─────────┘
       │
    ┌──▼────┐
    │  PC   │
    │(USB)  │
    └───────┘
```

**Network Requirements:**
- ESP32 and Home Assistant must be on the same network
- 2.4 GHz WiFi (ESP32 doesn't support 5 GHz)
- Static IP or mDNS support recommended

## Troubleshooting Connections

### Check USB Connection
```bash
# Windows: Check Device Manager
# Look for "Silicon Labs CP210x" or "USB Serial Device"

# Or in Command Prompt:
mode
```

### Check Serial Communication
1. Open Arduino IDE Serial Monitor
2. Set to 115200 baud
3. You should see ESP32 boot messages
4. Type commands manually to test

### LED Indicators (if implemented)
- Solid: WiFi connected
- Blinking: Sending/receiving commands
- Off: Not powered or error

## Safety Notes

1. **ESD Protection**: Use anti-static precautions when handling ESP32
2. **Voltage**: ESP32 is 3.3V logic - do not connect 5V signals to GPIO pins
3. **Current**: Do not draw more than 12 mA from any single GPIO pin
4. **USB Hot-plug**: Safe to connect/disconnect USB while PC is on
5. **Grounding**: Ensure proper grounding, especially with external power

## Quick Setup Checklist

- [ ] ESP32 board (any variant)
- [ ] USB cable (data capable)
- [ ] Windows PC with available USB port
- [ ] WiFi network (2.4 GHz)
- [ ] Home Assistant instance on same network
- [ ] Arduino IDE with ESP32 support
- [ ] Python 3.7+ installed on Windows PC
- [ ] Required libraries installed (both Arduino and Python)
