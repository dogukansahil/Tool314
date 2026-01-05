import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tool314.modules.dns as dns_module
from tool314.modules.dns import DnsConfig

def test_dns_google():
    print("Testing DNS Set Google...")
    
    # Ensure current path usage
    current_resolv_path = dns_module.RESOLV_CONF_PATH
    print(f"Initial Resolv Path: {current_resolv_path}")
    
    # Force delete info if we want clean state, but DnsConfig creates it if missing (on NT)
    if os.path.exists(current_resolv_path) and "resolv.conf" in current_resolv_path:
        # Only delete if it's our mock
        try:
            os.remove(current_resolv_path)
        except:
            pass
            
    # Apply DNS
    DnsConfig.apply_dns(["8.8.8.8", "8.8.4.4"])
    
    # Re-read path in case it changed (it shouldn't if we don't start it out as non-existent dir)
    # But logic in dns.py is: if not exists, set to resolv.conf.
    
    final_path = dns_module.RESOLV_CONF_PATH
    print(f"Final Resolv Path: {final_path}")
    
    if os.path.exists(final_path):
        with open(final_path, "r") as f:
            content = f.read()
            print("Content:")
            print(content)
            if "nameserver 8.8.8.8" in content and "nameserver 8.8.4.4" in content:
                print("SUCCESS: Google DNS applied.")
            else:
                print("FAILURE: Settings mismatch.")
    else:
        print(f"FAILURE: {final_path} not found.")

if __name__ == "__main__":
    test_dns_google()
