import os
from tool314.core.menu import Menu
import tool314.modules.fan as fan_module
from tool314.core.config_mgr import ConfigManager

class Overclock:
    @staticmethod
    def show_menu():
        menu = Menu("Overclocking Settings", info_text=Overclock.get_status)
        print("\nWARNING: Overclocking may void your warranty and cause instability.")
        
        menu.add_option("Set Medium Overclock (arm_freq=1800)", lambda: Overclock.apply_preset("medium"))
        menu.add_option("Set High Overclock (arm_freq=2000)", lambda: Overclock.apply_preset("high"))
        menu.add_option("Remove Overclock (Stock)", lambda: Overclock.apply_preset("none"))
        menu.display()

    @staticmethod
    def get_status():
        config_path = fan_module.CONFIG_PATH
        if not os.path.exists(config_path):
            return "Current Status: Unknown (Config file not found)"
        
        try:
            with open(config_path, "r") as f:
                content = f.read()
            
            if "arm_freq" in content:
                import re
                freq = re.search(r"arm_freq=(\d+)", content)
                volt = re.search(r"over_voltage=(\d+)", content)
                
                f_val = freq.group(1) if freq else "?"
                v_val = volt.group(1) if volt else "?"
                
                return f"Current Status: Overclocked (Freq: {f_val}, Voltage: {v_val})"
            else:
                return "Current Status: Stock (No overrides found)"
        except Exception:
            return "Current Status: Error reading config"

    @staticmethod
    def apply_preset(preset):
        config_path = fan_module.CONFIG_PATH
        
        # We need to make sure file exists mechanism is consistent.
        if not os.path.exists(config_path) and os.name == 'nt':
             try:
                 with open(config_path, "w") as f:
                     f.write(f"# Mock {config_path}\n")
             except FileNotFoundError:
                 # Fallback if directory doesn't exist (like /boot on windows)
                 print(f"Cannot create {config_path}. Using local 'config.txt' instead.")
                 fan_module.CONFIG_PATH = "config.txt"
                 config_path = fan_module.CONFIG_PATH
                 with open(config_path, "w") as f:
                     f.write(f"# Mock {config_path}\n")

        print(f"Applying preset: {preset}")
        
        settings = {}
        if preset == "medium":
            settings = {
                "arm_freq": "1800",
                "over_voltage": "2"
            }
        elif preset == "high":
            settings = {
                "arm_freq": "2000",
                "over_voltage": "6"
            }
        elif preset == "none":
            # For "none", we should ideally remove lines. 
            print("Resetting to stock not fully implemented (requires removing lines).")
            print("Please manually edit config.txt to remove arm_freq/over_voltage.")
            return

        for key, val in settings.items():
            ConfigManager.update_key_value(config_path, key, val)
        
        print("For changes to take effect, you must reboot.")
