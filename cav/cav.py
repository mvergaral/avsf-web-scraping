############# Imports
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cambiar producto y url según corresponda
product = "vinos"
url = "https://cav.cl/tienda?q=&hPP=20&idx=products&p=0&fR%5Bfamily.name%5D%5B0%5D=Vinos&is_v=1"

############# Functions
def items_to_csv(items):
    # Process the items as needed
    for item in items:
        item_description_data = item.find('article', class_="c-product--item")
        item_marca = item_description_data['data-brand']
        item_name = item_description_data['data-name']
        item_price = item_description_data['data-price']
        item_member_price = item_description_data.find('p', class_='o-text--primary').text.split()[1].replace('$', '').replace('.', '')

        # to csv
        with open(csv_filename, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([item_marca, item_name, item_price, item_member_price])

# Set the directory
directory = 'csv_files'
# Create the directory
os.makedirs(directory, exist_ok=True)
# Set the filename
csv_filename = os.path.join(directory, f'cav-{product}.csv')

# Create Csv File
with open(csv_filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Marca", "Nombre", "Precio", "Precio Socio"])

# Configure Selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)


driver.get(url)
time.sleep(2)

# Extract the page source
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

stop = True
page = 1

# Close Age modal
age_modal_yes_button = driver.find_element_by_css_selector("button.getIn")
try:
    age_modal_yes_button.click()
except:
    pass

# Loop through pages
while stop:
    # Get the items
    items = soup.find_all("div", class_="ais-hits--item")

    print(f"Scraping page {page}")
    items_to_csv(items)

    try:
        next_page_button = WebDriverWait(driver, 2).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'li.ais-pagination--item__next > a'))
                            )
    except:
        stop = False
        break

    #if next_page_button also have this class ais-pagination--item__disabled then stop
    if 'ais-pagination--item__disabled' in next_page_button.get_attribute('class'):
        stop = False
    else:
        if next_page_button is not None:
            next_page_button.click()
            time.sleep(2)

            # Extract the page source
            page_source = driver.page_source

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")

            page += 1

# Close the driver
driver.quit()

print("Done!")

