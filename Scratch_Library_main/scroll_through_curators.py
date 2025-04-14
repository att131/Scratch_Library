from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys

from Scratch_Library_main.Scratch_Library_main._scratch_website_lib import Studio, scroll_through_curators

def start_ui():
    # Ask for the studio ID and validate it
    studio_id = input("Enter the studio ID: ").strip()
    if not studio_id.isdigit():
        print("Invalid studio ID")
        return
    
    studio_id = int(studio_id)

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the website
    driver.get(Studio(studio_id).get_curator_url())

    # Scroll through curators
    wait = WebDriverWait(driver, 5)
    scroll_through_curators(driver, wait)
    
    # Fullscreen the window
    #driver.fullscreen_window()

    input("Press [ENTER] to close the page... ")

    driver.quit()
