# USB Monitoring Tool - Using Python

Here’s a Python tool based on the algorithm, using tkinter for the GUI, psutil for monitoring processes, and basic USB detection methods. Since exact USB detection varies across platforms, this code provides the structure and an example implementation. You will need to install additional platform-specific libraries (like pyudev for Linux or pywinusb for Windows) if needed.

```python
import tkinter as tk
from tkinter import messagebox
import psutil
import time
import threading
import platform
import logging

# Cross-platform support: Linux, Windows, Mac
SYSTEM_PLATFORM = platform.system()

# Set up logging
logging.basicConfig(filename="usb_monitor.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

# Function to simulate USB monitoring
def monitor_usb_activity():
    usb_connected = False
    while running:
        # USB connection detection (this needs platform-specific libraries)
        if SYSTEM_PLATFORM == "Linux":
            # Example for Linux using psutil (use pyudev for real USB detection)
            devices = psutil.disk_partitions()
            for device in devices:
                if "media" in device.mountpoint and not usb_connected:
                    logging.info(f"USB Connected: {device.device}")
                    messagebox.showinfo("USB Alert", f"USB Device Connected: {device.device}")
                    usb_connected = True
                elif usb_connected and "media" not in device.mountpoint:
                    logging.info("USB Disconnected")
                    messagebox.showinfo("USB Alert", "USB Device Disconnected")
                    usb_connected = False
        elif SYSTEM_PLATFORM == "Windows":
            # Placeholder for Windows USB detection logic
            pass
        elif SYSTEM_PLATFORM == "Darwin":
            # Placeholder for Mac USB detection logic
            pass

        time.sleep(5)  # Check every 5 seconds

# Function to monitor suspicious activity
def monitor_suspicious_activity():
    while running:
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
            try:
                # Check for suspicious commands (e.g., keyloggers, etc.)
                if "keylogger" in proc.info['name'].lower():
                    logging.warning(f"Suspicious activity detected: {proc.info}")
                    messagebox.showwarning("Suspicious Activity", f"Keylogger detected: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        time.sleep(10)  # Check every 10 seconds

# Function to start the monitoring process
def start_monitoring():
    global running
    running = True
    logging.info("Monitoring started")
    start_button.config(state="disabled")
    stop_button.config(state="normal")

    # Start USB monitoring thread
    usb_thread = threading.Thread(target=monitor_usb_activity)
    usb_thread.start()

    # Start suspicious activity monitoring thread
    activity_thread = threading.Thread(target=monitor_suspicious_activity)
    activity_thread.start()

# Function to stop the monitoring process
def stop_monitoring():
    global running
    running = False
    logging.info("Monitoring stopped")
    messagebox.showinfo("USB Monitor", "Monitoring stopped")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

    # Exit the application after stopping
    root.quit()

# Set up GUI
root = tk.Tk()
root.title("USB Monitoring Tool")

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring, width=25)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring, width=25, state="disabled")
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=25)
exit_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
```
### Key Aspects:
- GUI: Uses tkinter to provide a simple interface with "Start Monitoring" and "Stop Monitoring" buttons.
- USB Detection: A placeholder for USB detection based on the platform (e.g., Linux, Windows, Mac).
- Suspicious Activity Monitoring: Monitors running processes for specific suspicious patterns, like keyloggers.
- Logging: Logs USB connection, disconnection, and suspicious activity to a file (usb_monitor.log).

### How to run:
1. Install required dependencies using pip:
      pip install psutil
   
   You may also need platform-specific libraries (pyudev, pywinusb).

2. Run the script:
      python usb_monitor.py
   

### Next Steps:
- Add platform-specific logic for USB detection.
- Expand the suspicious activity detection based on your criteria (like file transfers between USB and system).

This is a basic structure that should be expanded for complete functionality.
