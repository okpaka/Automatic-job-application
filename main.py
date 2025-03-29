"""
A Python project that can help automate job applications on your behalf. 
This will be a sophisticated bot that can search job boards, tailor your resume, 
and submit applications automatically.

            Project Overview

            We'll create a system that:

                1 Searches job boards for relevant positions

                2 Parses job descriptions to understand requirements

                3 Customizes your resume/CV for each position

                4 Fills out application forms

                5 Tracks applications and follow-ups
"""

from job_search import JobSearch
from application import ApplicationBot
from tracker import ApplicationTracker
import yaml
import time

def main():
    # Load configuration
    with open('config/config.yaml') as f:
        config = yaml.safe_load(f)
    
    # Initialize components
    job_search = JobSearch()
    application_bot = ApplicationBot()
    tracker = ApplicationTracker()
    
    try:
        # Search for jobs
        print("Searching for jobs...")
        jobs = job_search.search_linkedin(
            keywords=config['search_keywords'],
            location=config['search_location']
        )
        
        print(f"Found {len(jobs)} jobs. Starting applications...")
        
        # Apply to each job
        for job in jobs[:5]:  # Limit to 5 applications for demo
            print(f"Applying to {job['title']} at {job['company']}...")
            
            # Apply to the job
            success = application_bot.apply_to_job(job)
            
            # Track the application
            if success:
                app_id = tracker.add_application(job)
                print(f"Successfully applied! Application ID: {app_id}")
            else:
                print("Application failed.")
            
            time.sleep(5)  # Be polite with delays between applications
    
    finally:
        # Clean up
        job_search.close()
        application_bot.close()
        tracker.close()

if __name__ == "__main__":
    main()