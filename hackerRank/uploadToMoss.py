import subprocess
import os
import re 
import requests
from bs4 import BeautifulSoup

def submit_to_moss(file_paths, language="c"):
    # Create the base command
    moss_command = f"perl moss.pl -l {language} "
    
    # Add each file to the command
    for path in file_paths:
        moss_command += f" '{path}'"
    
    # Execute the command
    result = subprocess.run(moss_command, shell=True, capture_output=True, text=True)

    if result.stderr :
        print("Error: ",result.stderr)
    return result.stdout



def extract_url(output):
    urls = re.findall(r'https?://\S+', output)  # This pattern matches http and https URLs
    if urls:
        print("Moss URL:", urls[0])
    else:
        print("No URL found in the output.")
    return urls[0] if urls else None  # Return the first URL found, or None if no URL is found


def get_similarity_percentage(files,language) :
  output = submit_to_moss(files, "cc")
  print("Output:", output)

  result_url = extract_url(output)
  response = requests.get(result_url)
  html_content = response.text

  soup = BeautifulSoup(html_content, 'html.parser')

  # Example: Find all percentage similarities assuming they are in <a> tags 
  # You will need to adjust the selectors based on the actual HTML structure of the Moss results page
  anchor_tag_texts = [a.text for a in soup.find_all('a')]
  percentages = [match for item in anchor_tag_texts for match in re.findall(r'\d+%', item)]


  print(percentages)


  percent_values = [int(p.strip('%')) for p in percentages]
  print(percent_values)
  return percent_values[0]


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
files = ['me1.cpp', 'me2.cpp']

update_userid_in_moss("./moss.pl",userid)

percentage = get_similarity_percentage(files,"cc")

print(percentage)




