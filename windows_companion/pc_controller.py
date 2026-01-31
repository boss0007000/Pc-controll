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
import webbrowser
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
    
    def browser_open_chrome(self):
        """Open Chrome browser"""
        print("Executing: Open Chrome")
        try:
            subprocess.Popen(['chrome.exe'])
            return "BROWSER_OPEN_CHROME executed"
        except FileNotFoundError:
            return "BROWSER_OPEN_CHROME failed - Chrome not found"
    
    def browser_open_firefox(self):
        """Open Firefox browser"""
        print("Executing: Open Firefox")
        try:
            subprocess.Popen(['firefox.exe'])
            return "BROWSER_OPEN_FIREFOX executed"
        except FileNotFoundError:
            return "BROWSER_OPEN_FIREFOX failed - Firefox not found"
    
    def browser_open_edge(self):
        """Open Edge browser"""
        print("Executing: Open Edge")
        try:
            subprocess.Popen(['msedge.exe'])
            return "BROWSER_OPEN_EDGE executed"
        except FileNotFoundError:
            return "BROWSER_OPEN_EDGE failed - Edge not found"
    
    def browser_new_tab(self):
        """Open a new tab in the active browser"""
        print("Executing: Browser New Tab")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Ctrl+T to open new tab
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(ord('T'), 0, 0, 0)
            windll.user32.keybd_event(ord('T'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_NEW_TAB executed"
        else:
            return "BROWSER_NEW_TAB failed - no browser found"
    
    def browser_close_tab(self):
        """Close current tab in the active browser"""
        print("Executing: Browser Close Tab")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Ctrl+W to close current tab
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(ord('W'), 0, 0, 0)
            windll.user32.keybd_event(ord('W'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_CLOSE_TAB executed"
        else:
            return "BROWSER_CLOSE_TAB failed - no browser found"
    
    def browser_next_tab(self):
        """Switch to next tab in the active browser"""
        print("Executing: Browser Next Tab")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Ctrl+Tab to switch to next tab
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_TAB, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_NEXT_TAB executed"
        else:
            return "BROWSER_NEXT_TAB failed - no browser found"
    
    def browser_prev_tab(self):
        """Switch to previous tab in the active browser"""
        print("Executing: Browser Previous Tab")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Ctrl+Shift+Tab to switch to previous tab
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_TAB, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_PREV_TAB executed"
        else:
            return "BROWSER_PREV_TAB failed - no browser found"
    
    def browser_reload(self):
        """Reload the current page"""
        print("Executing: Browser Reload")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send F5 to reload page
            windll.user32.keybd_event(win32con.VK_F5, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_F5, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_RELOAD executed"
        else:
            return "BROWSER_RELOAD failed - no browser found"
    
    def browser_hard_reload(self):
        """Hard reload the current page (bypass cache)"""
        print("Executing: Browser Hard Reload")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Ctrl+F5 or Ctrl+Shift+R for hard reload
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_F5, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_F5, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_HARD_RELOAD executed"
        else:
            return "BROWSER_HARD_RELOAD failed - no browser found"
    
    def browser_home(self):
        """Navigate to browser home page"""
        print("Executing: Browser Home")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            # Focus the browser first
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send Alt+Home to go to home page
            windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt key
            windll.user32.keybd_event(win32con.VK_HOME, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_HOME, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_HOME executed"
        else:
            return "BROWSER_HOME failed - no browser found"
    
    def browser_open_url(self, url):
        """Open a specific URL in the default browser"""
        print(f"Executing: Open URL: {url}")
        try:
            webbrowser.open(url)
            return f"BROWSER_OPEN_URL executed: {url}"
        except Exception as e:
            return f"BROWSER_OPEN_URL failed: {str(e)}"
    
    def browser_open_youtube(self):
        """Open YouTube in the default browser"""
        print("Executing: Open YouTube")
        return self.browser_open_url("https://www.youtube.com")
    
    def browser_open_hulu(self):
        """Open Hulu in the default browser"""
        print("Executing: Open Hulu")
        return self.browser_open_url("https://www.hulu.com")
    
    # Playback Control Methods (Universal - works on YouTube, Netflix, Hulu, Prime Video, etc.)
    
    def playback_play_pause(self):
        """Toggle play/pause in video player"""
        print("Executing: Playback Play/Pause Toggle")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Send spacebar to toggle play/pause (universal across all video platforms)
            windll.user32.keybd_event(win32con.VK_SPACE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_PLAY_PAUSE executed"
        else:
            return "PLAYBACK_PLAY_PAUSE failed - no browser found"
    
    def playback_play(self):
        """Play video (same as play/pause toggle)"""
        print("Executing: Playback Play")
        return self.playback_play_pause()
    
    def playback_pause(self):
        """Pause video (same as play/pause toggle)"""
        print("Executing: Playback Pause")
        return self.playback_play_pause()
    
    def playback_stop(self):
        """Stop video (pause and exit fullscreen)"""
        print("Executing: Playback Stop")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # First pause with spacebar
            windll.user32.keybd_event(win32con.VK_SPACE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.2)
            # Then exit fullscreen with Escape
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_STOP executed"
        else:
            return "PLAYBACK_STOP failed - no browser found"
    
    def playback_restart(self):
        """Restart video from beginning"""
        print("Executing: Playback Restart")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Press Home key to jump to beginning
            windll.user32.keybd_event(win32con.VK_HOME, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_HOME, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_RESTART executed"
        else:
            return "PLAYBACK_RESTART failed - no browser found"
    
    def playback_seek_forward_small(self):
        """Seek forward 5 seconds (Right arrow key)"""
        print("Executing: Playback Seek Forward Small")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Right arrow for small forward seek
            windll.user32.keybd_event(win32con.VK_RIGHT, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_RIGHT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_SEEK_FORWARD_SMALL executed"
        else:
            return "PLAYBACK_SEEK_FORWARD_SMALL failed - no browser found"
    
    def playback_seek_backward_small(self):
        """Seek backward 5 seconds (Left arrow key)"""
        print("Executing: Playback Seek Backward Small")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Left arrow for small backward seek
            windll.user32.keybd_event(win32con.VK_LEFT, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_LEFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_SEEK_BACKWARD_SMALL executed"
        else:
            return "PLAYBACK_SEEK_BACKWARD_SMALL failed - no browser found"
    
    def playback_seek_forward_large(self):
        """Seek forward 10 seconds (L key on YouTube, Shift+Right on others)"""
        print("Executing: Playback Seek Forward Large")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Try L key (YouTube standard)
            windll.user32.keybd_event(ord('L'), 0, 0, 0)
            windll.user32.keybd_event(ord('L'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_SEEK_FORWARD_LARGE executed"
        else:
            return "PLAYBACK_SEEK_FORWARD_LARGE failed - no browser found"
    
    def playback_seek_backward_large(self):
        """Seek backward 10 seconds (J key on YouTube, Shift+Left on others)"""
        print("Executing: Playback Seek Backward Large")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Try J key (YouTube standard)
            windll.user32.keybd_event(ord('J'), 0, 0, 0)
            windll.user32.keybd_event(ord('J'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_SEEK_BACKWARD_LARGE executed"
        else:
            return "PLAYBACK_SEEK_BACKWARD_LARGE failed - no browser found"
    
    def playback_jump_to_beginning(self):
        """Jump to the beginning of video"""
        print("Executing: Playback Jump to Beginning")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Home key to jump to beginning
            windll.user32.keybd_event(win32con.VK_HOME, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_HOME, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_JUMP_TO_BEGINNING executed"
        else:
            return "PLAYBACK_JUMP_TO_BEGINNING failed - no browser found"
    
    def playback_jump_to_end(self):
        """Jump to the end of video"""
        print("Executing: Playback Jump to End")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # End key to jump to end
            windll.user32.keybd_event(win32con.VK_END, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_END, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_JUMP_TO_END executed"
        else:
            return "PLAYBACK_JUMP_TO_END failed - no browser found"
    
    def playback_next_video(self):
        """Next video in playlist (Shift+N)"""
        print("Executing: Playback Next Video")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Shift+N for next video (YouTube standard)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(ord('N'), 0, 0, 0)
            windll.user32.keybd_event(ord('N'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_NEXT_VIDEO executed"
        else:
            return "PLAYBACK_NEXT_VIDEO failed - no browser found"
    
    def playback_previous_video(self):
        """Previous video in playlist (Shift+P)"""
        print("Executing: Playback Previous Video")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Shift+P for previous video (YouTube standard)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(ord('P'), 0, 0, 0)
            windll.user32.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PLAYBACK_PREVIOUS_VIDEO executed"
        else:
            return "PLAYBACK_PREVIOUS_VIDEO failed - no browser found"

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
        'BROWSER_OPEN_CHROME': controller.browser_open_chrome,
        'BROWSER_OPEN_FIREFOX': controller.browser_open_firefox,
        'BROWSER_OPEN_EDGE': controller.browser_open_edge,
        'BROWSER_NEW_TAB': controller.browser_new_tab,
        'BROWSER_CLOSE_TAB': controller.browser_close_tab,
        'BROWSER_NEXT_TAB': controller.browser_next_tab,
        'BROWSER_PREV_TAB': controller.browser_prev_tab,
        'BROWSER_RELOAD': controller.browser_reload,
        'BROWSER_HARD_RELOAD': controller.browser_hard_reload,
        'BROWSER_HOME': controller.browser_home,
        'BROWSER_OPEN_YOUTUBE': controller.browser_open_youtube,
        'BROWSER_OPEN_HULU': controller.browser_open_hulu,
        # Playback Control Commands
        'PLAYBACK_PLAY': controller.playback_play,
        'PLAYBACK_PAUSE': controller.playback_pause,
        'PLAYBACK_PLAY_PAUSE': controller.playback_play_pause,
        'PLAYBACK_STOP': controller.playback_stop,
        'PLAYBACK_RESTART': controller.playback_restart,
        'PLAYBACK_SEEK_FORWARD_SMALL': controller.playback_seek_forward_small,
        'PLAYBACK_SEEK_BACKWARD_SMALL': controller.playback_seek_backward_small,
        'PLAYBACK_SEEK_FORWARD_LARGE': controller.playback_seek_forward_large,
        'PLAYBACK_SEEK_BACKWARD_LARGE': controller.playback_seek_backward_large,
        'PLAYBACK_JUMP_TO_BEGINNING': controller.playback_jump_to_beginning,
        'PLAYBACK_JUMP_TO_END': controller.playback_jump_to_end,
        'PLAYBACK_NEXT_VIDEO': controller.playback_next_video,
        'PLAYBACK_PREVIOUS_VIDEO': controller.playback_previous_video,
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
                    
                    # Check if command has parameters (format: COMMAND:param)
                    parts = line.split(':', 1)
                    command = parts[0]
                    param = parts[1] if len(parts) > 1 else None
                    
                    if command in commands:
                        try:
                            # Handle commands with parameters (currently only BROWSER_OPEN_URL)
                            if param and command == 'BROWSER_OPEN_URL':
                                result = controller.browser_open_url(param)
                            else:
                                result = commands[command]()
                            
                            response = f"STATUS:{result}\n"
                            ser.write(response.encode('utf-8'))
                            print(f"Response sent: {result}")
                        except Exception as e:
                            error_msg = f"ERROR:{command} - {str(e)}\n"
                            ser.write(error_msg.encode('utf-8'))
                            print(f"Error executing {command}: {e}")
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
