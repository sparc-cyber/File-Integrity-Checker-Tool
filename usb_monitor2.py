import tkinter as tk
from tkinter import messagebox
import psutil
import time
import threading
import platform
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Cross-platform support: Linux, Windows, Mac
SYSTEM_PLATFORM = platform.system()

# Set up logging
logging.basicConfig(filename="usb_monitor.log", level=logging.INFO, 
                    format="%(asctime)s - %(message)s")

# Global variable to control the monitoring threads
running = False

# Function to simulate USB monitoring
def monitor_usb_activity():
    usb_connected = False
    usb_device_path = ""
    
    while running:
        if SYSTEM_PLATFORM == "Linux":
            devices = psutil.disk_partitions()
            for device in devices:
                if "media" in device.mountpoint and not usb_connected:
                    usb_device_path = device.mountpoint
                    logging.info(f"USB Connected: {device.device}")
                    messagebox.showinfo("USB Alert", f"USB Device Connected: {device.device}")
                    usb_connected = True
                    # Start file monitoring when USB is connected
                    start_file_monitoring(usb_device_path)
                elif usb_connected and "media" not in device.mountpoint:
                    logging.info("USB Disconnected")
                    messagebox.showinfo("USB Alert", "USB Device Disconnected")
                    usb_connected = False
                    # Stop file monitoring when USB is disconnected
                    stop_file_monitoring()
        elif SYSTEM_PLATFORM == "Windows":
            # Placeholder for Windows USB detection logic
            pass
        elif SYSTEM_PLATFORM == "Darwin":
            # Placeholder for Mac USB detection logic
            pass

        time.sleep(5)  # Check every 5 seconds

# File system event handler for logging file activities
class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            messagebox.showinfo("File Created", f"File created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
            messagebox.showinfo("File Deleted", f"File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            messagebox.showinfo("File Modified", f"File modified: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved: {event.src_path} to {event.dest_path}")
            messagebox.showinfo("File Moved", f"File moved: {event.src_path} to {event.dest_path}")

# Start file monitoring for USB device
def start_file_monitoring(usb_path):
    global observer
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, usb_path, recursive=True)
    observer.start()
    logging.info(f"Started monitoring file activities on {usb_path}")

# Stop file monitoring
def stop_file_monitoring():
    global observer
    if observer is not None:
        observer.stop()
        observer.join()
        logging.info("Stopped monitoring file activities")

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
