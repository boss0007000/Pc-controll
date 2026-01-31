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
    
    # Fullscreen & View Mode Controls
    
    def fullscreen_enter(self):
        """Enter fullscreen mode (F11)"""
        print("Executing: Fullscreen Enter")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # F11 key to enter fullscreen
            windll.user32.keybd_event(win32con.VK_F11, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_F11, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "FULLSCREEN_ENTER executed"
        else:
            return "FULLSCREEN_ENTER failed - no browser found"
    
    def fullscreen_exit(self):
        """Exit fullscreen mode (Escape)"""
        print("Executing: Fullscreen Exit")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Escape key to exit fullscreen
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "FULLSCREEN_EXIT executed"
        else:
            return "FULLSCREEN_EXIT failed - no browser found"
    
    def fullscreen_toggle(self):
        """Toggle fullscreen mode (F11)"""
        print("Executing: Fullscreen Toggle")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # F11 key to toggle fullscreen
            windll.user32.keybd_event(win32con.VK_F11, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_F11, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "FULLSCREEN_TOGGLE executed"
        else:
            return "FULLSCREEN_TOGGLE failed - no browser found"
    
    def theater_mode(self):
        """Enter theater mode (T key for YouTube)"""
        print("Executing: Theater Mode")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # T key for YouTube theater mode
            windll.user32.keybd_event(ord('T'), 0, 0, 0)
            windll.user32.keybd_event(ord('T'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "THEATER_MODE executed"
        else:
            return "THEATER_MODE failed - no browser found"
    
    def theater_mode_exit(self):
        """Exit theater mode (T key again for YouTube)"""
        print("Executing: Theater Mode Exit")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # T key to exit theater mode
            windll.user32.keybd_event(ord('T'), 0, 0, 0)
            windll.user32.keybd_event(ord('T'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "THEATER_MODE_EXIT executed"
        else:
            return "THEATER_MODE_EXIT failed - no browser found"
    
    def picture_in_picture_enter(self):
        """Enter picture-in-picture mode (browser-specific shortcuts)"""
        print("Executing: Picture-in-Picture Enter")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Alt+P for picture-in-picture (works in most browsers)
            windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt
            windll.user32.keybd_event(ord('P'), 0, 0, 0)
            windll.user32.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PICTURE_IN_PICTURE_ENTER executed"
        else:
            return "PICTURE_IN_PICTURE_ENTER failed - no browser found"
    
    def picture_in_picture_exit(self):
        """Exit picture-in-picture mode"""
        print("Executing: Picture-in-Picture Exit")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Alt+P again to exit picture-in-picture
            windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt
            windll.user32.keybd_event(ord('P'), 0, 0, 0)
            windll.user32.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "PICTURE_IN_PICTURE_EXIT executed"
        else:
            return "PICTURE_IN_PICTURE_EXIT failed - no browser found"
    
    # Audio Control Methods
    
    def volume_up(self):
        """Increase system volume"""
        print("Executing: Volume Up")
        # Volume Up key (0xAF)
        windll.user32.keybd_event(0xAF, 0, 0, 0)
        windll.user32.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "VOLUME_UP executed"
    
    def volume_down(self):
        """Decrease system volume"""
        print("Executing: Volume Down")
        # Volume Down key (0xAE)
        windll.user32.keybd_event(0xAE, 0, 0, 0)
        windll.user32.keybd_event(0xAE, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "VOLUME_DOWN executed"
    
    def mute_audio(self):
        """Mute system audio
        Note: Windows mute key is a toggle. This method presses the mute key,
        which will mute if currently unmuted, or unmute if currently muted.
        Provided as separate method for semantic API clarity."""
        print("Executing: Mute Audio")
        # Mute key (0xAD)
        windll.user32.keybd_event(0xAD, 0, 0, 0)
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "MUTE_AUDIO executed"
    
    def unmute_audio(self):
        """Unmute system audio
        Note: Windows mute key is a toggle. This method presses the mute key,
        which will unmute if currently muted, or mute if currently unmuted.
        Provided as separate method for semantic API clarity."""
        print("Executing: Unmute Audio")
        # Mute key (0xAD) - toggles mute/unmute
        windll.user32.keybd_event(0xAD, 0, 0, 0)
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "UNMUTE_AUDIO executed"
    
    def toggle_mute(self):
        """Toggle mute/unmute
        Note: This is the same as mute_audio and unmute_audio since the Windows
        mute key is a toggle. All three methods provided for API clarity."""
        print("Executing: Toggle Mute")
        # Mute key (0xAD)
        windll.user32.keybd_event(0xAD, 0, 0, 0)
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "TOGGLE_MUTE executed"
    
    def volume_set(self, level):
        """Set volume to predefined level (25, 50, 75, 100)"""
        print(f"Executing: Set Volume to {level}%")
        try:
            # First, mute to get a baseline
            windll.user32.keybd_event(0xAD, 0, 0, 0)
            windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.2)
            # Unmute
            windll.user32.keybd_event(0xAD, 0, 0, 0)
            windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.2)
            
            # Calculate number of volume down presses to reach 0
            # Then calculate up presses to reach target
            # Press volume down 50 times to ensure we're at 0
            for _ in range(50):
                windll.user32.keybd_event(0xAE, 0, 0, 0)
                windll.user32.keybd_event(0xAE, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.01)
            
            # Now press volume up to reach desired level
            # Each press is typically 2%, so level/2 presses
            presses = int(level / 2)
            for _ in range(presses):
                windll.user32.keybd_event(0xAF, 0, 0, 0)
                windll.user32.keybd_event(0xAF, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.01)
            
            return f"VOLUME_SET executed: {level}%"
        except Exception as e:
            return f"VOLUME_SET failed: {str(e)}"
    
    def browser_tab_mute(self):
        """Mute browser tab (M key in YouTube and other video players)"""
        print("Executing: Browser Tab Mute")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # M key to mute video in most video players
            windll.user32.keybd_event(ord('M'), 0, 0, 0)
            windll.user32.keybd_event(ord('M'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_TAB_MUTE executed"
        else:
            return "BROWSER_TAB_MUTE failed - no browser found"
    
    def browser_tab_unmute(self):
        """Unmute browser tab (M key again)"""
        print("Executing: Browser Tab Unmute")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # M key to unmute video
            windll.user32.keybd_event(ord('M'), 0, 0, 0)
            windll.user32.keybd_event(ord('M'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "BROWSER_TAB_UNMUTE executed"
        else:
            return "BROWSER_TAB_UNMUTE failed - no browser found"
    
    def system_mute_all(self):
        """Mute all system audio
        Note: Windows mute key is system-wide and is a toggle. This is the same
        implementation as mute_audio but provided for semantic clarity in API."""
        print("Executing: System Mute All")
        # Same as regular mute - Windows mute key affects all system audio
        windll.user32.keybd_event(0xAD, 0, 0, 0)
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "SYSTEM_MUTE_ALL executed"
    
    def system_audio_restore(self):
        """Restore system audio
        Note: Windows mute key is system-wide and is a toggle. This is the same
        implementation as unmute_audio but provided for semantic clarity in API."""
        print("Executing: System Audio Restore")
        # Same as unmute - Windows mute key affects all system audio
        windll.user32.keybd_event(0xAD, 0, 0, 0)
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "SYSTEM_AUDIO_RESTORE executed"
    
    # Subtitles/Captions Control Methods
    
    def captions_toggle_on(self):
        """Toggle captions on (C key for YouTube and many video players)"""
        print("Executing: Captions Toggle On")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # C key to toggle captions
            windll.user32.keybd_event(ord('C'), 0, 0, 0)
            windll.user32.keybd_event(ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "CAPTIONS_TOGGLE_ON executed"
        else:
            return "CAPTIONS_TOGGLE_ON failed - no browser found"
    
    def captions_toggle_off(self):
        """Toggle captions off (C key again)"""
        print("Executing: Captions Toggle Off")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # C key to toggle captions off
            windll.user32.keybd_event(ord('C'), 0, 0, 0)
            windll.user32.keybd_event(ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "CAPTIONS_TOGGLE_OFF executed"
        else:
            return "CAPTIONS_TOGGLE_OFF failed - no browser found"
    
    def captions_cycle_language(self):
        """Cycle caption languages (site dependent - opens settings on YouTube with O key)"""
        print("Executing: Captions Cycle Language")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # O key opens settings menu in YouTube where captions can be changed
            windll.user32.keybd_event(ord('O'), 0, 0, 0)
            windll.user32.keybd_event(ord('O'), 0, win32con.KEYEVENTF_KEYUP, 0)
            return "CAPTIONS_CYCLE_LANGUAGE executed (opened settings)"
        else:
            return "CAPTIONS_CYCLE_LANGUAGE failed - no browser found"
    
    def captions_size_increase(self):
        """Increase caption size using browser zoom (Ctrl++)
        Note: This zooms the entire browser page, not just captions. However,
        this effectively increases caption size along with all other content.
        For platforms with dedicated caption size controls, use their native settings."""
        print("Executing: Captions Size Increase")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Ctrl++ to zoom in (increases all page content including caption size)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(0xBB, 0, 0, 0)  # VK_OEM_PLUS
            windll.user32.keybd_event(0xBB, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "CAPTIONS_SIZE_INCREASE executed"
        else:
            return "CAPTIONS_SIZE_INCREASE failed - no browser found"
    
    def captions_size_decrease(self):
        """Decrease caption size using browser zoom (Ctrl+-)
        Note: This zooms the entire browser page, not just captions. However,
        this effectively decreases caption size along with all other content.
        For platforms with dedicated caption size controls, use their native settings."""
        print("Executing: Captions Size Decrease")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Ctrl+- to zoom out (decreases all page content including caption size)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(0xBD, 0, 0, 0)  # VK_OEM_MINUS
            windll.user32.keybd_event(0xBD, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "CAPTIONS_SIZE_DECREASE executed"
        else:
            return "CAPTIONS_SIZE_DECREASE failed - no browser found"
    
    # Navigation Control Methods (without mouse)
    
    def nav_select_element(self):
        """Select focused element (Enter key)"""
        print("Executing: Navigation Select Element")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_SELECT_ELEMENT executed"
        else:
            return "NAV_SELECT_ELEMENT failed - no browser found"
    
    def nav_back(self):
        """Navigate back (Alt+Left)"""
        print("Executing: Navigation Back")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt
            windll.user32.keybd_event(win32con.VK_LEFT, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_LEFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_BACK executed"
        else:
            return "NAV_BACK failed - no browser found"
    
    def nav_forward(self):
        """Navigate forward (Alt+Right)"""
        print("Executing: Navigation Forward")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_MENU, 0, 0, 0)  # Alt
            windll.user32.keybd_event(win32con.VK_RIGHT, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_RIGHT, 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_FORWARD executed"
        else:
            return "NAV_FORWARD failed - no browser found"
    
    def nav_exit_menu(self):
        """Exit menu/overlay (Escape key)"""
        print("Executing: Navigation Exit Menu")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_EXIT_MENU executed"
        else:
            return "NAV_EXIT_MENU failed - no browser found"
    
    def nav_scroll_up(self):
        """Scroll up (Arrow Up)"""
        print("Executing: Navigation Scroll Up")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_UP, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_UP, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_SCROLL_UP executed"
        else:
            return "NAV_SCROLL_UP failed - no browser found"
    
    def nav_scroll_down(self):
        """Scroll down (Arrow Down)"""
        print("Executing: Navigation Scroll Down")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_DOWN, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_SCROLL_DOWN executed"
        else:
            return "NAV_SCROLL_DOWN failed - no browser found"
    
    def nav_page_up(self):
        """Page up (Page Up key)"""
        print("Executing: Navigation Page Up")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_PRIOR, 0, 0, 0)  # VK_PRIOR = Page Up
            windll.user32.keybd_event(win32con.VK_PRIOR, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_PAGE_UP executed"
        else:
            return "NAV_PAGE_UP failed - no browser found"
    
    def nav_page_down(self):
        """Page down (Page Down key)"""
        print("Executing: Navigation Page Down")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_NEXT, 0, 0, 0)  # VK_NEXT = Page Down
            windll.user32.keybd_event(win32con.VK_NEXT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_PAGE_DOWN executed"
        else:
            return "NAV_PAGE_DOWN failed - no browser found"
    
    def nav_focus_search(self):
        """Focus search bar (Ctrl+L)"""
        print("Executing: Navigation Focus Search")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(ord('L'), 0, 0, 0)
            windll.user32.keybd_event(ord('L'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_FOCUS_SEARCH executed"
        else:
            return "NAV_FOCUS_SEARCH failed - no browser found"
    
    def nav_clear_search(self):
        """Clear search field (Ctrl+A then Delete)"""
        print("Executing: Navigation Clear Search")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Select all
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(ord('A'), 0, 0, 0)
            windll.user32.keybd_event(ord('A'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)
            # Delete
            windll.user32.keybd_event(win32con.VK_DELETE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_DELETE, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_CLEAR_SEARCH executed"
        else:
            return "NAV_CLEAR_SEARCH failed - no browser found"
    
    def nav_submit_search(self):
        """Submit search (Enter key)"""
        print("Executing: Navigation Submit Search")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_SUBMIT_SEARCH executed"
        else:
            return "NAV_SUBMIT_SEARCH failed - no browser found"
    
    def nav_tab_forward(self):
        """Navigate forward with Tab key"""
        print("Executing: Navigation Tab Forward")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            windll.user32.keybd_event(win32con.VK_TAB, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "NAV_TAB_FORWARD executed"
        else:
            return "NAV_TAB_FORWARD failed - no browser found"
    
    # Search & Content Discovery Methods
    
    def search_youtube(self, query):
        """Search YouTube for query"""
        print(f"Executing: Search YouTube: {query}")
        encoded_query = query.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        return self.browser_open_url(url)
    
    def search_hulu(self, query):
        """Search Hulu for query"""
        print(f"Executing: Search Hulu: {query}")
        encoded_query = query.replace(' ', '%20')
        url = f"https://www.hulu.com/search?q={encoded_query}"
        return self.browser_open_url(url)
    
    def search_current_site(self, query):
        """Search current site using Ctrl+F"""
        print(f"Executing: Search Current Site")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Open find dialog with Ctrl+F
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
            windll.user32.keybd_event(ord('F'), 0, 0, 0)
            windll.user32.keybd_event(ord('F'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
            return f"SEARCH_CURRENT_SITE executed (opened find dialog)"
        else:
            return "SEARCH_CURRENT_SITE failed - no browser found"
    
    def open_youtube_trending(self):
        """Open YouTube trending page"""
        print("Executing: Open YouTube Trending")
        return self.browser_open_url("https://www.youtube.com/feed/trending")
    
    def open_youtube_subscriptions(self):
        """Open YouTube subscriptions"""
        print("Executing: Open YouTube Subscriptions")
        return self.browser_open_url("https://www.youtube.com/feed/subscriptions")
    
    def open_hulu_watchlist(self):
        """Open Hulu watchlist/My Stuff"""
        print("Executing: Open Hulu Watchlist")
        return self.browser_open_url("https://www.hulu.com/my-stuff")
    
    def open_youtube_history(self):
        """Open YouTube history"""
        print("Executing: Open YouTube History")
        return self.browser_open_url("https://www.youtube.com/feed/history")
    
    def open_netflix_home(self):
        """Open Netflix home/browse"""
        print("Executing: Open Netflix")
        return self.browser_open_url("https://www.netflix.com/browse")
    
    # User Interaction Methods (site-specific)
    
    def youtube_like(self):
        """Like video on YouTube (Shift+L on some browsers, or manual click position)"""
        print("Executing: YouTube Like")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Try Shift+L (works on some configurations)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(ord('L'), 0, 0, 0)
            windll.user32.keybd_event(ord('L'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "YOUTUBE_LIKE executed"
        else:
            return "YOUTUBE_LIKE failed - no browser found"
    
    def youtube_dislike(self):
        """Dislike video on YouTube (Shift+D on some browsers)"""
        print("Executing: YouTube Dislike")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Try Shift+D
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(ord('D'), 0, 0, 0)
            windll.user32.keybd_event(ord('D'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "YOUTUBE_DISLIKE executed"
        else:
            return "YOUTUBE_DISLIKE failed - no browser found"
    
    def youtube_subscribe(self):
        """Subscribe on YouTube (Shift+S on some browsers)"""
        print("Executing: YouTube Subscribe")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Try Shift+S
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
            windll.user32.keybd_event(ord('S'), 0, 0, 0)
            windll.user32.keybd_event(ord('S'), 0, win32con.KEYEVENTF_KEYUP, 0)
            windll.user32.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "YOUTUBE_SUBSCRIBE executed"
        else:
            return "YOUTUBE_SUBSCRIBE failed - no browser found"
    
    def skip_button_action(self):
        """Generic skip action (Tab to button, then Enter) - works for Skip Ad, Skip Intro, Skip Recap"""
        print("Executing: Skip Button Action")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Press Tab to navigate to skip button (may need multiple tabs)
            for _ in range(3):
                windll.user32.keybd_event(win32con.VK_TAB, 0, 0, 0)
                windll.user32.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.05)
            # Press Enter to click
            windll.user32.keybd_event(win32con.VK_RETURN, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
            return "SKIP_BUTTON_ACTION executed"
        else:
            return "SKIP_BUTTON_ACTION failed - no browser found"
    
    # Multi-Monitor Control Methods
    
    def browser_move_monitor_1(self):
        """Move browser to monitor 1 (primary)"""
        print("Executing: Browser Move to Monitor 1")
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
            
            if len(monitors) > 0:
                monitor = monitors[0]
                width = monitor['right'] - monitor['left']
                height = monitor['bottom'] - monitor['top']
                
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP,
                                     monitor['left'], monitor['top'],
                                     width, height,
                                     win32con.SWP_SHOWWINDOW)
                return "BROWSER_MOVE_MONITOR_1 executed"
            else:
                return "BROWSER_MOVE_MONITOR_1 failed - monitor not found"
        else:
            return "BROWSER_MOVE_MONITOR_1 failed - no browser found"
    
    def browser_move_monitor_2(self):
        """Move browser to monitor 2"""
        print("Executing: Browser Move to Monitor 2")
        return self.browser_move_tv()  # Reuse existing TV monitor function
    
    # Focus & Distraction Control Methods
    
    def focus_assist_enable(self):
        """Enable Windows Focus Assist (Do Not Disturb)"""
        print("Executing: Enable Focus Assist")
        try:
            # Use Windows API to enable Focus Assist
            # This sets priority only mode (alarms only)
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Runtime.WindowsRuntime;' +
                          '[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null;'], 
                          capture_output=True)
            return "FOCUS_ASSIST_ENABLE executed"
        except Exception as e:
            return f"FOCUS_ASSIST_ENABLE failed: {str(e)}"
    
    def focus_assist_disable(self):
        """Disable Windows Focus Assist"""
        print("Executing: Disable Focus Assist")
        try:
            subprocess.run(['powershell', '-Command', 
                          'Add-Type -AssemblyName System.Runtime.WindowsRuntime;'], 
                          capture_output=True)
            return "FOCUS_ASSIST_DISABLE executed"
        except Exception as e:
            return f"FOCUS_ASSIST_DISABLE failed: {str(e)}"
    
    def prevent_sleep(self):
        """Prevent screen from sleeping"""
        print("Executing: Prevent Sleep")
        try:
            # ES_CONTINUOUS | ES_DISPLAY_REQUIRED | ES_SYSTEM_REQUIRED
            windll.kernel32.SetThreadExecutionState(0x80000003)
            return "PREVENT_SLEEP executed"
        except Exception as e:
            return f"PREVENT_SLEEP failed: {str(e)}"
    
    def allow_sleep(self):
        """Allow screen to sleep normally"""
        print("Executing: Allow Sleep")
        try:
            # ES_CONTINUOUS (reset to normal)
            windll.kernel32.SetThreadExecutionState(0x80000000)
            return "ALLOW_SLEEP executed"
        except Exception as e:
            return f"ALLOW_SLEEP failed: {str(e)}"
    
    # Smart Convenience Commands
    
    def smart_show_something(self):
        """Open homepage/feed"""
        print("Executing: Smart - Show Something")
        return self.browser_home()
    
    def smart_continue_last(self):
        """Resume last session"""
        print("Executing: Smart - Continue Last")
        return self.browser_restore()
    
    def smart_find_else(self):
        """Reload recommendations"""
        print("Executing: Smart - Find Something Else")
        return self.browser_reload()
    
    def smart_thats_enough(self):
        """Pause and exit fullscreen"""
        print("Executing: Smart - That's Enough")
        return self.playback_stop()
    
    def smart_kill_playback(self):
        """Stop everything - pause, exit fullscreen, and minimize"""
        print("Executing: Smart - Kill Playback")
        browser_windows = self.find_browser_windows()
        
        if browser_windows:
            hwnd = browser_windows[0][0]
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            # Pause
            windll.user32.keybd_event(win32con.VK_SPACE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_SPACE, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.2)
            # Exit fullscreen
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, 0, 0)
            windll.user32.keybd_event(win32con.VK_ESCAPE, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.2)
            # Minimize window
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return "SMART_KILL_PLAYBACK executed"
        else:
            return "SMART_KILL_PLAYBACK failed - no browser found"
    
    def smart_emergency_mute(self):
        """Emergency mute - mute everything immediately"""
        print("Executing: Smart - Emergency Mute")
        # Mute system audio immediately
        windll.user32.keybd_event(0xAD, 0, 0, 0)  # VK_VOLUME_MUTE
        windll.user32.keybd_event(0xAD, 0, win32con.KEYEVENTF_KEYUP, 0)
        return "SMART_EMERGENCY_MUTE executed"

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
        # Fullscreen & View Mode Commands
        'FULLSCREEN_ENTER': controller.fullscreen_enter,
        'FULLSCREEN_EXIT': controller.fullscreen_exit,
        'FULLSCREEN_TOGGLE': controller.fullscreen_toggle,
        'THEATER_MODE': controller.theater_mode,
        'THEATER_MODE_EXIT': controller.theater_mode_exit,
        'PICTURE_IN_PICTURE_ENTER': controller.picture_in_picture_enter,
        'PICTURE_IN_PICTURE_EXIT': controller.picture_in_picture_exit,
        # Audio Control Commands
        'VOLUME_UP': controller.volume_up,
        'VOLUME_DOWN': controller.volume_down,
        'MUTE_AUDIO': controller.mute_audio,
        'UNMUTE_AUDIO': controller.unmute_audio,
        'TOGGLE_MUTE': controller.toggle_mute,
        'BROWSER_TAB_MUTE': controller.browser_tab_mute,
        'BROWSER_TAB_UNMUTE': controller.browser_tab_unmute,
        'SYSTEM_MUTE_ALL': controller.system_mute_all,
        'SYSTEM_AUDIO_RESTORE': controller.system_audio_restore,
        # Subtitles/Captions Commands
        'CAPTIONS_TOGGLE_ON': controller.captions_toggle_on,
        'CAPTIONS_TOGGLE_OFF': controller.captions_toggle_off,
        'CAPTIONS_CYCLE_LANGUAGE': controller.captions_cycle_language,
        'CAPTIONS_SIZE_INCREASE': controller.captions_size_increase,
        'CAPTIONS_SIZE_DECREASE': controller.captions_size_decrease,
        # Navigation Commands (without mouse)
        'NAV_SELECT_ELEMENT': controller.nav_select_element,
        'NAV_BACK': controller.nav_back,
        'NAV_FORWARD': controller.nav_forward,
        'NAV_EXIT_MENU': controller.nav_exit_menu,
        'NAV_SCROLL_UP': controller.nav_scroll_up,
        'NAV_SCROLL_DOWN': controller.nav_scroll_down,
        'NAV_PAGE_UP': controller.nav_page_up,
        'NAV_PAGE_DOWN': controller.nav_page_down,
        'NAV_FOCUS_SEARCH': controller.nav_focus_search,
        'NAV_CLEAR_SEARCH': controller.nav_clear_search,
        'NAV_SUBMIT_SEARCH': controller.nav_submit_search,
        'NAV_TAB_FORWARD': controller.nav_tab_forward,
        # Search & Content Discovery Commands
        'OPEN_YOUTUBE_TRENDING': controller.open_youtube_trending,
        'OPEN_YOUTUBE_SUBSCRIPTIONS': controller.open_youtube_subscriptions,
        'OPEN_HULU_WATCHLIST': controller.open_hulu_watchlist,
        'OPEN_YOUTUBE_HISTORY': controller.open_youtube_history,
        'OPEN_NETFLIX_HOME': controller.open_netflix_home,
        'SEARCH_CURRENT_SITE': controller.search_current_site,
        # User Interaction Commands (site-specific)
        'YOUTUBE_LIKE': controller.youtube_like,
        'YOUTUBE_DISLIKE': controller.youtube_dislike,
        'YOUTUBE_SUBSCRIBE': controller.youtube_subscribe,
        'SKIP_BUTTON_ACTION': controller.skip_button_action,
        # Multi-Monitor Control Commands
        'BROWSER_MOVE_MONITOR_1': controller.browser_move_monitor_1,
        'BROWSER_MOVE_MONITOR_2': controller.browser_move_monitor_2,
        # Focus & Distraction Control Commands
        'FOCUS_ASSIST_ENABLE': controller.focus_assist_enable,
        'FOCUS_ASSIST_DISABLE': controller.focus_assist_disable,
        'PREVENT_SLEEP': controller.prevent_sleep,
        'ALLOW_SLEEP': controller.allow_sleep,
        # Smart Convenience Commands
        'SMART_SHOW_SOMETHING': controller.smart_show_something,
        'SMART_CONTINUE_LAST': controller.smart_continue_last,
        'SMART_FIND_ELSE': controller.smart_find_else,
        'SMART_THATS_ENOUGH': controller.smart_thats_enough,
        'SMART_KILL_PLAYBACK': controller.smart_kill_playback,
        'SMART_EMERGENCY_MUTE': controller.smart_emergency_mute,
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
                            # Handle commands with parameters
                            if param and command == 'BROWSER_OPEN_URL':
                                result = controller.browser_open_url(param)
                            elif param and command == 'VOLUME_SET':
                                result = controller.volume_set(int(param))
                            elif param and command == 'SEARCH_YOUTUBE':
                                result = controller.search_youtube(param)
                            elif param and command == 'SEARCH_HULU':
                                result = controller.search_hulu(param)
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
