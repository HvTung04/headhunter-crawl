import logging
import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import json

logging.getLogger('selenium').setLevel(logging.WARNING)

# Load environment variables from .env file
load_dotenv()

class Crawler:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")
        self.options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=self.options)
        
        # You can now access environment variables like this:
        self.linkedin_username = os.getenv('LINKEDIN_USERNAME')
        self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')

    def login_linkedin(self, username=None, password=None):
        """
        Log in to LinkedIn.

        Args:
        username (str, optional): The LinkedIn username. If not provided, uses environment variable.
        password (str, optional): The LinkedIn password. If not provided, uses environment variable.
        """
        username = username or self.linkedin_username
        password = password or self.linkedin_password
        
        if not username or not password:
            raise ValueError("LinkedIn credentials not found in environment variables or parameters")
            
        self.driver.get("https://www.linkedin.com/login?fromSignIn=true")
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys(username)
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)
    
    def load_cookies(self, cookies_path="cookies.json"):
        with open(cookies_path, "r") as file:
            cookies = json.load(file)
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        print("Cookies loaded")

    def login_linkedin_cookies(self):
        login_url = "https://www.linkedin.com/login"
        self.driver.get(login_url)
        time.sleep(5)
        self.load_cookies()
        self.driver.refresh()

    def search_linkedin_people(self, query, page):
        """
        Search for people on LinkedIn.
        """
        query = query.replace(" ", "%20")
        url = f"https://www.linkedin.com/search/results/people/?keywords={query}&page={page}"
        self.driver.get(url)
        time.sleep(5)

    def get_people_links(self):
        """
        Get the links of people from the search results.
        """
        people = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="mb1"]'))
        )
        hrefs = []
        for person in people:
            hrefs.append(person.find_element(By.TAG_NAME, "a").get_attribute("href"))
        return hrefs

    def get_company_from_profile(self, profile_link):
        """
        Get the latest company from a LinkedIn profile.

        Args:
        profile_link (str): The LinkedIn profile URL.

        Returns:
        str: The URL of the latest company.
        """
        self.driver.get(f"{profile_link}/details/experience/")
        try:
            latest_company = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-view-name="profile-component-entity"]//a'))
            )
        except:
            return ""
        return latest_company.get_attribute("href")

    def linkedin_about(self, company_link):
        """
        Get the "About" section of a LinkedIn company page.

        Args:
        company_link (str): The LinkedIn company URL.

        Returns:
        str: The scraped text of the "About" section.
        """
        self.driver.get(f"{company_link}/about/")
        try:
            about_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "main"))
            )
        except:
            return ""
        return about_section.text

    def get_text(self, url):
        """
        Get the text content of a webpage.

        Args:
        url (str): The URL of the webpage.

        Returns:
        str: The text content of the webpage.
        """
        self.driver.get(url)
        body = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return body.text
        
    def stop(self):
        self.driver.close()