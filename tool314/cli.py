from tool314.core.menu import Menu
from tool314.modules.fan import FanControl
from tool314.modules.overclock import Overclock
from tool314.modules.dns import DnsConfig
from tool314.modules.sys_info import SystemInfo

def main():
    menu = Menu("Tool314 - Raspberry Pi Utility")
    
    def fan_control():
        FanControl.show_menu()
    
    def overclock():
        Overclock.show_menu()
        
    def dns_config():
        DnsConfig.show_menu()
        
    def system_tweaks():
        SystemInfo.show_menu()

    menu.add_option("Fan Control", fan_control)
    menu.add_option("Overclocking", overclock)
    menu.add_option("DNS Configuration", dns_config)
    menu.add_option("System Tweaks", system_tweaks)
    
    menu.display()

if __name__ == "__main__":
    main()
