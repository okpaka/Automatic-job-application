from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class JobApplication(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    company = Column(String)
    location = Column(String)
    application_date = Column(DateTime, default=datetime.now)
    status = Column(String, default='Applied')  # Applied, Interview, Rejected, Offer
    source = Column(String)
    job_url = Column(String)
    notes = Column(String)
    follow_up_date = Column(DateTime)

class ApplicationTracker:
    def __init__(self):
        self.engine = create_engine('sqlite:///data/applications.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_application(self, job_details):
        """Record a new job application"""
        application = JobApplication(
            job_title=job_details['title'],
            company=job_details['company'],
            location=job_details['location'],
            source=job_details['source'],
            job_url=job_details['link']
        )
        self.session.add(application)
        self.session.commit()
        return application.id
    
    def update_status(self, application_id, new_status, notes=None):
        """Update the status of an application"""
        application = self.session.query(JobApplication).filter_by(id=application_id).first()
        if application:
            application.status = new_status
            if notes:
                application.notes = notes
            self.session.commit()
            return True
        return False
    
    def get_applications(self, status=None):
        """Get all applications, optionally filtered by status"""
        if status:
            return self.session.query(JobApplication).filter_by(status=status).all()
        return self.session.query(JobApplication).all()
    
    def close(self):
        self.session.close()