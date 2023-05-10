"""Models for hiring app."""

#notes from code review:
        # global lists in server.py > put the actual skill in the table rather than having to do a foreign key
    

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class JobSeeker(db.Model):
    __tablename__ = "job_seekers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    linkedin = db.Column(db.String)
    github = db.Column(db.String)
    location = db.Column(db.String)
    yoe = db.Column(db.Integer)
    desired_salary = db.Column(db.Integer)
    remote_only = db.Column(db.Boolean)
    sponsorship_needed = db.Column(db.Boolean)
    resume_url = db.Column(db.String)
    notifications_enabled = db.Column(db.Boolean, default=True)

    connection_requests = db.relationship("JobSeekerConnectionRequest", back_populates="sender")
    received_requests = db.relationship("RecruiterConnectionRequest", back_populates="receiver")
    skills = db.relationship("JobSeekerSkill", back_populates="job_seeker")
    role_types = db.relationship("JobSeekerRoleType", back_populates="job_seeker")
    notifications = db.relationship("JobSeekerNotificaton", back_populates="user_notified")
    saved_searches = db.relationship("JobSeekerSavedSearch", back_populates="user")

    def to_dict(self):
        result =  {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'linkedin': self.linkedin,
            'github': self.github,
            'location': self.location,
            'yoe': self.yoe,
            'salary': self.desired_salary,
            'remote': self.remote_only,
            'sponsorship': self.sponsorship_needed,
            'resume_url': self.resume_url   
        }
        return result
    
    

    def __repr__(self):
        return f"<JobSeeker id={self.id} email={self.email}>"


class Recruiter(db.Model):
    __tablename__ = "recruiters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    company = db.Column(db.String)
    linkedin = db.Column(db.String)
    notifications_enabled = db.Column(db.Boolean, default=True)

    roles = db.relationship("Role", back_populates="recruiter")
    connection_requests = db.relationship("RecruiterConnectionRequest", back_populates="sender")
    received_requests = db.relationship("JobSeekerConnectionRequest", back_populates="receiver")
    notifications = db.relationship("RecruiterNotification", back_populates="user_notified")
    saved_searches = db.relationship("RecruiterSavedSearch", back_populates="user")

    def __repr__(self):
        return f"<Recruiter id={self.id} email={self.email}>"
    
    def to_dict(self):
      result = {'id': self.id,
        'fname': self.fname,
        'lname': self.lname,
        'company': self.company,
        'linkedin': self.linkedin,
      }
      return result


class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    name = db.Column(db.String)
    role_type = db.Column(db.String)
    min_yoe = db.Column(db.Integer)
    level = db.Column(db.String)
    location = db.Column(db.String)
    salary = db.Column(db.Integer)
    remote = db.Column(db.Boolean)
    sponsorship_provided = db.Column(db.Boolean)
    jd_url = db.Column(db.String)

    recruiter = db.relationship("Recruiter", back_populates="roles")
    skills = db.relationship("RoleSkill", back_populates="role")

    def to_dict(self):
        result =  {
            'id': self.id,
            'recruiter_id': self.recruiter_id,
            'name': self.name,
            'role_type': self.role_type,
            'min_yoe': self.min_yoe,
            'level': self.level,
            'location': self.location,
            'salary': self.salary,
            'remote': self.remote,
            'sponsorship_provided': self.sponsorship_provided,
            'jd_url': self.jd_url
        }

        return result

    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"


class RoleSkill(db.Model):
    __tablename__ = "role_skills"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    skill_name = db.Column(db.String)

    role = db.relationship("Role", back_populates="skills")

    def to_dict(self):
        return {
            'id': self.id,
            'role_id': self.id,
            'skill_name': self.skill_name,
        }

    def __repr__(self):
        return f"<Skill id={self.id} name={self.skill_name}>"


class JobSeekerSkill(db.Model):
    __tablename__ = "js_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    skill_name = db.Column(db.String)

    job_seeker = db.relationship("JobSeeker", back_populates="skills")

    def to_dict(self):
        return {
            'id': self.id,
            'job_seeker_id': self.job_seeker_id,
            'skill_name': self.skill_name,
        }

    def __repr__(self):
        return f"<Skill id={self.id} name={self.skill_name}>"


class JobSeekerRoleType(db.Model):
    __tablename__ = "js_role_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    role_type = db.Column(db.String)

    job_seeker = db.relationship("JobSeeker", back_populates="role_types")

    def to_dict(self):
        return {
            'id': self.id,
            'job_seeker_id': self.job_seeker_id,
            'role_type': self.role_type,
        }

    def __repr__(self):
        return f"<Role type id={self.id} Type={self.role_type}>"

    
class JobSeekerConnectionRequest(db.Model):
    __tablename__ = "js_connect_rqsts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    requested_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    status = db.Column(db.String, nullable=False)

    sender = db.relationship("JobSeeker", back_populates="connection_requests")
    receiver = db.relationship("Recruiter", back_populates="received_requests")

    def __repr__(self):
        return f"<Connect Request requestor_id={self.requestor_id} requested_id={self.requested_id}>"


class RecruiterConnectionRequest(db.Model):
    __tablename__ = "rec_connect_rqsts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    requested_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    status = db.Column(db.String, nullable=False)

    sender = db.relationship("Recruiter", back_populates="connection_requests")
    receiver = db.relationship("JobSeeker", back_populates="received_requests")

    def __repr__(self):
        return f"<Connect Request requestor_id={self.requestor_id} requested_id={self.requested_id}>"

class JobSeekerNotificaton(db.Model):
    __tablename__ = "js_notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    js_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    received_request = db.Column(db.Integer, db.ForeignKey("rec_connect_rqsts.id"))
    sent_request = db.Column(db.Integer, db.ForeignKey("js_connect_rqsts.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String)
    read_status = db.Column(db.Boolean)

    user_notified = db.relationship("JobSeeker", back_populates="notifications")

    def __repr__(self):
        return f"Notification id={self.id} for user {self.js_id}"

class RecruiterNotification(db.Model):
    __tablename__ = "rec_notifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rec_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    received_request = db.Column(db.Integer, db.ForeignKey("js_connect_rqsts.id"))
    sent_request = db.Column(db.Integer, db.ForeignKey("rec_connect_rqsts.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.String)
    read_status = db.Column(db.Boolean)

    user_notified = db.relationship("Recruiter", back_populates="notifications")

    def __repr__(self):
        return f"Notification id={self.id} for user {self.rec_id}"

class JobSeekerSavedSearch(db.Model):
    __tablename__ = "js_saved_searches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    js_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    search_nickname = db.Column(db.String)
    search_params = db.Column(db.JSON)

    user = db.relationship("JobSeeker", back_populates="saved_searches")
    
    def __repr__(self):
        return f"Saved search id={self.id} for user {self.js_id}"
    
class RecruiterSavedSearch(db.Model):
    __tablename__ = "rec_saved_searches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rec_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    search_nickname = db.Column(db.String)
    search_params = db.Column(db.JSON)

    user = db.relationship("Recruiter", back_populates="saved_searches")
    
    def __repr__(self):
        return f"Saved search id={self.id} for user {self.js_id}"

def connect_to_db(flask_app, db_uri="postgresql:///jobs", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = False
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)


