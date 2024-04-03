import json
import os
import sys

def extract_vulnerabilities(data):
    # Check if "Results" key exists for data_b(trivy)
    if "Results" in data:
        # If "Results" is a list, extract vulnerabilities from each result
        if isinstance(data["Results"], list):
            vuln_list = []
            for result in data["Results"]:
                 if "Vulnerabilities" in result:
                    for vulnerability in result["Vulnerabilities"]:
                            if "VulnerabilityID" in vulnerability:
                                vuln_list.append(vulnerability["VulnerabilityID"])
            return vuln_list
        # If "Results" is a dictionary, extract vulnerabilities directly
        elif isinstance(data["Results"], dict) and "Vulnerabilities" in data["Results"]:
            return data["Results"]["Vulnerabilities"]
    
    # Check data_a(clair)
    elif "vulnerabilities" in data:
        if isinstance(data["vulnerabilities"], list):
             # If "vulnerabilities" is a list, extract vulnerability strings from each dictionary
            vuln_list = []
            for vulnerability_data in data["vulnerabilities"]:
                if "vulnerability" in vulnerability_data:
                    vuln_list.append(vulnerability_data["vulnerability"])
            return vuln_list
        elif isinstance(data["vulnerabilities"], dict) and "vulnerability" in data["vulnerabilities"]:
        # If "vulnerabilities" is a dictionary, directly extract the vulnerability string
            return [data["vulnerabilities"]["vulnerability"]]
   
    return []

def process_directory_results(directory_results):
    results = {}
    for file, filepath in directory_results.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                content = json.load(f)
                results[file] = extract_vulnerabilities(content)
            except Exception as e:
                print(f"Error reading {file}: {e}")
    return results

# Function to filter files with filenames starting with 'free5gc' or 'open5gs'
def filter_files_starting_with(directory, prefixes):
    filtered_files = {}
    for filename in os.listdir(directory):
        for prefix in prefixes:
            if filename.startswith(prefix):
                filepath = os.path.join(directory, filename)
                filtered_files[filename] = filepath
                break  # Stop searching for prefixes once a match is found
    return filtered_files

def main():
    # Paths to the directories
    dir_a = 'clair-cve-result'
    dir_b = 'trivy-cve-result'

    # Specify prefixes to filter filenames
    prefixes = ['free5gc', 'open5gs']

    dir_a_results = filter_files_starting_with(dir_a, prefixes[0])
    dir_b_results = filter_files_starting_with(dir_b, prefixes[1])

    # Define the filename for the output file
    output_file = 'prototype_comparison_results.log'

    # Redirect standard output to a file
    with open(output_file, 'w') as f_out:

        free5gc_result = process_directory_results(dir_a_results)
        open5gs_result = process_directory_results(dir_b_results)

        f_out.write(f"free5gc vulnerabilities: \n '{free5gc_result}'\n")
        f_out.write("========================================================================\n")
        f_out.write(f"open5gs vulnerabilities: \n '{open5gs_result}'\n")


if __name__ == "__main__":
    main()
