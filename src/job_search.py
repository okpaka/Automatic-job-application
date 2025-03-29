import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml
import time

class JobSearch:
    def __init__(self):
        with open('config/config.yaml') as f:
            self.config = yaml.safe_load(f)
        
        # Set up Selenium WebDriver (make sure you have ChromeDriver installed)
        self.driver = webdriver.Chrome()
    
    def search_linkedin(self, keywords, location):
        """Search for jobs on LinkedIn"""
        self.driver.get("https://www.linkedin.com/jobs")
        
        # Login (you'd need to handle this securely)
        self._linkedin_login()
        
        # Enter search criteria
        search_keywords = self.driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]")
        search_keywords.send_keys(keywords)
        
        search_location = self.driver.find_element(By.XPATH, "//input[contains(@id, 'jobs-search-box-location')]")
        search_location.send_keys(location)
        search_location.submit()
        
        time.sleep(3)  # Wait for results to load
        
        # Parse job listings
        jobs = []
        listings = self.driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")
        
        for job in listings:
            title = job.find_element(By.CSS_SELECTOR, "h3").text
            company = job.find_element(By.CSS_SELECTOR, "h4").text
            location = job.find_element(By.CSS_SELECTOR, "[class*='job-card-container__metadata-item']").text
            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "source": "LinkedIn"
            })
        
        return jobs
    
    def _linkedin_login(self):
        """Handle LinkedIn login (simplified - use proper credential management)"""
        with open('config/credentials.yaml') as f:
            creds = yaml.safe_load(f)
        
        email = self.driver.find_element(By.ID, "username")
        email.send_keys(creds['linkedin']['email'])
        
        password = self.driver.find_element(By.ID, "password")
        password.send_keys(creds['linkedin']['password'])
        
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
    
    def close(self):
        self.driver.quit()