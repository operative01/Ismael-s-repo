from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
 
# Initialize ChromeDriver with WebDriver Manager
options = Options()
options.headless = False  # Run in headless mode, change to False if you want to see the browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
 
# URL to scrape
url = "https://www.circulaire-bouwmaterialen.nl/artikel/24644/gebruikte-vuren-plank-12x95x2950mm-partij.html"
 
# Open the webpage
driver.get(url)
content = driver.page_source
 
# Use BeautifulSoup to parse the page content
soup = BeautifulSoup(content, 'html.parser')
 
# Extract metadata
meta_data = []
meta_tags = soup.find_all('meta')
for tag in meta_tags:
    name = tag.get('name') or tag.get('property')
    content = tag.get('content')
    if name and content:
        meta_data.append({'Name': name, 'Content': content})
 
# Extract additional information
title = soup.find('title').text.strip() if soup.find('title') else 'No title found'
description = soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else 'No description found'
price = soup.find('span', {'class': 'price'}).text if soup.find('span', {'class': 'price'}) else 'No price found'
 
# Extract specific product details
product_details = {}
details_section = soup.find('div', {'class': 'product attribute description'})
if details_section:
    product_details_text = details_section.get_text(separator=" ").strip()
    product_details = {
        "description": product_details_text
    }
 
# Extract table data
table_data = []
specs_section = soup.find('table', {'class': 'data table additional-attributes'})
if specs_section:
    rows = specs_section.find_all('tr')
    for row in rows:
        cells = row.find_all(['th', 'td'])
        if len(cells) == 2:  # Assuming each row has two columns
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            table_data.append({'Spec': key, 'Value': value})
 
# Close the WebDriver
driver.quit()
 
# Print extracted data
print(f"Title: {title}")
print(f"Description: {description}")
print(f"Price: {price}")
print(f"Product Details: {product_details}")
 
# Print table data
for item in table_data:
    print(f"{item['Spec']}: {item['Value']}")
 
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['product_database']  # Create or connect to the 'product_database'
collection = db['circulaire']  # Create or connect to the 'gebruikte_bouwmaterialen' collection
 
# Create a document to insert
document = {
    'Title': title,
    'Description': description,
    'Price': price,
    'Product Details': product_details,
    'Specs': table_data
}
 
# Insert the document into the collection
collection.insert_one(document)
 
print("Data inserted into MongoDB successfully.")