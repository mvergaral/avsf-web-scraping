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
url = "https://descorcha.com/vinos-21"

############# Functions
def items_to_csv(items):
    # Process the items as needed
    for item in items:
        item_marca = item.find('h2', class_="product-title").text
        item_type = item.find('h3', class_="product-type").text
        item_class = item.find('h3', class_="product-class").text
        item_name = f"{item_type} {item_class}"
        item_price = item.find('span', class_="descorcha_combo_sale_price")
        if item_price is not None:
            item_price = item_price.text.replace('$', '').replace('.', '')
        else:
            item_price = "Agotado"

        # to csv
        with open(csv_filename, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([item_marca, item_name, item_price])

# Set the directory
directory = 'csv_files'
# Create the directory
os.makedirs(directory, exist_ok=True)
# Set the filename
csv_filename = os.path.join(directory, f'descorcha-{product}.csv')

# Create Csv File
with open(csv_filename, 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Marca", "Nombre", "Precio"])

# Configure Selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

driver.get(url)

timeout = 10

# Wait until the page is fully loaded
wait = WebDriverWait(driver, timeout)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


# Extract the page source
page_source = driver.page_source

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

modal_button = driver.find_element_by_xpath('//*[@id="btnUpdateState"]')
modal_button.click()

running = True
page = 1

while running:
    # Extract the items
    items = soup.find_all('div', class_="product-description")
    # Process the items
    items_to_csv(items)
    # Go to the next page
    # try:
    print(f"Scraping page  {page}")
    try:
        next_page_button = WebDriverWait(driver, 2).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.next'))
                            )
        next_page_button.click()
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    except:
        stop = False
        break
    # Extract the page source
    page_source = driver.page_source
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    page += 1

driver.quit()

print("Done!")
