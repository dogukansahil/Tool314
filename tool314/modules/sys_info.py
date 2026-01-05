import os
import subprocess
from tool314.core.menu import Menu

class SystemInfo:
    @staticmethod
    def show_menu():
        menu = Menu("System Info & Tweaks")
        menu.add_option("Show Temperature", SystemInfo.show_temp)
        menu.add_option("Show Uptime", SystemInfo.show_uptime)
        menu.add_option("Update Packages (apt update & upgrade)", SystemInfo.update_system)
        menu.display()

    @staticmethod
    def show_temp():
        try:
            # vcgencmd measure_temp is standard on Pi
            res = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8").strip()
            print(f"\nCPU Temperature: {res}")
        except:
             # Fallback for non-Pi or error
             print("\nCould not read temperature. (Is this a Raspberry Pi?)")

    @staticmethod
    def show_uptime():
        try:
            res = subprocess.check_output(["uptime", "-p"]).decode("utf-8").strip()
            print(f"\nUptime: {res}")
        except:
             print("\nCould not read uptime.")

    @staticmethod
    def update_system():
        print("\nRunning 'sudo apt update && sudo apt upgrade -y'...")
        # In real scenario:
        # os.system("sudo apt update && sudo apt upgrade -y")
        print("Update command skipped (simulation mode).")
