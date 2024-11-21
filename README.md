# ffuf_fuzz
Overview ffuf_scan.py is a Python script that automates the process of running the ffuf fuzzing tool against one or multiple URLs. The script dynamically handles repeated output lines in ffuf results by applying the -fl (filter by lines) option, restarting the scan when necessary, and saving results for each target in uniquely named files.


# Features
1. Single URL Scanning: Scans a single URL with /FUZZ appended to it.
2. Batch URL Scanning: Processes multiple URLs from a file, scanning each one sequentially.
3. Dynamic Filtering (-fl):

3.1 Monitors ffuf output for repeated Lines: values.
   
3.2 If a Lines: value appears more than 5 times, the script:

* Stops the current scan.
* Adds the repeated Lines: value to the -fl filter.
* Restarts the scan with the updated filter.
4. Output Management:
Results for each URL are saved in the ffuf/ directory.
Output files are named based on the domain name of the URL (e.g., ffuf/example.com.txt).
5. Error Handling: Handles missing input files, invalid URLs, and process interruptions gracefully.
