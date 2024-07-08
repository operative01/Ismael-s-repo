import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Initialize ChromeDriver with WebDriver Manager
options = Options()
options.headless = True  # Run in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL of the JavaScript file
js_url = "https://marktplaats.insert.nl/_nuxt/8a58809.js"

# Fetch the JavaScript file content
response = requests.get(js_url)

# Check if the request was successful
if response.status_code == 200:
    content = response.text

    # Save the JavaScript content to a local file
    with open('javascript.js', 'w', encoding='utf-8') as file:
        file.write(content)

    # Extract key-value pairs (this pattern might need adjustment based on the actual content)
    key_value_pairs = re.findall(r'(\w+)\s*:\s*("[^"]*"|\d+|true|false|null)', content)

    # Create a DataFrame to store the extracted data
    kvp_df = pd.DataFrame(key_value_pairs, columns=['Key', 'Value'])

    # Save the DataFrame to a CSV file
    kvp_df.to_csv('extracted_key_value_pairs.csv', index=False)

    print("JavaScript file content saved to 'javascript.js'.")
    print("Extracted key-value pairs saved to 'extracted_key_value_pairs.csv'.")
else:
    print(f"Failed to retrieve the JavaScript file. Status code: {response.status_code}")

# Close the WebDriver
driver.quit()
