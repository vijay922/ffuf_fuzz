import subprocess
import re
from collections import Counter
import argparse
import os
from urllib.parse import urlparse, urljoin

# Set up argument parser
parser = argparse.ArgumentParser(description="Automate ffuf scans with dynamic -fl filtering for URLs.")
parser.add_argument(
    "-u", "--url", help="The target domain (e.g., https://example.com)"
)
parser.add_argument(
    "-l", "--list", help="File containing a list of URLs to scan (one URL per line)."
)
args = parser.parse_args()

# Validate input: either -u or -l must be provided
if not args.url and not args.list:
    parser.error("Either -u (URL) or -l (list of URLs) must be provided.")

# Prepare URLs to scan
urls = []
if args.url:
    urls.append(args.url.strip())  # Add single URL to list
if args.list:
    try:
        with open(args.list, "r") as file:
            urls.extend([line.strip() for line in file if line.strip()])  # Add URLs from file
    except FileNotFoundError:
        print(f"Error: File '{args.list}' not found.")
        exit(1)

# Output directory
output_dir = "ffuf"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

fl_values = set()  # To keep track of -fl values
repeat_threshold = 5  # Threshold for repetitions to stop and add -fl
pattern = re.compile(r"Lines: (\d+)")  # Regex to capture the Lines: field


def run_ffuf(command):
    """Runs ffuf with the given command and monitors the output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    line_counts = []  # To store 'Lines:' values
    count = Counter()

    try:
        for line in process.stdout:
            print(line.strip())  # Print ffuf output in real time

            # Capture 'Lines:' value
            match = pattern.search(line)
            if match:
                line_value = match.group(1)
                line_counts.append(line_value)

                # Update Counter and check for threshold
                count[line_value] += 1
                if count[line_value] > repeat_threshold:
                    print(f"Stopping scan: 'Lines: {line_value}' repeated more than {repeat_threshold} times.")
                    process.terminate()  # Stop the ffuf process
                    process.wait()
                    return line_value  # Return the repeated value
    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        print("Scan interrupted by user.")
        return None
    except Exception as e:
        process.terminate()
        process.wait()
        print(f"An error occurred: {e}")
        return None

    process.wait()
    return None


# Iterate through each URL in the list
for url in urls:
    # Ensure FUZZ is appended to the URL
    if not url.endswith("/"):
        url += "/"
    url_with_fuzz = urljoin(url, "FUZZ")

    # Extract domain name from the URL for output file naming
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc  # e.g., example.com
    output_file = os.path.join(output_dir, f"{domain_name}.txt")

    # Initial ffuf command
    base_command = [
        "ffuf",
        "-u", url_with_fuzz,
        "-w", "wordlist.txt",
        "-mc", "200,204,301,307,302,401,403,405",
        "-t", "400",
        "-ac",
        "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
        "-H", "Accept: */*",
        "-of", "md",  # Output format markdown
        "-o", output_file,  # Output file path
    ]

    fl_values.clear()  # Clear -fl values for each new URL

    print(f"\nStarting ffuf scan for: {url_with_fuzz}")
    while True:
        # Add the updated -fl options to the command
        if fl_values:
            fl_option = ",".join(map(str, sorted(fl_values)))
            current_command = base_command + ["-fl", fl_option]
        else:
            current_command = base_command

        # Run ffuf and capture repeated Lines: value
        repeated_value = run_ffuf(current_command)

        if repeated_value:
            # Add the repeated Lines: value to -fl and restart
            fl_values.add(int(repeated_value))
            print(f"Adding -fl {repeated_value} and restarting the scan...")
        else:
            print(f"Scan completed for {url}. Output saved to {output_file}")
            break
