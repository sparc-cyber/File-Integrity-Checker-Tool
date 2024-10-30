Got it! We’ll adjust the logging to format integrity violations as structured blocks using your specified format. Here’s how the modified logging format will look in `integrity_log.txt`:

```plaintext
{
Integrity violation detected for <file_path>
Previous hash: <previous_hash>
New hash: <new_hash>
Timestamp: <timestamp>
}
```

And here’s the updated code to achieve this:

```python
import hashlib
import json
import os
import logging
from datetime import datetime

# Configurations
HASH_FILE = 'hashes.json'
HISTORY_FILE = 'history.json'
LOG_FILE = 'integrity_log.txt'

# Initialize logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(message)s')

def load_json(file_path):
    """Load JSON data from a file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
    except FileNotFoundError:
        logging.warning(f"File not found: {file_path}")
        return None
    return sha256.hexdigest()

def add_file_to_monitor():
    """Add a new file path to monitor."""
    file_path = input("Enter the full path of the file to monitor: ")
    if os.path.exists(file_path):
        hashes = load_json(HASH_FILE)
        current_hash = calculate_hash(file_path)
        if current_hash is None:
            return
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if file is already monitored
        for entry in hashes:
            if entry["file"] == file_path:
                print("This file is already being monitored.")
                return
        
        # Add the file with the hash and timestamp
        hashes.append({"file": file_path, "hash": current_hash, "timestamp": timestamp})
        save_json(hashes, HASH_FILE)
        print(f"File {file_path} has been added for monitoring.")
    else:
        print("File path is invalid or does not exist.")

def update_history(file_path, new_hash):
    """Update the history file with the last 5 hashes for a file."""
    history = load_json(HISTORY_FILE)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Find the history for the file or create it if it doesn't exist
    file_history = next((item for item in history if item["file"] == file_path), None)
    if file_history:
        file_history["hashes"].append({"hash": new_hash, "timestamp": timestamp})
        # Keep only the last 5 entries
        file_history["hashes"] = file_history["hashes"][-5:]
    else:
        # Create a new entry for the file
        history.append({"file": file_path, "hashes": [{"hash": new_hash, "timestamp": timestamp}]})

    save_json(history, HISTORY_FILE)

def log_integrity_violation(file_path, previous_hash, new_hash):
    """Log integrity violation details in a structured format."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = (
        f"{{\n"
        f"Integrity violation detected for {file_path}\n"
        f"Previous hash: {previous_hash}\n"
        f"New hash: {new_hash}\n"
        f"Timestamp: {timestamp}\n"
        f"}}\n"
    )
    logging.info(log_message)
    print(log_message)

def remove_file_from_monitor():
    """Remove a file from monitoring."""
    hashes = load_json(HASH_FILE)
    if not hashes:
        print("No files are currently being monitored.")
        return
    
    print("Files currently being monitored:")
    for idx, entry in enumerate(hashes, start=1):
        print(f"{idx}. {entry['file']}")
    
    try:
        choice = int(input("Enter the number of the file to remove: ")) - 1
        file_path = hashes[choice]["file"]
        hashes.pop(choice)
        save_json(hashes, HASH_FILE)
        print(f"File {file_path} has been removed from monitoring.")
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")

def check_integrity():
    """Check integrity of all monitored files and log any changes."""
    hashes = load_json(HASH_FILE)
    if not hashes:
        print("No files are currently being monitored.")
        return

    for entry in hashes:
        file_path = entry["file"]
        stored_hash = entry["hash"]
        current_hash = calculate_hash(file_path)
        if current_hash is None:
            continue  # Skip if the file is not found
        
        if stored_hash != current_hash:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Log the integrity violation in specified format
            log_integrity_violation(file_path, stored_hash, current_hash)

            # Update history and current hash with timestamp
            update_history(file_path, current_hash)
            entry["hash"] = current_hash
            entry["timestamp"] = timestamp
            save_json(hashes, HASH_FILE)
        else:
            print(f"File {file_path} is unchanged.")

def main():
    while True:
        print("\nFile Integrity Checker Menu:")
        print("1. Add a file to monitor")
        print("2. Remove a file from monitoring")
        print("3. Run integrity check")
        print("4. Quit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            add_file_to_monitor()
        elif choice == '2':
            remove_file_from_monitor()
        elif choice == '3':
            check_integrity()
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please choose between 1 and 4.")

# Run the program
if __name__ == "__main__":
    main()
```

### Summary of Changes
1. **Structured Integrity Violation Logging**:
   - Each integrity violation log entry in `integrity_log.txt` follows the specified format:
     ```plaintext
     {
     Integrity violation detected for /path/to/file
     Previous hash: <previous_hash>
     New hash: <new_hash>
     Timestamp: <timestamp>
     }
     ```

2. **Helper Function for Logging Violations**:
   - A new function `log_integrity_violation()` is created to handle the structured logging of integrity violations.

Let me know if this setup works for your requirements!
