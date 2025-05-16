from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import string
import time
import logging
import os

# Create logs and output directories
os.makedirs('logs', exist_ok=True)
os.makedirs('output', exist_ok=True)

# Set up logging
logging.basicConfig(filename='logs/errors.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Starting script execution")  # Log start of script

def generate_random_string(length):
    """Generate a random string of letters and digits"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def handle_popup(driver):
    """Handle pop-up windows"""
    logging.debug("Checking for pop-ups")
    original_window = driver.current_window_handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            driver.close()
    driver.switch_to.window(original_window)

def main():
    # Set up browser
    logging.debug("Setting up Chrome browser")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Phase 1: Create user
        logging.debug("Navigating to create.php")
        driver.get('https://moodtv.xyz/create.php')
        
        # Generate username and password
        username = f"user_{generate_random_string(8)}"
        password = generate_random_string(12)
        logging.debug(f"Generated username: {username}, password: {password}")
        
        # Enter credentials
        logging.debug("Entering credentials")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
        driver.find_element(By.ID, 'get_user_button').click()
        
        # Phase 2: Handle ads (3 iterations)
        for i in range(3):
            logging.debug(f"Ad iteration {i+1}")
            WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.ID, 'next_button')))
            handle_popup(driver)
            try:
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close_video'))).click()
            except:
                logging.debug("No video close button found")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'skip_button'))).click()
            driver.find_element(By.ID, 'next_button').click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'next_button_second')))
            driver.find_element(By.ID, 'next_button_second').click()
        
        # Phase 3: Handle continue pages (3 iterations)
        for i in range(3):
            logging.debug(f"Continue iteration {i+1}")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'continue_button')))
            driver.find_element(By.ID, 'continue_button').click()
            driver.back()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'continue_button')))
            driver.find_element(By.ID, 'continue_button').click()
        
        # Phase 4: Copy M3U link
        logging.debug("Copying M3U link")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'copy_m3u_button'))).click()
        m3u_link = driver.find_element(By.ID, 'm3u_link').get_attribute('data-clipboard-text')
        
        # Save link to file
        logging.debug(f"Saving M3U link: {m3u_link}")
        with open('output/playlist.m3u', 'w') as f:
            f.write(m3u_link)
        
        print(f"Saved M3U link: {m3u_link}")
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"An error occurred, check logs/errors.log")
        raise
    
    finally:
        driver.quit()
        logging.debug("Browser closed")

if __name__ == "__main__":
    main()
