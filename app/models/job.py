from datetime import datetime
from app.extensions.db import db

class Job(db.Model):
    __tablename__="jobs"

    id = db.Column(db.Integer, primary_key=True)

    scrape_id =db.Column(db.String(36), nullable =False, index = True)
    source = db.Column(db.String(50), nullable =False, index = True)

    title = db.Column(db.String(255), nullable =False)
    company = db.Column(db.String(255), nullable=False)

    skills = db.Column(db.Text, nullable =True)
    experience = db.Column(db.String(100), nullable = True)
    salary = db.Column(db.String(100), nullable = True)
    location = db.Column(db.String(255), nullable =True, index = True)

    created_at = db.Column(db.DateTime,default = datetime.utcnow, nullable = False, index =True)

    # api - friendly representation

    def to_dict(self) -> dict:
        return{
            "id": self.id,
            "scrape_id": self.scrape_id,
            "source": self.source,
            "title": self.title,
            "company":self.company,
            "skills": self.skills,
            "experience": self.experience,
            "salary":self.salary,
            "location": self.location,
            "created_at": self.created_at.isoformat(),  # convert datetime to ISO format
        }
                