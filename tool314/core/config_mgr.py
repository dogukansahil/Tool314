import os
import shutil
import re

class ConfigManager:
    @staticmethod
    def backup_file(file_path):
        """Creates a backup of the given file."""
        if os.path.exists(file_path):
            backup_path = f"{file_path}.bak"
            shutil.copy2(file_path, backup_path)
            print(f"Backup created: {backup_path}")
            return True
        print(f"File not found: {file_path}")
        return False

    @staticmethod
    def read_file(file_path):
        """Reads content of a file."""
        if not os.path.exists(file_path):
            return None
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def update_key_value(file_path, key, value, separator='=', quote_value=False):
        """
        Updates a key-value pair in a file.
        If key exists, it updates it.
        If not, it appends it.
        """
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return False

        ConfigManager.backup_file(file_path)

        with open(file_path, 'r') as f:
            lines = f.readlines()

        key_pattern = re.compile(rf"^\s*{re.escape(key)}\s*{re.escape(separator)}")
        updated = False
        new_lines = []
        
        val_str = f'"{value}"' if quote_value else f"{value}"

        for line in lines:
            if key_pattern.match(line):
                new_lines.append(f"{key}{separator}{val_str}\n")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append(f"{key}{separator}{val_str}\n")

        try:
            with open(file_path, 'w') as f:
                f.writelines(new_lines)
            print(f"Updated {key} to {value} in {file_path}")
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
            
    @staticmethod
    def append_if_not_exists(file_path, line_content):
        """Appends a line if it doesn't already exist."""
        if not os.path.exists(file_path):
             print(f"File not found: {file_path}")
             return False
             
        ConfigManager.backup_file(file_path)
        
        with open(file_path, 'r') as f:
            lines = [l.strip() for l in f.readlines()]
            
        if line_content.strip() in lines:
            print(f"Config already exists: {line_content}")
            return True
            
        try:
            with open(file_path, 'a') as f:
                f.write(f"\n{line_content}\n")
            print(f"Appended: {line_content}")
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
