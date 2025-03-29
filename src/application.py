from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import yaml
from resume_tailor import ResumeTailor

class ApplicationBot:
    def __init__(self):
        with open('config/config.yaml') as f:
            self.config = yaml.safe_load(f)
        
        self.driver = webdriver.Chrome()
        self.resume_tailor = ResumeTailor()
    
    def apply_to_job(self, job_details):
        """Apply to a single job posting"""
        try:
            self.driver.get(job_details['link'])
            time.sleep(3)  # Wait for page to load
            
            # Check if easy apply is available
            easy_apply_button = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
            if easy_apply_button:
                self._handle_easy_apply(job_details)
            else:
                self._handle_regular_application(job_details)
            
            return True
        except Exception as e:
            print(f"Failed to apply to {job_details['title']} at {job_details['company']}: {str(e)}")
            return False
    
    def _handle_easy_apply(self, job_details):
        """Handle LinkedIn Easy Apply"""
        # Click Easy Apply button
        self.driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-apply-button')]").click()
        time.sleep(2)
        
        # Fill out the multi-step form
        current_step = 0
        while True:
            try:
                # Tailor resume for this specific job
                job_description = self.driver.find_element(By.CSS_SELECTOR, ".jobs-description-content").text
                tailored_resume_path = self.resume_tailor.tailor_resume(
                    job_description, 
                    f"data/tailored_resume_{job_details['company'].replace(' ', '_')}.docx"
                )
                
                # Handle file upload if present
                file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if file_inputs:
                    file_inputs[0].send_keys(tailored_resume_path)
                
                # Click next or submit button
                next_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Next') or contains(@aria-label, 'Submit')]")
                if not next_buttons:
                    break
                
                next_buttons[0].click()
                current_step += 1
                time.sleep(2)
                
                # Break if we've gone through too many steps (safety)
                if current_step > 5:
                    break
            except Exception as e:
                print(f"Error in step {current_step}: {str(e)}")
                break
    
    def _handle_regular_application(self, job_details):
        """Handle applications on company websites"""
        # This would need to be customized per website
        # You might need to implement specific handlers for common platforms
        print(f"Regular application needed for {job_details['title']} at {job_details['company']}")
        # Implement website-specific logic here
    
    def close(self):
        self.driver.quit()