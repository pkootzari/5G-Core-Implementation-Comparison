import json
import os
import sys

# Paths to the directories
dir_a = 'clair-cve-result'
dir_b = 'trivy-cve-result'

def load_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

# Compare each image's CVE report 
def compare_vulnerabilities(file_a, file_b, output_file):
    data_a = load_json_file(file_a)
    data_b = load_json_file(file_b)
    
    # Extract vulnerabilities from data_a
    vuln_a = extract_vulnerabilities(data_a)

    # Extract vulnerabilities from data_b
    vuln_b = extract_vulnerabilities(data_b)

    # Convert the vulnerability lists to sets for easy comparison
    set_vuln_a = set(vuln_a)
    set_vuln_b = set(vuln_b)

    # Find the common vulnerabilities
    common_vulnerabilities = set_vuln_a.intersection(set_vuln_b)

    # Count the number of vulnerabilities in each list
    num_vuln_a = len(vuln_a)
    num_vuln_b = len(vuln_b)

    # Count the number of shared vulnerabilities
    num_shared_vulnerabilities = len(common_vulnerabilities)

    # Count the number of different vulnerabilities
    num_different_vulnerabilities = len(set_vuln_a.symmetric_difference(set_vuln_b))

    output_file.write(f"File '{os.path.basename(file_a)}' has {num_vuln_a} vulnerabilities.\n")
    output_file.write(f"File '{os.path.basename(file_b)}' has {num_vuln_b} vulnerabilities.\n\n")

    output_file.write(f"{num_shared_vulnerabilities} vulnerabilities are shared between the two files.\n")
    output_file.write(f"{num_different_vulnerabilities} vulnerabilities are different between the two files.\n\n")

    if common_vulnerabilities:
        output_file.write(f"Files '{os.path.basename(file_a)}' and '{os.path.basename(file_b)}' share the following vulnerabilities:\n")
        output_file.write(", ".join(common_vulnerabilities) + "\n\n")

    if num_different_vulnerabilities > 0:  # Only print different vulnerabilities if there are any
        output_file.write(f"Files '{os.path.basename(file_a)}' and '{os.path.basename(file_b)}' have different vulnerabilities:\n\n")
        output_file.write(f"Vulnerability in '{os.path.basename(file_a)}' that is not in '{os.path.basename(file_b)}':\n")
        if set_vuln_a.difference(set_vuln_b):
            output_file.write(", ".join(set_vuln_a.difference(set_vuln_b)) + "\n")
        else:
            output_file.write("None\n")
        output_file.write("\n")
        output_file.write(f"Vulnerability in '{os.path.basename(file_b)}' that is not in '{os.path.basename(file_a)}':\n")
        if set_vuln_b.difference(set_vuln_a):
            output_file.write(", ".join(set_vuln_b.difference(set_vuln_a)) + "\n")
        else:
            output_file.write("None\n")
    
    output_file.write("=====================================================================")


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

def main():
    # List json files in both directories
    files_in_a = [os.path.join(dir_a, f) for f in os.listdir(dir_a) if f.endswith('.json')]
    files_in_b = [os.path.join(dir_b, f) for f in os.listdir(dir_b) if f.endswith('.json')]

    # Define the filename for the output file
    output_file = 'image_comparison_results.log'

    # Redirect standard output to a file
    with open(output_file, 'w') as f_out:

        f_out.write("Comparing each image's vulnerabilities between clair and trivy:\n")

        # Assuming the same filenames exist in both directories
        for file_a in files_in_a:
            file_basename = os.path.basename(file_a)
            file_b = os.path.join(dir_b, file_basename)
            
            if file_b in files_in_b:
                compare_vulnerabilities(file_a, file_b, f_out)
            else:
                f_out.write(f"No matching file found in Directory B for {file_basename}\n")

        print("Log printed: image_comparison_results.log")

    # Close the output file
    sys.stdout.close()

    # Reset stdout to the default console output
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    main()
