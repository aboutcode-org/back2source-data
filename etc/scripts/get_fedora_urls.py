import requests
from bs4 import BeautifulSoup
import csv

# The base URL to scrape
base_url = "https://archive.fedoraproject.org/pub/fedora/linux/releases/40/Everything/x86_64/debug/tree/Packages/"

# Function to scrape the URL and extract pairs
def scrape_and_extract_pairs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all directories
    dirs = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('/') and a['href'] != '../']
    
    pairs = []
    for dir in dirs:
        dir_url = url + dir
        dir_response = requests.get(dir_url)
        dir_soup = BeautifulSoup(dir_response.content, 'html.parser')
        
        # Extract all .rpm files
        rpm_files = [a['href'] for a in dir_soup.find_all('a', href=True) if a['href'].endswith('.rpm')]
        # Create dictionaries to hold debuginfo and debugsource files
        debuginfo_files = {}
        debugsource_files = {}
        
        for file in rpm_files:
            if '-debuginfo-' in file:
                package_name = file.split('-debuginfo-')[0]
                debuginfo_files[package_name] = file
            elif '-debugsource-' in file:
                package_name = file.split('-debugsource-')[0]
                debugsource_files[package_name] = file
        
        # Find pairs based on the package name
        for package_name in set(debuginfo_files.keys()).union(set(debugsource_files.keys())):
            debuginfo_file = debuginfo_files.get(package_name)
            debugsource_file = debugsource_files.get(package_name)
            if debuginfo_file and debugsource_file:
                pairs.append((dir_url + debuginfo_file, dir_url + debugsource_file))
                if len(pairs) >=1000:
                    return pairs

    return pairs


def generate_csv():
    # Get pairs
    pairs = scrape_and_extract_pairs(base_url)

    # Write pairs to a CSV file
    with open('pairs.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for debuginfo, debugsource in pairs:
            print(debuginfo, debugsource)
            csvwriter.writerow([debuginfo, debugsource])

generate_csv()
