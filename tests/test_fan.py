import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tool314.modules.fan import FanControl

def test_fan_enable():
    print("Testing Fan Enable...")
    # Force mock path
    import tool314.modules.fan as fan_module
    fan_module.CONFIG_PATH = "config_test.txt"
    
    # Remove if exists
    if os.path.exists("config_test.txt"):
        os.remove("config_test.txt")
        
    FanControl.apply_settings(14, 80)
    
    if os.path.exists("config_test.txt"):
        with open("config_test.txt", "r") as f:
            content = f.read()
            print("Content:")
            print(content)
            if "dtoverlay=gpio-fan,gpiopin=14,temp=80000" in content:
                print("SUCCESS: Config updated correctly.")
            else:
                print("FAILURE: Config content mismatch.")
    else:
        print("FAILURE: Config file not created.")

if __name__ == "__main__":
    test_fan_enable()
