from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import keyboard  # For listening to hotkeys

# Set up WebDriver using WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www.behance.net/joblist?tracking_source=nav20"
driver.get(url)

# Allow initial page load
print("Waiting for the page to load...")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "JobCard-jobCard-mzZ"))
)
print("Page loaded successfully.")

print("Scrolling... Press 'ESC' to stop.")

# Scroll until the user presses the 'ESC' key
try:
    last_height = driver.execute_script("return document.body.scrollHeight")
    while not keyboard.is_pressed('esc'):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow time for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break
        last_height = new_height
    print("Scrolling stopped by user.")
except Exception as e:
    print(f"Error occurred during scrolling: {e}")

# Find all job cards
try:
    job_cards = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "JobCard-jobCard-mzZ"))
    )
    print(f"Number of job cards found: {len(job_cards)}")
except TimeoutException:
    print("No job cards were found.")
    driver.quit()
    exit()

# Prepare data storage
data = []

# Extract details for each job card
for index, card in enumerate(job_cards):
    try:
        company = card.find_element(By.CLASS_NAME, "JobCard-company-GQS").text
        title = card.find_element(By.CLASS_NAME, "JobCard-jobTitle-LS4").text
        description = card.find_element(By.CLASS_NAME, "JobCard-jobDescription-SYp").text
        time_posted = card.find_element(By.CLASS_NAME, "JobCard-time-Cvz").text
        location = card.find_element(By.CLASS_NAME, "JobCard-jobLocation-sjd").text
        image_element = card.find_element(By.CLASS_NAME, "JobLogo-logoButton-aes").find_element(By.TAG_NAME, "img")
        image_url = image_element.get_attribute("src")

        # Add extracted data to the list
        data.append([company, title, description, time_posted, location, image_url])
        print(f"Successfully extracted job details for card {index + 1}")

    except NoSuchElementException as e:
        print(f"Missing element in job card {index + 1}: {e}")
    except Exception as e:
        print(f"Error extracting job details for card {index + 1}: {e}")

# Save to CSV
if data:
    filename = "behance_jobs.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company", "Job Title", "Description", "Time Posted", "Location", "Image URL"])  # Header
        writer.writerows(data)
    print(f"Data saved to {filename}")
else:
    print("No data to save.")

# Close the driver
driver.quit()
