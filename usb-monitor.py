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
