############# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import os

# Cambiar producto y url según corresponda
product = "carnes"
url = "https://www.lider.cl/supermercado/category/Carnes_y_Pescados/Todas_las_Carnes/Carnes_Premium"

############# Functions
def items_to_csv(items):
    # Process the items as needed
    for item in items:
        item_description = item.find('div', class_="product-card_description-wrapper")
        item_description_data = item_description.find_all('span')
        item_marca = item_description_data[0].text
        item_name = item_description_data[1].text.strip()
        item_price = item.find('div', class_="product-card__sale-price").text

        # to csv
        with open(csv_filename, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([item_marca, item_name, item_price])

############# Main

# Set the directory
directory = 'csv_files'
# Create the directory
os.makedirs(directory, exist_ok=True)

# Set the filename
csv_filename = os.path.join(directory, f'lider-{product}.csv')

# Create Csv File
with open(csv_filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Marca", "Nombre", "Precio Oferta"])

# Configure Selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

# Set initial page and max hits per page
url = f"{url}?page=1&hitsPerPage=100"

# Open the page in Selenium
driver.get(url)

# Wait for the page to fully render
time.sleep(3)

# Extract the page source
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Get all pages for pagination
pages = soup.find_all("li", class_="ais-Pagination-item--page")
total_pages = int(pages[-1].text)

# Append first items
items = soup.find_all("li", class_="ais-Hits-item")
items_to_csv(items)

print(f"Scraping page 1 of {total_pages}...")

if total_pages > 1:
# Loop through all pages
    for page in range(2, total_pages + 1):
        try:
            # Find the next page button
            next_page = driver.find_element_by_css_selector("li.ais-Pagination-item--nextPage")
            next_page_a = next_page.find_element_by_tag_name("a")
            # Click the next page button
            next_page_a.click()
            # Wait for the page to fully render
            time.sleep(3)
            # Update the soup
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            print(f"Scraping page {page} of {total_pages}...")
            # Find all <li> elements with class "ais-Hits-item"
            items = soup.find_all("li", class_="ais-Hits-item")
            items_to_csv(items)
        except:
            print("Scraping terminated before reaching target page.")
            break

# Close the browser
driver.quit()

print("Done!")