"""Models for hiring app."""

#notes from code review:
        # global lists in server.py > put the actual skill in the table rather than having to do a foreign key
    

from flask_sqlalchemy import SQLAlchemy

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

    connection_request = db.relationship("JobSeekerConnectionRequest", back_populates="sender")
    received_request = db.relationship("RecruiterConnectionRequest", back_populates="receiver")
    skills = db.relationship("JobSeekerSkill", back_populates="job_seeker")
    role_types = db.relationship("JobSeekerRoleType", back_populates="job_seeker")

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

    roles = db.relationship("Role", back_populates="recruiter")
    connection_request = db.relationship("RecruiterConnectionRequest", back_populates="sender")
    received_request = db.relationship("JobSeekerConnectionRequest", back_populates="receiver")

    def __repr__(self):
        return f"<Recruiter id={self.id} email={self.email}>"


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

    recruiter = db.relationship("Recruiter", back_populates="roles")
    skills = db.relationship("RoleSkill", back_populates="role")

    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"


class RoleSkill(db.Model):
    __tablename__ = "role_skills"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    skill_name = db.Column(db.String)

    role = db.relationship("Role", back_populates="skills")

    def __repr__(self):
        return f"<Skill id={self.id} name={self.skill_name}>"


class JobSeekerSkill(db.Model):
    __tablename__ = "js_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    skill_name = db.Column(db.String)

    job_seeker = db.relationship("JobSeeker", back_populates="skills")

    def __repr__(self):
        return f"<Skill id={self.id} name={self.skill_name}>"


class JobSeekerRoleType(db.Model):
    __tablename__ = "js_role_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_seeker_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    role_type = db.Column(db.String)

    job_seeker = db.relationship("JobSeeker", back_populates="role_types")

    def __repr__(self):
        return f"<Role type id={self.id} Type={self.role_type}>"

    
class JobSeekerConnectionRequest(db.Model):
    __tablename__ = "js_connect_rqst"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    requested_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    accepted = db.Column(db.Boolean, nullable=False)

    sender = db.relationship("JobSeeker", back_populates="connection_request")
    receiver = db.relationship("Recruiter", back_populates="received_request")

    def __repr__(self):
        return f"<Connect Request requestor_id={self.requestor_id} requested_id={self.requested_id}>"


class RecruiterConnectionRequest(db.Model):
    __tablename__ = "rec_connect_rqst"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requestor_id = db.Column(db.Integer, db.ForeignKey("recruiters.id"))
    requested_id = db.Column(db.Integer, db.ForeignKey("job_seekers.id"))
    accepted = db.Column(db.Boolean, nullable=False)

    sender = db.relationship("Recruiter", back_populates="connection_request")
    receiver = db.relationship("JobSeeker", back_populates="received_request")

    def __repr__(self):
        return f"<Connect Request requestor_id={self.requestor_id} requested_id={self.requested_id}>"


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


