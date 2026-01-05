import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tool314.modules.overclock import Overclock
# We need to access CONFIG_PATH to check it. 
# It's imported in overclock from fan.
import tool314.modules.fan as fan_module

def test_overclock_medium():
    print("Testing Overclock Medium Preset...")
    
    # Ensure clean state or reuse
    current_config_path = fan_module.CONFIG_PATH
    print(f"Initial Config Path: {current_config_path}")
    
    # Apply Preset
    Overclock.apply_preset("medium")
    
    # Re-read path in case it changed
    final_path = fan_module.CONFIG_PATH
    print(f"Final Config Path: {final_path}")
    
    if os.path.exists(final_path):
        with open(final_path, "r") as f:
            content = f.read()
            print("Content:")
            print(content)
            if "arm_freq=1800" in content and "over_voltage=2" in content:
                print("SUCCESS: Overclock settings applied.")
            else:
                print("FAILURE: Settings mismatch.")
    else:
        print(f"FAILURE: {final_path} not found.")

if __name__ == "__main__":
    test_overclock_medium()
