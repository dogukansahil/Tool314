import os
from tool314.core.menu import Menu
from tool314.core.config_mgr import ConfigManager

# Default path for Raspberry Pi, but can be overridden for testing
CONFIG_PATH = os.getenv("TOOL314_CONFIG_PATH", "/boot/config.txt")

class FanControl:
    @staticmethod
    def show_menu():
        menu = Menu("Fan Control")
        menu.add_option("Enable Fan (GPIO 14, 80C)", FanControl.enable_default)
        menu.add_option("Set Custom Fan Settings", FanControl.set_custom)
        menu.add_option("Disable Fan", FanControl.disable)
        menu.display()

    @staticmethod
    def enable_default():
        # dtoverlay=gpio-fan,gpiopin=14,temp=80000
        FanControl.apply_settings(14, 80)

    @staticmethod
    def set_custom():
        try:
            pin = input("Enter GPIO Pin (default 14): ").strip() or "14"
            temp = input("Enter Trigger Temp in Celsius (default 60): ").strip() or "60"
            FanControl.apply_settings(int(pin), int(temp))
        except ValueError:
            print("Invalid input.")

    @staticmethod
    def disable():
        # Ideally we remove the line. For now, let's just comment it out is harder with simple replace.
        # We will just warn user or try to remove it. 
        # ConfigManager currently updates key=value. 
        # dtoverlay can appear multiple times, so ConfigManager might need a specific 'remove_line_starting_with'
        print("Disabling not fully implemented in this version (needs complex parsing).")
        print("Please edit /boot/config.txt manually to remove 'dtoverlay=gpio-fan' lines.")

    @staticmethod
    def apply_settings(pin, temp_c):
        global CONFIG_PATH
        temp_millicelsius = temp_c * 1000
        line = f"dtoverlay=gpio-fan,gpiopin={pin},temp={temp_millicelsius}"
        
        # We need to append this to the file.
        # But wait, if it already exists, we should replace it.
        # "dtoverlay=gpio-fan" might differ.
        # Simple approach: Check if "dtoverlay=gpio-fan" exists.
        
        print(f"Applying: {line} to {CONFIG_PATH}")
        if not os.path.exists(CONFIG_PATH):
             # For testing purposes on Windows, if not found, maybe create it locally?
             if os.name == 'nt': 
                 print(f"[{CONFIG_PATH}] not found. Creating local mock '{CONFIG_PATH}' for testing.")
                 # CONFIG_PATH is already set, just use it.
                 with open(CONFIG_PATH, "w") as f:
                     f.write(f"# Mock {CONFIG_PATH}\n")

        # Basic implementation: Append for now, or use sed-like replace if common.
        ConfigManager.append_if_not_exists(CONFIG_PATH, line)
