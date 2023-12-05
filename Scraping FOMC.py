'''
Scrape FOMC statement from March 2022 to March 2023
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import pandas as pd

# FOMC website
url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"

# Set up the Selenium WebDriver
chrome_driver_path = "C:/Users/user/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(url)

# Set up WebDriverWait
wait = WebDriverWait(driver, 10)

# Find the date range input fields and type checkboxes
from_date_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search from Date"]')
to_date_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search to Date"]')
monetary_policy_checkbox = driver.find_element(By.XPATH, '//label[text()="Monetary Policy"]/input')

# Clear default values
from_date_input.clear()
to_date_input.clear()

# Set the date range and check the Monetary Policy checkbox
from_date_input.send_keys("03/01/2022")
to_date_input.send_keys("03/31/2023")    
monetary_policy_checkbox.click()

# Submit the form (assuming there's a submit button)
submit_button = driver.find_element(By.CSS_SELECTOR, 'div.eventSearch__submit a')
submit_button.click()

# Scraping Method
def scrape_page_content(driver, url, data):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    angular_events_div = soup.find('div', class_='angularEvents Press_Release ng-scope')

    if angular_events_div:
        # Find all <div> tags with class "row ng-scope" within the "angularEvents" div
        item_divs = angular_events_div.find_all('div', class_='row ng-scope')

        # Iterate through each <div> tag and extract information
        for item_div in item_divs:
            # Extract date
            date = item_div.find('time', class_='itemDate').get_text(strip=True)

            # Extract title
            title_link = item_div.find('span', class_='itemTitle').find('a')
            title = title_link.get_text(strip=True)

            # Extract press type
            press_type = item_div.find('p', class_='eventlist__press').find('em').get_text(strip=True)

            # Extract link and make another HTTP request
            link = urljoin(url, title_link['href'])
            link_response = requests.get(link)
            if link_response.status_code == 200:
                link_soup = BeautifulSoup(link_response.text, 'html.parser')

                # Extract paragraph inside the link
                linked_paragraph = link_soup.find('div', id='article')  # Adjust if needed
                if linked_paragraph:
                    linked_content = linked_paragraph.get_text(strip=True)
                else:
                    linked_content = None

                # Append data to the list
                data.append({
                    "Date": date,
                    "Title": title,
                    "Press Type": press_type,
                    "Linked Content": linked_content
                })

    # Return the updated data
    return data


# Initialize an empty list to store the data
data = []

# Loop through three pages
while True:
    # Call the function to scrape the content of the current page
    data= scrape_page_content(driver, url, data)

    # Your existing code to navigate to the next page, e.g., clicking the "Next" button
    try:
        next_page_button = driver.find_element(By.XPATH, '//li[@ng-if="::directionLinks" and @class="pagination-next ng-scope"]/a')
        next_page_button.click()

        # Wait for the new content to be present
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'angularEvents')))
        wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'loading-spinner')))
    except NoSuchElementException:
        # No next page button found, exit the loop
        break

driver.quit()

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("scraped_fomc_data.xlsx", index=False)
