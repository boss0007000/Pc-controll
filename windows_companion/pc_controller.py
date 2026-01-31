"""
PC Controller - Windows Companion Script

This Python script runs on the Windows PC and receives commands from the ESP32
via serial communication. It executes the commands using Windows APIs and system calls.

Requirements:
    pip install pyserial pywin32 psutil

Usage:
    python pc_controller.py [--port COM3] [--baud 115200]
"""

import serial
import time
import sys
import subprocess
import argparse
import win32api
import win32con
import win32gui
import win32process
import psutil
from ctypes import windll, Structure, c_uint, sizeof, byref

# Command handlers
class PCController:
    def __init__(self):
        self.browser_process_names = ['chrome.exe', 'firefox.exe', 'msedge.exe', 'brave.exe']
        self.tv_monitor_index = 1  # Change this to your TV monitor index (0-based)
        
    def wake_pc(self):
        """Wake the PC - typically done via WOL, but can also wake from sleep"""
        print("Executing: Wake PC")
        # Move mouse to wake from sleep
        windll.user32.SetCursorPos(100, 100)
        windll.user32.mouse_event(1, 0, 0, 0, 0)  # Mouse move
        return "PC_WAKE executed"
    
    def sleep_pc(self):
        """Put the PC to sleep"""
        print("Executing: Sleep PC")
        subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'])
        return "PC_SLEEP executed"
    
    def display_on(self):
        """Turn the display on"""
        print("Executing: Display On")
        # Send monitor on message
        windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
        # Also move mouse to ensure wake
        windll.user32.SetCursorPos(100, 100)
        windll.user32.mouse_event(1, 0, 0, 0, 0)
        return "DISPLAY_ON executed"
    
    def display_off(self):
        """Turn the display off"""
        print("Executing: Display Off")
        # Send monitor off message
        windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
        return "DISPLAY_OFF executed"
    
    def find_browser_windows(self):
        """Find all browser windows"""
        browser_windows = []
        
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    if process.name().lower() in [name.lower() for name in self.browser_process_names]:
                        title = win32gui.GetWindowText(hwnd)
                        if title:  # Only include windows with titles
                            windows.append((hwnd, title, process.name()))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return True
        
        win32gui.EnumWindows(callback, browser_windows)
        return browser_windows
    
    def browser_focus(self):
        """Focus the browser window"""
        print("Executing: Browser Focus")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Restore if minimized
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            # Bring to front
            win32gui.SetForegroundWindow(hwnd)
            return f"BROWSER_FOCUS executed on {browser_windows[0][2]}"
        else:
            return "BROWSER_FOCUS failed - no browser found"
    
    def browser_move_tv(self):
        """Move browser window to TV monitor"""
        print("Executing: Browser Move to TV")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            
            # Get monitor info
            monitors = []
            def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
                monitors.append({
                    'handle': hMonitor,
                    'left': lprcMonitor[0],
                    'top': lprcMonitor[1],
                    'right': lprcMonitor[2],
                    'bottom': lprcMonitor[3]
                })
                return True
            
            windll.user32.EnumDisplayMonitors(None, None, 
                win32api.WINFUNCTYPE(win32con.BOOL, win32con.DWORD, win32con.DWORD, 
                                     win32con.POINTER(win32con.RECT), win32con.LPARAM)(monitor_enum_proc), 0)
            
            if len(monitors) > self.tv_monitor_index:
                monitor = monitors[self.tv_monitor_index]
                width = monitor['right'] - monitor['left']
                height = monitor['bottom'] - monitor['top']
                
                # Move and resize window to TV monitor
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP,
                                     monitor['left'], monitor['top'],
                                     width, height,
                                     win32con.SWP_SHOWWINDOW)
                return f"BROWSER_MOVE_TV executed to monitor {self.tv_monitor_index}"
            else:
                return f"BROWSER_MOVE_TV failed - monitor {self.tv_monitor_index} not found"
        else:
            return "BROWSER_MOVE_TV failed - no browser found"
    
    def browser_maximize(self):
        """Maximize browser window"""
        print("Executing: Browser Maximize")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return "BROWSER_MAXIMIZE executed"
        else:
            return "BROWSER_MAXIMIZE failed - no browser found"
    
    def browser_minimize(self):
        """Minimize browser window"""
        print("Executing: Browser Minimize")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return "BROWSER_MINIMIZE executed"
        else:
            return "BROWSER_MINIMIZE failed - no browser found"
    
    def browser_close(self):
        """Close browser window"""
        print("Executing: Browser Close")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return "BROWSER_CLOSE executed"
        else:
            return "BROWSER_CLOSE failed - no browser found"
    
    def browser_restore(self):
        """Restore last browser session"""
        print("Executing: Browser Restore Session")
        
        # Try to find and launch the default browser
        # Chrome restore: chrome.exe --restore-last-session
        # Firefox: firefox.exe -restore
        
        try:
            # Try Chrome first
            subprocess.Popen(['chrome.exe', '--restore-last-session'])
            return "BROWSER_RESTORE executed - Chrome"
        except FileNotFoundError:
            try:
                # Try Firefox
                subprocess.Popen(['firefox.exe', '-restore'])
                return "BROWSER_RESTORE executed - Firefox"
            except FileNotFoundError:
                try:
                    # Try Edge
                    subprocess.Popen(['msedge.exe', '--restore-last-session'])
                    return "BROWSER_RESTORE executed - Edge"
                except FileNotFoundError:
                    return "BROWSER_RESTORE failed - no browser found"

def main():
    parser = argparse.ArgumentParser(description='PC Controller - Windows Companion Script')
    parser.add_argument('--port', default='COM3', help='Serial port (default: COM3)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    args = parser.parse_args()
    
    controller = PCController()
    
    # Command mapping
    commands = {
        'PC_WAKE': controller.wake_pc,
        'PC_SLEEP': controller.sleep_pc,
        'DISPLAY_ON': controller.display_on,
        'DISPLAY_OFF': controller.display_off,
        'BROWSER_FOCUS': controller.browser_focus,
        'BROWSER_MOVE_TV': controller.browser_move_tv,
        'BROWSER_MAXIMIZE': controller.browser_maximize,
        'BROWSER_MINIMIZE': controller.browser_minimize,
        'BROWSER_CLOSE': controller.browser_close,
        'BROWSER_RESTORE': controller.browser_restore,
    }
    
    print(f"PC Controller starting...")
    print(f"Connecting to {args.port} at {args.baud} baud...")
    
    try:
        ser = serial.Serial(args.port, args.baud, timeout=1)
        time.sleep(2)  # Wait for serial connection to stabilize
        print(f"Connected to {args.port}")
        print("Waiting for commands...")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if line:
                    print(f"\nReceived command: {line}")
                    
                    if line in commands:
                        try:
                            result = commands[line]()
                            response = f"STATUS:{result}\n"
                            ser.write(response.encode('utf-8'))
                            print(f"Response sent: {result}")
                        except Exception as e:
                            error_msg = f"ERROR:{line} - {str(e)}\n"
                            ser.write(error_msg.encode('utf-8'))
                            print(f"Error executing {line}: {e}")
                    else:
                        print(f"Unknown command: {line}")
                        ser.write(f"ERROR:Unknown command {line}\n".encode('utf-8'))
            
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        print(f"Make sure {args.port} is correct and not in use by another program")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
