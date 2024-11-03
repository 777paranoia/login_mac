import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import time

# Set up logging
log_path = os.path.expanduser('~/.login_log/login_script.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO)

# Function to read credentials from file
def read_credentials(filepath):
    credentials = {}
    try:
        with open(filepath, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                credentials[key] = value
    except FileNotFoundError:
        logging.error("Credentials file not found.")
        raise
    except Exception as e:
        logging.error(f"Error reading credentials: {e}")
        raise
    return credentials.get('username'), credentials.get('password')

def login():
    logging.info(f'Script started at {datetime.now()}')

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get('http://www.showcrewnetwork.com')
        logging.info('Opened login page')

        # Read credentials
        username, password = read_credentials('credentials.txt')
        
        if not username or not password:
            raise Exception("Username or password missing in credentials file.")

        # Input credentials
        driver.find_element(By.ID, 'modlgn-username').send_keys(username)
        driver.find_element(By.ID, 'modlgn-passwd').send_keys(password)

        logging.info('Entered username and password')

        # Find and click the login button
        login_button = driver.find_element(By.CLASS_NAME, 'login-button')
        login_button.click()

        logging.info('Login button clicked')
        time.sleep(5)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.expanduser(f'~/.login_log/screenshot_{timestamp}.png')
        driver.save_screenshot(screenshot_path)
        logging.info(f'Screenshot saved: {screenshot_path}')

    except Exception as e:
        logging.error(f'Error during login: {e}')

    finally:
        driver.quit()
        logging.info(f'Script finished at {datetime.now()}')

login()

