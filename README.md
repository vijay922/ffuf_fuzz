# ffuf_scan.py

## Overview

`ffuf_scan.py` is a Python script that automates the process of running the `ffuf` fuzzing tool against one or multiple URLs. The script dynamically handles repeated output lines in `ffuf` results by applying the `-fl` (filter by lines) option, restarting the scan when necessary, and saving results for each target in uniquely named files.

---

## Features

1. **Single URL Scanning**: Scans a single URL with `/FUZZ` appended to it.
2. **Batch URL Scanning**: Processes multiple URLs from a file, scanning each one sequentially.
3. **Dynamic Filtering (`-fl`)**:
   - Monitors `ffuf` output for repeated `Lines:` values.
   - **If a `Lines:` value appears more than 5 times**, the script:
     - Stops the current scan.
     - Adds the repeated `Lines:` value to the `-fl` filter.
     - Restarts the scan with the updated filter.
4. **Output Management**:
   - Results for each URL are saved in the `ffuf/` directory.
   - Output files are named based on the domain name of the URL (e.g., `ffuf/example.com.txt`).
5. **Error Handling**: Handles missing input files, invalid URLs, and process interruptions gracefully.

---

## Requirements

### Prerequisites

- **Python 3.7+**
- `ffuf` installed and available in your system's PATH
 `go install github.com/ffuf/ffuf/v2@latest`
- A wordlist file to use with `ffuf`.

---

## Usage

### Script Arguments

The script accepts the following arguments:

1. **`-u, --url`**  
   Specify a single URL to scan (e.g., `https://example.com`). The script automatically appends `/FUZZ` to the URL if not already included.

   Example:
   ```bash
   python3 ffuf_scan.py -u https://example.com

2. **-l, --list`**  
Specify a file containing a list of URLs (one per line). The script appends /FUZZ to each URL and scans them sequentially.

Example:
```bash
Copy code
python3 ffuf_scan.py -l urls.txt
```


### Dynamic Filtering Feature

- During each scan, the script monitors the `Lines:` values in the `ffuf` output.
- **If any `Lines:` value is repeated more than 5 times**, the following actions are taken:
  1. The current scan is **stopped**.
  2. The repeated `Lines:` value is **added to the `-fl` filter**.
  3. The scan is **restarted** with the updated `-fl` filter.
 
# If you want to run ffuf_proxy.py, First execute Below Tor commands

# Tor IP Changer Every 5 Seconds

This script allows you to change your Tor IP address every 5 seconds by restarting the Tor service using a simple bash loop.

## Prerequisites

- A Linux-based system
- `tor` installed on your machine
- Basic knowledge of terminal commands

## Installation

1. **Install Tor**:
   ```bash
   sudo apt install tor
   ```

   # Tor IP Rotator

A guide and script to configure Tor for changing your IP address every 5 seconds.

## Configuration

### 1. Add or Modify Tor Configuration
Edit the Tor configuration file:
```bash
sudo nano /etc/tor/torrc
```
# Tor Configuration and Usage

## Add or Modify the Following Lines
```
SocksPort 9050
SocksPolicy accept *
```
## Start Tor

To start the Tor service, run:

```bash
sudo service tor start
```

# Usage

## Test Tor IP Address
Use `curl` with the Tor proxy to confirm your public IP address:

```bash
curl --socks5-hostname localhost:9050 https://api.ipify.org
```

## Run IP Rotation Script

To rotate your IP address every 5 seconds, execute the following command:

```bash
while true; do pkill -HUP tor; sleep 5; done
```
