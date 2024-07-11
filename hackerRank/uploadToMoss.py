import subprocess
import os
import re
import requests
from bs4 import BeautifulSoup

def submit_to_moss(file_paths, language="c"):
    # Create the base command
    moss_command = ["perl", "E:\projects\CodePlag\hackerRank\moss.pl", "-l", language]
    
    # Add each file to the command
    for path in file_paths:
        if not os.path.exists(path):
            print(f"File '{path}' does not exist.")
            return None
        moss_command.append(path)
    
    # Debug: Print the command
    print("Running command:", " ".join(moss_command))
    
    # Execute the command
    result = subprocess.run(moss_command, capture_output=True, text=True)

    if result.stderr:
        print("Error: ", result.stderr)
    return result.stdout

def extract_url(output):
    urls = re.findall(r'https?://\S+', output)  # This pattern matches http and https URLs
    if urls:
        print("Moss URL:", urls[0])
    else:
        print("No URL found in the output.")
    return urls[0] if urls else None  # Return the first URL found, or None if no URL is found

def get_similarity_percentage(files, language):
    output = submit_to_moss(files, language)
    if not output:
        print("Failed to submit to MOSS.")
        return None
    
    print("Output:", output)
    result_url = extract_url(output)
    if not result_url:
        print("No valid MOSS result URL found.")
        return None
    
    response = requests.get(result_url)
    if response.status_code != 200:
        print(f"Failed to fetch MOSS results. Status code: {response.status_code}")
        return None
    
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Example: Find all percentage similarities assuming they are in <a> tags 
    # You will need to adjust the selectors based on the actual HTML structure of the Moss results page
    anchor_tag_texts = [a.text for a in soup.find_all('a')]
    percentages = [match for item in anchor_tag_texts for match in re.findall(r'\d+%', item)]

    print(percentages)

    percent_values = [int(p.strip('%')) for p in percentages]
    print(percent_values)
    return percent_values[0] if percent_values else None

def update_userid_in_moss(perl_script_path, new_userid):
    # Read the original Perl script
    with open(perl_script_path, 'r') as file:
        content = file.readlines()
    
    # Modify the user ID in the script
    with open(perl_script_path, 'w') as file:
        for line in content:
            if '$userid' in line:
                # Regular expression to find the userid line and replace it
                line = re.sub(r'\$userid\s*=\s*\d+;', f'$userid = {new_userid};', line)
            file.write(line)

# Example usage
userid = 493505943
files = ['./py1.py', './py2.py']

#update_userid_in_moss("./moss.pl", userid)

# percentage = get_similarity_percentage(files, "python")

'''if percentage is not None:
    print(f"Similarity Percentage: {percentage}%")
else:
    print("Failed to calculate similarity percentage.")'''
