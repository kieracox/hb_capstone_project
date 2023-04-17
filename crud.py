"""CRUD operations."""

from model import db, JobSeeker, Recruiter, Role, RoleSkill, JobSeekerSkill, JobSeekerRoleType, JobSeekerConnectionRequest, RecruiterConnectionRequest, connect_to_db

def create_job_seeker(fname, lname, email, password, 
                      linkedin, github='', location='', yoe='', 
                      remote_only=False, sponsorship_needed=False, salary=''):
   
    """Create and return a new job seeker."""

    job_seeker = JobSeeker(fname=fname, lname=lname, email=email, password=password,
                            linkedin=linkedin, github=github, location=location, yoe=yoe,
                            remote_only=remote_only, sponsorship_needed=sponsorship_needed, salary=salary)
    
    return job_seeker

def return_all_job_seekers():
    """Return all job seekers."""
    return JobSeeker.query.all()

def get_js_by_id(id):
    """Get and return a job seeker by their id."""
    return JobSeeker.query.get(id)

def create_recruiter(fname, lname, email, password, linkedin):
    """Create and return a new recruiter."""
    recruiter = Recruiter(fname=fname, lname=lname, email=email, password=password, linkedin=linkedin)
    
    return recruiter

def return_all_recruiters():
    """Return all recruiters."""
    return Recruiter.query.all()

def get_recruiter_by_id(id):
    """Get and return a recruiter by their id."""
    return Recruiter.query.get(id)

def create_role(recruiter_id, name, role_type, 
                min_yoe, level='', location='', 
                remote=False, sponsorship_provided=False, salary=0):
    
    """Create and return a new role."""
    
    role = Role(recruiter_id=recruiter_id, name=name, role_type=role_type, 
                min_yoe=min_yoe, level=level, location=location, 
                remote=remote, sponsorship_provided=sponsorship_provided, salary=salary)
    
    return role

def return_all_roles():
    """Return all roles."""
    return Role.query.all()

def get_role_by_id(id):
    """Get and return a role by its id."""
    return Role.query.get(id)

def create_role_skill(role_id, skill_name):
    """Create and return a new role skill."""
    role_skill = RoleSkill(role_id=role_id, skill_name=skill_name)

    return role_skill

def create_js_skill(job_seeker_id, skill_name):
    """Create and return a new job seeker skill."""
    js_skill = JobSeekerSkill(job_seeker_id=job_seeker_id, skill_name=skill_name)

    return js_skill

def create_js_roletype(job_seeker_id, role_type):
    """Create and return a new job seeker role type."""
    js_roletype = JobSeekerRoleType(job_seeker_id=job_seeker_id, role_type=role_type)

    return js_roletype

def js_request_connect(requestor_id, requested_id, accepted=False):
    """Create and return a connection request from a job seeker."""
    
    return JobSeekerConnectionRequest(requestor_id=requestor_id, requested_id=requested_id, accepted=accepted)

    

def rec_request_connect(requestor_id, requested_id, accepted=False):
    """Create and return a connection request from a recruiter."""

    connection_request = RecruiterConnectionRequest(requestor_id=requestor_id, requested_id=requested_id, accepted=accepted)

    return connection_request


if __name__ == '__main__':
    from server import app
    connect_to_db(app)