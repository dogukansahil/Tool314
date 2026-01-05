import os
from tool314.core.menu import Menu
from tool314.core.config_mgr import ConfigManager

RESOLV_CONF_PATH = os.getenv("TOOL314_RESOLV_PATH", "/etc/resolv.conf")

class DnsConfig:
    @staticmethod
    def show_menu():
        menu = Menu("DNS Configuration")
        menu.add_option("Set Google DNS (8.8.8.8, 8.8.4.4)", lambda: DnsConfig.apply_dns(["8.8.8.8", "8.8.4.4"]))
        menu.add_option("Set Cloudflare DNS (1.1.1.1, 1.0.0.1)", lambda: DnsConfig.apply_dns(["1.1.1.1", "1.0.0.1"]))
        menu.add_option("Set OpenDNS (208.67.222.222, 208.67.220.220)", lambda: DnsConfig.apply_dns(["208.67.222.222", "208.67.220.220"]))
        menu.display()

    @staticmethod
    def apply_dns(servers):
        # We need to handle mock if on Windows
        global RESOLV_CONF_PATH
        if not os.path.exists(RESOLV_CONF_PATH) and os.name == 'nt':
             RESOLV_CONF_PATH = "resolv.conf"
             print(f"Mocking /etc/resolv.conf at {RESOLV_CONF_PATH}")
             if not os.path.exists(RESOLV_CONF_PATH):
                 with open(RESOLV_CONF_PATH, "w") as f:
                     f.write("# Mock resolv.conf\n")

        print(f"Setting DNS to {servers} in {RESOLV_CONF_PATH}")
        
        # Read file
        content = ConfigManager.read_file(RESOLV_CONF_PATH) or ""
        lines = content.splitlines()
        
        new_lines = []
        # Keep comments and non-nameserver lines?
        # Standard approach: Filter out existing nameservers and prepend new ones.
        
        for line in lines:
            if not line.strip().startswith("nameserver"):
                new_lines.append(line)
        
        # Add new nameservers at the top (after comments maybe?)
        # Let's just add them at the end of the preserved lines, ensuring they are active.
        # Actually resolv.conf reads top down.
        
        dns_lines = [f"nameserver {srv}" for srv in servers]
        
        # If file has comments at top, preserved lines might be header.
        # We will reconstruct: preserved + new
        
        final_lines = new_lines + dns_lines
        
        try:
            with open(RESOLV_CONF_PATH, "w") as f:
                f.write("\n".join(final_lines) + "\n")
            print("DNS updated successfully.")
        except Exception as e:
            print(f"Error writing DNS config: {e}")
