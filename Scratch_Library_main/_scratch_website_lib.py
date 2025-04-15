from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, NoSuchWindowException
from selenium.webdriver.common.keys import Keys

import requests
import numpy as np
from time import sleep
import random
import pyperclip

# VARIABLES

FOLLOWERS = "FOLLOWERS"
FOLLOWING = "FOLLOWING"

NPY_PATH = "usernames.npy"
MANUAL_PATH = "names.txt"

LOGIN_URL = 'https://scratch.mit.edu/login'

PASSWORD = "cupcake"
USERNAME = "Fluffy_Notebook"

WEEKLY_SHOUTOUT_STUDIO_ID = 36283762

POSSIBLE_POINT_INCREMENTS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# FUNCTIONS

# Web scraping functions

def get_website_requests(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.text

def get_website(url):
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the website
    driver.get(url)

    # Wait for a specific element to be present before proceeding
    # Adjust the timeout and the element to wait for as needed
    try:
        element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return

    # Retrieve the HTML of the website
    html = driver.page_source

    # Close the browser
    driver.quit()

    # Return the html
    return html

def scroll_through_curators(driver, wait):
    # Click the "Load more" button until it is no longer clickable
    while True:
        sleep(0.1)
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="button"]')))
            button.click()
        except: # (NoSuchElementException, StaleElementReferenceException, NoSuchWindowException, TimeoutException):
            return

# Luck studio functions

def sort_lines(lines):
    return sorted(lines, key = lambda line: line.points, reverse = True)

def format_lines(lines):
    result = ""

    for line_idx, line in enumerate(lines):
        result += line.as_string(line_idx + 1)

    return result

def get_luck_studio_current_points():
    raise NotImplementedError("This function is not implemented yet.")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the website
    driver.get("https://scratch.mit.edu/studios/36531441/")

    wait = WebDriverWait(driver, 5)

def copy_luck_studio_update():
    print("Enter the data (Press [ENTER] twice to input): ")

    lines = []
    while True:
        line = input()
        if line == "":  # Blank line to signal end of input
            break
        lines.append(line)
        
    data = "\n".join(lines).strip().split("\n")

    if len(data) != 50:
        return "Expected 50 entries!"

    # Create the lines
    lines = [Line() for line in range(len(data))]
    for line_idx in range(len(lines)):
        lines[line_idx].text_init(data[line_idx])

    if len(lines) != len(data):
        return "Internal error: {}/{}".format(len(lines), len(data))

    # Increment the lines
    for line_idx in range(len(lines)):
        lines[line_idx].increment_points()

    # Sort, format, and print the lines
    lines = format_lines(sort_lines(lines))

    pyperclip.copy(lines)

# Luck line class

class Line(object):
    def text_init(self, text):
        # place - @username - points
        data = text.strip().split(" - ")
        
        assert len(data) == 3

        self.username = data[1].strip()
        self.points = int(data[2].strip())

    def increment_points(self):
        self.points += random.choice(POSSIBLE_POINT_INCREMENTS)

    def as_string(self, place):
        return "{} - {} - {}\n".format(place, self.username, self.points)

# Scratcher Class

class Scratcher(object):
    def __init__(self, username):
        self.username = username

    # FOLLOWERS

    def is_following(self, username):
        # Get the usernames this account is following
        following = self.get_followers_following(FOLLOWING)

        # Return if the username is in the following list
        return username in following

    def generate_followers_urls(self, username, n_pages, page_type = FOLLOWING):
        # Generate the base url for the username page
        if page_type == FOLLOWERS:
            base_url = 'https://scratch.mit.edu/users/{}/followers/?page='.format(username)
        elif page_type == FOLLOWING:
            base_url = 'https://scratch.mit.edu/users/{}/following/?page='.format(username)
        else:
            raise Exception("Invalid page type: {}".format(page_type))
        
        # Initalize a list of urls
        urls = []

        # Iterate through all the pages of followers
        for i in range(n_pages):
            # Add the url to the list
            urls.append(base_url + str(i + 1))

        # Return the result
        return urls

    GET_FOLLOWERS_PAGES_TEXT = "page-links"
    GET_FOLLOWERS_PAGES_STOP_TEXT = "</div>"
    GET_FOLLOWERS_PAGES_SPAN = "span"
    GET_FOLLOWERS_PAGES_FIRST_SKIP = 42

    def get_followers_pages(self, page_type):
        # Generate the urls for the first follower page
        url = self.generate_followers_urls(self.username, 1, page_type)[0]

        # Get the HTML from the url
        html = get_website_requests(url)

        # If html is None, the VPN was not turned on
        if not html:
            raise Exception("VPN was not turned on.")

        # Find the location of the parent span tag of the list of links to other pages
        start_location = html.find(Scratcher.GET_FOLLOWERS_PAGES_TEXT)

        # Add the skip amount to the start location
        start_location += Scratcher.GET_FOLLOWERS_PAGES_FIRST_SKIP

        # Cut off the html text from the start position so it is easier to work with
        html = html[start_location:]

        # Now, keep going till we find the stop text
        # The fomula is, count the "span"s, sub 2, and div 2

        span_count = 0

        # Keep looping till loop is broken
        while True:
            # Get the location of the next span
            span_location = html.find(Scratcher.GET_FOLLOWERS_PAGES_SPAN)

            # Make sure we have not passed a div, if so, the pages section of the code has ended
            # After finding the div location, compare it to the location of the next span
            # If the div location is lower, the div is sooner than the next span and we break the loop
            div_location = html.find(Scratcher.GET_FOLLOWERS_PAGES_STOP_TEXT)
            if div_location < span_location:
                break

            # Otherwise, add one to the span count, and cut off the html
            span_count += 1
            html = html[span_location + len(Scratcher.GET_FOLLOWERS_PAGES_SPAN):]

        # Calculate the number of pages, based on the number of spans
        pages = int((span_count - 2) / 2)

        # 1 page will show up as 0, so set it
        if pages == 0:
            pages = 1

        # Return the number of pages
        return pages

    GET_FOLLOWERS_SKIP_CHAR = "/"
    GET_FOLLOWERS_CHARS_TO_SKIP = 20
    GET_FOLLOWERS_PER_PAGE = 59 # Doesn't include first username, the real number is 60
    GET_FOLLOWERS_AFTER_THUMB = 39
    GET_FOLLOWERS_THUMB_TEXT = "user thumb item"

    def get_followers_following(self, page_type):
        # Generate the urls for the followers pages
        urls = self.generate_followers_urls(self.username, self.get_followers_pages(page_type), page_type)

        usernames = []

        # Iterate through all the urls
        for url in urls:
            # Print a progress message
            print("Reading pages: {}/{}".format(urls.index(url) + 1, len(urls)))

            # Get the text
            html = get_website_requests(url)

            # Return the existing usernames if the page failed to load
            if not html:
                return usernames

            # Get start location
            start_location = html.find(Scratcher.GET_FOLLOWERS_THUMB_TEXT) + Scratcher.GET_FOLLOWERS_AFTER_THUMB

            # Shorten url
            html = html[start_location - 1:]

            # Get first username
            usernames.append(html[:html.find(Scratcher.GET_FOLLOWERS_SKIP_CHAR)])

            # First username needed one more char, so add it back
            html = html[1:]

            # Iterate through all the code
            for i in range(Scratcher.GET_FOLLOWERS_PER_PAGE):
                # Skip the number of triangles
                for i in range(Scratcher.GET_FOLLOWERS_CHARS_TO_SKIP):
                    start_location = html.find(Scratcher.GET_FOLLOWERS_SKIP_CHAR)

                    # Cut off the html, but add delete one more char, this is the triangle
                    html = html[start_location + 1:]

                usernames.append(html[:html.find(Scratcher.GET_FOLLOWERS_SKIP_CHAR)])
        
        # Each of the methods introduce some incorrect random text, delete that
        if page_type == FOLLOWERS:
            del usernames[-9:]
        elif page_type == FOLLOWING:
            del usernames[-14:]

        # Convert the data to a np array
        return np.array(usernames)

# Studio Class

class Studio(object):
    def __init__(self, studio_id = 36283762):
        self.studio_id = studio_id

    def get_curator_url(self):
        return "https://scratch.mit.edu/studios/{}/curators".format(self.studio_id)
    
    CHARS_AFTER_A_TO_SKIP = 16
    TAG_TO_FIND = "<a"
    START_LOCATION_TEXT = "studio-members-grid"
    ENDING_TEXT = "studio-member-tile"

    def get_curators(self):
        # Returns a list of the curators AND managers

        # Get the url of the studio
        url = self.get_curator_url()
        
        # Initialize the Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Open the website
        driver.get(url)

        # Scroll through the curators
        wait = WebDriverWait(driver, 5)
        scroll_through_curators(driver, wait)

        # Copy the HTML text
        html = driver.page_source[:]

        # Find all the curators:
        # First, find the "studio-members-grid" as the start location
        # Then, find each of the "<a" tags, and skip 16 chars to get the username
        # Cut off the html, and find the first " symbol as the end of the username
        # Add the username to the list
        # Skip one "<a" tag, and repeat the process

        # Cut off the html text to the start location
        start_location = html.find(Studio.START_LOCATION_TEXT)
        html = html[start_location:]

        curators = []
        while True:
            # Try to find the "studio-member-tile" text
            # If it is not found, we are done
            if html.find(Studio.ENDING_TEXT) == -1:
                break

            # Find the first "<a" tag
            a_location = html.find(Studio.TAG_TO_FIND) + Studio.CHARS_AFTER_A_TO_SKIP

            # Cut off the html text to the "<a" tag
            html = html[a_location:]

            # Find the end of the username
            end_location = html.find("\"")

            # Add the username to the list
            curators.append(html[:end_location])

            # Find the next "<a" tag
            a_location = html.find(Studio.TAG_TO_FIND) + len(Studio.TAG_TO_FIND)

            # Cut off the html
            html = html[a_location:]

        # Close the driver
        driver.quit()

        return curators

    def invite_curators(self, curators, func = None):
        # Enter the usernames of curators to invite
        usernames = list(np.load(NPY_PATH))

        # Initialize the web driver (e.g., Chrome)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # Open the login page
        driver.get(LOGIN_URL)

        # Wait until the username input is interactable
        wait = WebDriverWait(driver, 10)
        username_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_username" and @name="username"]')))
        password_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="id_password" and @name="password"]')))

        # Alternative method using CSS Selectors
        # username_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="id_username"][name="username"]')))
        # password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[id="id_password"][name="password"]')))

        # Enter username and password
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        # Click "Sign in" button
        sign_in_button = driver.find_element(By.XPATH, '//button[contains(text(), "Login")]')
        sign_in_button.click()

        # Wait for login to complete
        sleep(5)

        # Go to the URL of the studio
        driver.get(self.get_curator_url())

        for username_idx, username in enumerate(usernames):
            # Scroll into view if needed
            invite_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[not(@name="q")]')))
            #driver.execute_script("arguments[0].scrollIntoView(true);", invite_input)
            
            invite_input.send_keys(username)
            invite_input.send_keys(Keys.RETURN)
            del usernames[username_idx] # Remove this username from the list

            # Every 3 usernames, execute the given function, and pass the usernames
            if username_idx % 3 == 0:
                print("Usernames used: {}".format(username_idx))
                if func:
                    func(usernames)

            sleep(0.3)
            #wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Invite")]')))  

        # Close the browser
        driver.quit()

# TEST

if __name__ == "__main__":
    studio = Studio(36533604)

    curators = studio.get_curators()
    print(curators)
    
    # Create a scratcher
    scratcher = Scratcher("asmileyfacesticker")

    # Get the number of followers pages
    print("# followers pages:", scratcher.get_followers_pages(FOLLOWERS))
    print("# following pages:", scratcher.get_followers_pages(FOLLOWING))
    print("# Followers: {}".format(len(scratcher.get_followers_following(FOLLOWERS))))
    print("# Following: {}".format(len(scratcher.get_followers_following(FOLLOWING))))
    print("Is following blast: {}".format(scratcher.is_following("Crazy-Coderz")))
