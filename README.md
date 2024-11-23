# File Integrity Monitoring Tool
This tool monitors file integrity by checking the hashes of specified files at regular intervals to detect unauthorized modifications. It provides two main functionalities:

### File Manager (file.py):
- Add Files: Register files for integrity monitoring.
- Save Current Hash: Save the current state of a file's hash to the database.
- Remove Files: Unregister files from monitoring.
- Each file entry in the database includes the file's path, timestamp, and hash history.
&nbsp;
### Integrity Checker (int.py):
- Runs in a continuous monitoring loop, comparing the current hash of each monitored file to the last known hash in the database every 30 seconds.
&nbsp;


