import json
import os
import sys
import requests

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

def process_merge_directory_results(directory_results):
    results = {}
    for file, filepaths in directory_results.items():
        for filepath in filepaths:
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    content = json.load(f)
                    results[filepath] = extract_vulnerabilities(content)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    return results

def process_directory_results(directory_results):
    results = {}
    for file, filepaths in directory_results.items():
        with open(filepaths, 'r', encoding='utf-8') as f:
            try:
                content = json.load(f)
                results[filepaths] = extract_vulnerabilities(content)
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


def analyze_total_cve_results(name, result, output):
    total_cves = 0

    for vulnerabilities in result.values():
        total_cves += len(vulnerabilities)

    output.write(f"Total number of CVEs in '{name}': '{total_cves}' \n\n")

def analyze_category_cve_results(name, result, output):
    # Analyze the severity of each vulnerability
    # NVD API base URL
    nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    # Initialize lists to store attack vectors and base severities
    attack_vectors = []
    base_severities = []

    for vulnerabilities in result.values():
        for cve in vulnerabilities:
            # Make API request to NVD API
            response = requests.get(f"{nvd_api}?cveId={cve}")
            if response.status_code == 200:
                cve_data = response.json()

                for vulnerability in cve_data['vulnerabilities']:
                    # Check if 'cve' key exists
                    if 'cve' in vulnerability:
                        cve_data = vulnerability['cve']
                        # Check if 'metrics' key exists
                        if 'metrics' in cve_data:
                            metrics_data = cve_data['metrics']
                            # Check if 'cvssMetricV31' key exists in 'metrics'
                            if 'cvssMetricV31' in metrics_data:
                                cvss_metrics = metrics_data['cvssMetricV31']
                                # Iterate through each entry in 'cvssMetricV31'
                                for cvss_metric in cvss_metrics:
                                    cvss_data = cvss_metric.get('cvssData')
                                    # Extract 'attackVector' and 'baseSeverity' from 'cvssData'
                                    if cvss_data:
                                        attack_vector = cvss_data.get('attackVector')
                                        base_severity = cvss_data.get('baseSeverity')
                                    # Append to respective lists if they exist
                                    if attack_vector:
                                        attack_vectors.append(attack_vector)
                                    if base_severity:
                                        base_severities.append(base_severity)

                                    print("checked " + cve)

                                    # Get unique attack vectors
                                    unique_attack_vectors = set(attack_vectors)

                                    # Count occurrences of each unique attack vector
                                    for attack_vector in unique_attack_vectors:
                                        count = attack_vectors.count(attack_vector)

                                    # Get unique attack vectors
                                    unique_base_severities = set(base_severities)

                                    # Count occurrences of each unique attack vector
                                    for base_severity in unique_base_severities:
                                        count = base_severities.count(base_severity)
            else:
                print(f"Failed to retrieve data for CVE {cve}")


    # Get unique attack vectors
    unique_attack_vectors = set(attack_vectors)

    # Count occurrences of each unique attack vector
    for attack_vector in unique_attack_vectors:
        count = attack_vectors.count(attack_vector)
        output.write(f"'{name}' '{attack_vector}': '{count}'\n")

    # Get unique attack vectors
    unique_base_severities = set(base_severities)

    # Count occurrences of each unique attack vector
    for base_severity in unique_base_severities:
        count = base_severities.count(base_severity)
        output.write(f"'{name}' '{base_severity}': '{count}'\n")

    output.write("========================================================================\n")

def merge_list(dic_a, dic_b):
    merged_dict = dic_a.copy()  # Create a copy of dir_a_results_free5gc to keep its original content

    for key, value in dic_b.items():
        if key in merged_dict:
            # If the key already exists in merged_dict, append the new value to a list
            if isinstance(merged_dict[key], list):
                merged_dict[key].append(value)
            else:
                merged_dict[key] = [merged_dict[key], value]
        else:
            # If the key doesn't exist in merged_dict, simply add it
            merged_dict[key] = value
    print(f"dir_a_results: '{dic_a}'")
    print(f"dir_b_results: '{dic_b}'")
    print(f"merged_dict: '{merged_dict}'")
    return merged_dict
def main():
    # Paths to the directories
    dir_a = 'clair-cve-result'
    dir_b = 'trivy-cve-result'

    # Specify prefixes to filter filenames
    prefixes = ['free5gc', 'open5gs']

    dir_a_results_free5gc = filter_files_starting_with(dir_a, prefixes[0])
    dir_b_results_free5gc = filter_files_starting_with(dir_b, prefixes[0])
    dir_a_results_open5gs = filter_files_starting_with(dir_a, prefixes[1])
    dir_b_results_open5gs = filter_files_starting_with(dir_b, prefixes[1])

    free5gc_merge = merge_list(dir_a_results_free5gc, dir_b_results_free5gc)
    open5gs_merge = merge_list(dir_a_results_open5gs, dir_b_results_open5gs)


    # Define the filename for the output file
    output_file = 'prototype_comparison_results_category.log'

    # Redirect standard output to a file
    with open(output_file, 'w') as f_out:
        # TODO: modify the input dictionary

        free5gc_result = process_merge_directory_results(free5gc_merge)
        open5gs_result = process_merge_directory_results(open5gs_merge)

        # Find each prototype implementation CVE number
        analyze_total_cve_results("free5GC", free5gc_result, f_out)
        analyze_total_cve_results("free5GC in Clair", process_directory_results(dir_a_results_free5gc), f_out)
        analyze_total_cve_results("free5GC in Trivy", process_directory_results(dir_b_results_free5gc), f_out)
        f_out.write("=================================================\n")

        analyze_total_cve_results("Open5GS", open5gs_result, f_out)
        analyze_total_cve_results("Open5GS in Clair", process_directory_results(dir_a_results_open5gs), f_out)
        analyze_total_cve_results("Open5GS in Trivy", process_directory_results(dir_b_results_open5gs), f_out)
        f_out.write("=================================================\n")


        # Analyze for the attack vector & severity
        analyze_category_cve_results("free5GC in Clair", process_directory_results(dir_a_results_free5gc), f_out)
        analyze_category_cve_results("free5GC in Trivy", process_directory_results(dir_b_results_free5gc), f_out)
        f_out.write("=================================================\n")
        analyze_category_cve_results("Open5GS in Clair", process_directory_results(dir_a_results_open5gs), f_out)
        analyze_category_cve_results("Open5GS in Trivy", process_directory_results(dir_b_results_open5gs), f_out)
        f_out.write("=================================================\n")

        # TODO: seperate these 3 analyzation
        # TODO: CWE categorize
        # analyze_category_cve_results("free5GC", free5gc_result, f_out)
        # analyze_category_cve_results("Open5GS", open5gs_result, f_out)
        #
        # f_out.write(f"free5GC detailed vulnerabilities: \n '{free5gc_result}'\n")
        # f_out.write("========================================================================\n")
        # f_out.write(f"Open5GS detailed vulnerabilities: \n '{open5gs_result}'\n")

if __name__ == "__main__":
    main()
