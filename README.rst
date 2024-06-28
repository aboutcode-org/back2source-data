back2source-data
================

Checking if package sources and binaries match

Instructions to run:
====================

1. Clone the repository using git clone  https://github.com/aboutcode-org/back2source-data

2. Install beautifulsoup4 using pip install beautifulsoup4

3. Run the script using python3 etc/scripts/get_fedora_urls.py

4. It will generate a file named pairs.csv

5. Install purldb https://github.com/nexB/purldb

6. Setup purldb using purldb Instructions

7. activate venv and run etc/scripts/run_d2d.py

8. It will generate a file named d2d-summary.csv
