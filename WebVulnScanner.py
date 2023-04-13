import requests
from bs4 import BeautifulSoup

# Define the target URL
target_url = "https://www.hackthissite.org/"

# Send a GET request to the target URL and receive the response
response = requests.get(target_url)

# Parse the HTML code of the response
soup = BeautifulSoup(response.text, "html.parser")

# Find all input fields in the HTML code
input_fields = soup.find_all("input")

# Check for XSS vulnerabilities by injecting malicious JavaScript code
for input_field in input_fields:
    if input_field.has_attr("name"): # Check if the 'name' attribute exists
        payload = "<script>alert('test');</script>"
        input_field["value"] = payload
        # Resend the modified request and check if the code is executed
        modified_response = requests.get(target_url, params={input_field["name"]: input_field["value"]})
        if payload in modified_response.text:
            print(f"XSS vulnerability detected in {target_url}!")

# Check for SQL injection vulnerabilities by injecting SQL commands
for input_field in input_fields:
    if input_field.has_attr("name"): # Check if the 'name' attribute exists
        payload = "1'; SELECT * FROM users; --"
        input_field["value"] = payload
        # Resend the modified request and check if the command is executed
        modified_response = requests.get(target_url, params={input_field["name"]: input_field["value"]})
        if "error" in modified_response.text:
            print(f"SQL injection vulnerability detected in {target_url}!")

# Generate a report of the vulnerabilities detected
# TODO: implement report generation
