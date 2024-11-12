import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options for headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL and download directory
base_url = "https://jdih.kkp.go.id/Homedev/PeraturanAll"
download_directory = "pdfs"
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Track downloaded files to avoid duplicates
downloaded_files = set()

# Open the target URL
driver.get(base_url)
time.sleep(2)  # Allow the page to load

try:
    page_number = 1
    while True:
        print(f"Scraping page {page_number}...")

        # Re-fetch PDF links on each page to avoid stale elements
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/DetailPeraturan/')]")

        # Process each link found on the page
        for link in pdf_links:
            try:
                # Re-check href for each link iteration to prevent stale element
                pdf_url = link.get_attribute("href")
                pdf_name = pdf_url.split("/")[-1] + ".pdf"
                pdf_path = os.path.join(download_directory, pdf_name)

                # Skip if already downloaded
                if pdf_name in downloaded_files:
                    print(f"Already downloaded: {pdf_name}")
                    continue

                print(f"Downloading: {pdf_name}")
                driver.get(pdf_url)  # Go to the detail page

                # Wait until the download button is clickable
                download_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Unduh')]"))
                )

                # Scroll to the download button if necessary
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                time.sleep(1)  # Small wait to ensure the scroll completes

                # Attempt to click the download button
                try:
                    download_button.click()  # Trigger the download
                    time.sleep(3)  # Adjust if needed for larger files
                    downloaded_files.add(pdf_name)  # Mark as downloaded

                except ElementClickInterceptedException:
                    print(f"Click intercepted for {pdf_name}, retrying...")
                    driver.execute_script("arguments[0].click();", download_button)
                    time.sleep(3)
                    downloaded_files.add(pdf_name)

                # Go back to the main page after each download
                driver.get(base_url)
                time.sleep(2)  # Wait for the main page to reload

            except StaleElementReferenceException:
                print("Encountered a stale element, skipping this link.")
                continue

        # Find and click the "Selanjutnya" button to go to the next page
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Selanjutnya")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)  # Scroll into view
            time.sleep(1)  # Small wait for scroll
            next_button.click()
            time.sleep(2)  # Allow the next page to load
            page_number += 1
        except NoSuchElementException:
            print("No more pages to scrape.")
            break

except (TimeoutException, NoSuchElementException) as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up and close the browser
    driver.quit()
    print("Script completed.")

