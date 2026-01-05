import os

class Menu:
    def __init__(self, title="Tool314", info_text=None):
        self.title = title
        self.options = []
        self.info_text = info_text  # Can be a string or a callable

    def add_option(self, label, callback):
        self.options.append({'label': label, 'callback': callback})

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display(self):
        while True:
            self.clear_screen()
            print(f"=== {self.title} ===")
            print("-" * len(f"=== {self.title} ==="))
            
            # Display info/status if provided
            if self.info_text:
                if callable(self.info_text):
                    print(self.info_text())
                else:
                    print(self.info_text)
                print("-" * len(f"=== {self.title} ==="))
            
            for index, option in enumerate(self.options, start=1):
                print(f"{index}. {option['label']}")
            
            print("0. Exit")
            print()
            
            choice = input("Select an option: ").strip()

            if choice == '0':
                print("Exiting...")
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(self.options):
                    # Execute callback
                    self.options[idx]['callback']()
                    input("\nPress Enter to continue...")  # Pause after execution
                else:
                    input("Invalid option. Press Enter to try again.")
            except ValueError:
                input("Invalid input. Please enter a number. Press Enter to try again.")
