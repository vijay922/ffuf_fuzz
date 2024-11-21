# ffuf_fuzz
Overview ffuf_scan.py is a Python script that automates the process of running the ffuf fuzzing tool against one or multiple URLs. The script dynamically handles repeated output lines in ffuf results by applying the -fl (filter by lines) option, restarting the scan when necessary, and saving results for each target in uniquely named files.
