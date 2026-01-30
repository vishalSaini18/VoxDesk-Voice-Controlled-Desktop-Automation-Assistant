import subprocess
import pyautogui
import pygetwindow as gw
import time

# Import pywinauto for Windows UI Automation
try:
    from pywinauto import Desktop
    from pywinauto.uia_defines import IUIA
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    print("Warning: pywinauto not available, using fallback methods")

# Global flag to stop focus search
STOP_FOCUS = False

def stop_focus_search():
    """Call this to stop any ongoing focus/open search."""
    global STOP_FOCUS
    STOP_FOCUS = True

def reset_focus_stop():
    """Reset the stop flag before starting a new search."""
    global STOP_FOCUS
    STOP_FOCUS = False

def is_stop_requested():
    """Check if stop was requested."""
    return STOP_FOCUS



def focus_element_direct(target):
    """
    FAST: Directly find and focus an element by name using Windows UI Automation.
    No keyboard scanning - searches the UI tree directly.
    
    Works for: Desktop icons, File Explorer items, taskbar, Start menu, etc.
    """
    if not PYWINAUTO_AVAILABLE:
        return False
    
    target = target.lower().strip()
    if not target:
        return False
    
    try:
        # Get the desktop (root of all UI)
        desktop = Desktop(backend="uia")
        
        # Search in all top-level windows
        for window in desktop.windows():
            try:
                # Try to find element by partial name match
                # Use depth limit to avoid searching too deep
                elements = window.descendants(depth=8)
                
                for elem in elements:
                    try:
                        name = elem.element_info.name
                        if name and target in name.lower():
                            # Found it! Try to focus/select it
                            elem.set_focus()
                            return True
                    except:
                        continue
            except:
                continue
        
        return False
    except Exception as e:
        print(f"Direct focus error: {e}")
        return False


def focus_desktop_icon(target):
    """
    FAST: Directly focus a desktop icon by name.
    """
    if not PYWINAUTO_AVAILABLE:
        return False
    
    target = target.lower().strip()
    
    try:
        desktop = Desktop(backend="uia")
        
        # Find the desktop icons list
        # Desktop icons are in "Program Manager" -> "Desktop" -> "Folder View"
        shell = desktop.window(class_name="Progman")
        folder_view = shell.child_window(class_name="SysListView32")
        
        # Get all items
        items = folder_view.children()
        for item in items:
            try:
                name = item.element_info.name
                if name and target in name.lower():
                    item.set_focus()
                    item.select()
                    return True
            except:
                continue
        
        return False
    except Exception as e:
        return False


def focus_explorer_item(target):
    """
    FAST: Focus an item in the active File Explorer window.
    """
    if not PYWINAUTO_AVAILABLE:
        return False
    
    target = target.lower().strip()
    
    try:
        desktop = Desktop(backend="uia")
        
        # Find File Explorer windows
        for window in desktop.windows():
            try:
                if "explorer" in window.element_info.class_name.lower() or \
                   "cabinetwclass" in window.element_info.class_name.lower():
                    
                    # Search for item in this explorer window
                    items = window.descendants(control_type="ListItem", depth=10)
                    for item in items:
                        try:
                            name = item.element_info.name
                            if name and target in name.lower():
                                item.set_focus()
                                item.select()
                                return True
                        except:
                            continue
            except:
                continue
        
        return False
    except:
        return False

FOCUS_PREFIXES = [
    "go to",
    "focus",
]

OPEN_PREFIXES = [
    "open",
    "launch",
    "start"
]


def focus_window(target):
    """
    Find and focus a window by matching target name (case-insensitive, partial match).
    
    This function searches through all visible windows and focuses the first one
    whose title contains the target string.
    
    Args:
        target: String to search for in window titles (case-insensitive, partial match)
    
    Returns:
        True if window found and focused, False otherwise
    """
    target = target.lower().strip()
    
    if not target:
        return False
    
    try:
        # Get all visible windows
        all_windows = gw.getAllWindows()
        
        # Filter for visible windows with titles
        visible_windows = [w for w in all_windows if w.title and w.visible]
        
        # Search for matching window
        for window in visible_windows:
            window_title = window.title.lower()
            
            # Check if target matches window title (partial match)
            if target in window_title:
                try:
                    # Restore if minimized
                    if window.isMinimized:
                        window.restore()
                        time.sleep(0.2)
                    
                    # Bring to front and activate
                    window.activate()
                    return True
                except Exception as e:
                    print(f"Error activating window: {e}")
                    # Fallback: try using pyautogui
                    try:
                        window.minimize()
                        time.sleep(0.1)
                        window.restore()
                        return True
                    except:
                        pass
        
        # No exact partial match found, try fuzzy matching
        # Check if any word from target matches any word in window title
        target_words = target.split()
        for window in visible_windows:
            window_title = window.title.lower()
            for word in target_words:
                if len(word) > 2 and word in window_title:  # Skip very short words
                    try:
                        if window.isMinimized:
                            window.restore()
                            time.sleep(0.2)
                        window.activate()
                        return True
                    except:
                        pass
        
        return False
        
    except Exception as e:
        print(f"Error in focus_window: {e}")
        return False


def get_all_window_titles():
    """
    Returns a list of all visible window titles for debugging.
    """
    try:
        all_windows = gw.getAllWindows()
        return [w.title for w in all_windows if w.title and w.visible]
    except:
        return []


def get_focused_name():
    # 1️⃣ Try pywinauto UI Automation (best method)
    if PYWINAUTO_AVAILABLE:
        try:
            iuia = IUIA()
            focused = iuia.iuia.GetFocusedElement()
            if focused:
                name = focused.CurrentName
                if name:
                    return name.lower()
        except Exception as e:
            pass
    
    # 2️⃣ Fallback: Try AHK script
    try:
        r = subprocess.run(
            ["AutoHotkey.exe", "get_focused_name.ahk"],
            capture_output=True,
            text=True,
            timeout=2
        )
        name = r.stdout.strip().lower()
        if name:
            return name
    except:
        pass

    # 3️⃣ Fallback: active window title
    try:
        win = gw.getActiveWindow()
        if win and win.title:
            return win.title.lower()
    except:
        pass

    return ""



def scan_zone_full(target, max_attempts=100):
    """
    Fully explore current zone using arrow directions.
    Uses multi-directional sweep to handle both lists and grids.
    
    Strategy:
    1. Try Home key to go to start
    2. Scan DOWN direction (handles lists, menus, trees)
    3. Try RIGHT direction (handles grids, multi-column layouts)
    4. After each RIGHT move, try DOWN again (explore new columns)
    
    Returns:
        True if target found, False otherwise
    """
    target = target.lower()
    visited = set()
    last_name = ""
    
    # Check current position first
    start_name = get_focused_name()
    if start_name:
        visited.add(start_name)
        if target in start_name:
            return True
        last_name = start_name
    
    # Try Home to go to start of zone
    pyautogui.press("home")
    time.sleep(0.15)
    
    start_name = get_focused_name()
    if start_name and target in start_name:
        return True
    if start_name:
        visited.add(start_name)
        last_name = start_name
    
    # PRIMARY SCAN: DOWN direction
    stuck_count = 0
    for _ in range(max_attempts):
        if is_stop_requested():
            return False
        pyautogui.press("down")
        time.sleep(0.12)
        
        name = get_focused_name()
        
        # Check for target
        if name and target in name:
            return True
        
        # Detect if stuck (same name or cycling)
        if not name or name == last_name or name in visited:
            stuck_count += 1
            if stuck_count >= 3:
                break
        else:
            stuck_count = 0
            visited.add(name)
            last_name = name
    
    # Go back to start
    pyautogui.press("home")
    time.sleep(0.15)
    
    # SECONDARY SCAN: RIGHT direction for grids
    stuck_count = 0
    last_name = get_focused_name() or ""
    
    for _ in range(max_attempts):
        if is_stop_requested():
            return False
        pyautogui.press("right")
        time.sleep(0.12)
        
        name = get_focused_name()
        
        if name and target in name:
            return True
        
        if not name or name == last_name or name in visited:
            stuck_count += 1
            if stuck_count >= 3:
                break
        else:
            stuck_count = 0
            visited.add(name)
            last_name = name
            
            # After moving right, scan down in this column
            inner_stuck = 0
            inner_last = name
            for _ in range(30):
                if is_stop_requested():
                    return False
                pyautogui.press("down")
                time.sleep(0.12)
                
                down_name = get_focused_name()
                
                if down_name and target in down_name:
                    return True
                
                if not down_name or down_name == inner_last or down_name in visited:
                    inner_stuck += 1
                    if inner_stuck >= 2:
                        break
                else:
                    inner_stuck = 0
                    visited.add(down_name)
                    inner_last = down_name
            
            # Go back up to continue scanning right
            pyautogui.press("home")
            time.sleep(0.1)
    
    return False


def focus_target(target, max_zones=50):
    """
    Find and focus target element. Uses fast direct methods first,
    falls back to keyboard scanning if needed.
    """
    reset_focus_stop()  # Reset stop flag for new search
    target_lower = target.lower()
    
    # ========== FAST METHODS (try these first) ==========
    
    # 1. Try desktop icons (fastest for desktop)
    if focus_desktop_icon(target):
        return True
    
    # 2. Try File Explorer items
    if focus_explorer_item(target):
        return True
    
    # 3. Try general UI element search
    if focus_element_direct(target):
        return True
    
    # ========== SLOW FALLBACK: Keyboard scanning ==========
    
    visited_zones = {}
    # Get initial position
    initial_name = get_focused_name()
    if not initial_name:
        # Try to get focus by clicking desktop
        pyautogui.press("win")
        time.sleep(0.3)
        pyautogui.press("esc")
        time.sleep(0.2)
        initial_name = get_focused_name()
        if not initial_name:
            return False
    
    # Check if we're already on target
    if target_lower in initial_name:
        return True
    
    # Mark starting zone
    visited_zones[initial_name] = 1
    
    # Fully scan starting zone
    if scan_zone_full(target):
        return True
    
    # Cycle through TAB zones
    cycle_complete_count = 0
    
    for _ in range(max_zones):
        if is_stop_requested():
            return False
        # Move to next zone
        pyautogui.press("tab")
        time.sleep(0.12)
        
        zone_id = get_focused_name()
        if not zone_id:
            continue
        
        # Check if zone's first element matches target
        if target_lower in zone_id:
            return True
        
        # TAB CYCLE DETECTION
        if zone_id in visited_zones:
            visited_zones[zone_id] += 1
            cycle_complete_count += 1
            
            if cycle_complete_count >= 3:
                return False
        else:
            visited_zones[zone_id] = 1
            cycle_complete_count = 0
        
        # Fully scan this zone
        if scan_zone_full(target):
            return True
    
    return False


def open_target(target):
    """
    Find target element and press Enter to open/activate it.
    
    Args:
        target: String to search for (case-insensitive, partial match)
    
    Returns:
        True if target found and opened, False otherwise
    """
    if focus_target(target):
        time.sleep(0.2)
        pyautogui.press("enter")
        return True
    return False

