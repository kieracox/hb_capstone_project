"""CRUD operations."""

from model import db, JobSeeker, Recruiter, Role, RoleSkill, JobSeekerSkill, JobSeekerRoleType, JobSeekerConnectionRequest, RecruiterConnectionRequest, connect_to_db

def create_job_seeker(email, password, fname='', lname='',  
                      linkedin='', github='', location='', yoe=0, desired_salary=0,
                      remote_only=False, sponsorship_needed=False, resume_url=''):
   
    """Create and return a new job seeker."""

    job_seeker = JobSeeker(email=email, password=password, fname=fname, lname=lname,
                            linkedin=linkedin, github=github, location=location, yoe=yoe,
                            desired_salary=desired_salary, remote_only=remote_only, sponsorship_needed=sponsorship_needed, resume_url=resume_url)
    
    return job_seeker

def return_all_job_seekers():
    """Return all job seekers."""
    return JobSeeker.query.all()

def get_js_by_id(id):
    """Get and return a job seeker by their id."""
    return JobSeeker.query.get(id)

def get_js_by_email(email):
    """Get and return a job seeker by their email."""
    return JobSeeker.query.filter(JobSeeker.email == email).first()

def create_recruiter(email, password, fname='', lname='', company='', linkedin=''):
    """Create and return a new recruiter."""
    recruiter = Recruiter(fname=fname, lname=lname, email=email, password=password, company=company, linkedin=linkedin)
    
    return recruiter

def return_all_recruiters():
    """Return all recruiters."""
    return Recruiter.query.all()

def get_recruiter_by_id(id):
    """Get and return a recruiter by their id."""
    return Recruiter.query.get(id)

def get_recruiter_by_email(email):
    """Get and return a job seeker by their email."""
    return Recruiter.query.filter(Recruiter.email == email).first()

def create_role(recruiter, name='', role_type='', 
                min_yoe=0, level='', location='', salary=0,
                remote=False, sponsorship_provided=False):
    
    """Create and return a new role."""
    
    role = Role(recruiter=recruiter, name=name, role_type=role_type, 
                min_yoe=min_yoe, level=level, location=location, 
                salary=salary, remote=remote, sponsorship_provided=sponsorship_provided)
    
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

def get_role_skill(role_id):
    """Get a role's skills."""
    return RoleSkill.query.filter(RoleSkill.role_id == role_id).all()

def edit_rec_profile(rec_id, fname, lname, company, linkedin):
    """Update a recruiter's profile with the data they provide."""
    user = Recruiter.query.get(rec_id)

    if fname:
        user.fname = fname
    if lname:
        user.lname = lname
    if linkedin:
        user.linkedin = linkedin

    if company:
        user.company = company
    
    db.session.commit() 

def edit_role(role_id, role_name, role_type, location, yoe, level, min_salary, remote, sponsorship_provided ):
    """Update a role's information."""
    role = Role.query.get(role_id)
    print('crud.py 96:', role_name)
    if role_name:
        role.name = role_name
    if role_type:
        role.role_type = role_type
    if location:
        role.location = location
    if yoe:
        role.yoe = yoe
    if level:
        role.level = level
    if min_salary:
        role.min_salary = min_salary
    if remote is not None:
        role.remote = remote
    if sponsorship_provided is not None:
        role.sponsorship_provided = sponsorship_provided
    
    db.session.commit()

def create_js_skill(job_seeker_id, skill_name):
    """Create and return a new job seeker skill."""
    js_skill = JobSeekerSkill(job_seeker_id=job_seeker_id, skill_name=skill_name)

    return js_skill

def get_js_skill(job_seeker_id):
    """Get a job seeker's skills."""
    return JobSeekerSkill.query.filter(JobSeekerSkill.job_seeker_id == job_seeker_id).all()

def create_js_roletype(job_seeker_id, role_type):
    """Create and return a new job seeker role type."""
    js_roletype = JobSeekerRoleType(job_seeker_id=job_seeker_id, role_type=role_type)

    return js_roletype

def get_js_roletype(job_seeker_id):
    """Get a job seeker's role type."""
    return JobSeekerRoleType.query.filter(JobSeekerRoleType.job_seeker_id == job_seeker_id).all()

def edit_js_profile(job_seeker_id, fname, lname, linkedin, github, location, yoe, desired_salary, remote_only, sponsorship_needed):
    """Update a jobseeker's profile with the data they provide."""
    user = JobSeeker.query.get(job_seeker_id)

    if fname:
        user.fname = fname
    if lname:
        user.lname = lname
    if linkedin:
        user.linkedin = linkedin
    if github:
        user.github = github
    if location:
        user.location = location
    if yoe:
        user.yoe = yoe
    if desired_salary:
        user.desired_salary = desired_salary
    if remote_only:
        user.remote_only = remote_only
    if sponsorship_needed:
        user.sponsorship_needed = sponsorship_needed

    db.session.commit()  


def js_role_search(role_type, level, location, yoe, yoe_param, salary, salary_param, remote, sponsorship):
    roles = db.session.query(Role)

    if role_type != "All":
        roles = roles.filter(Role.role_type == role_type)
    
    if level != "All":
        roles = roles.filter(Role.level == level)

    if location != "All":
        roles = roles.filter(Role.location == location)
    
    if yoe != None and yoe_param == "exact":
        roles = roles.filter(Role.min_yoe == yoe)
    elif yoe != None and yoe_param == "higher":
        roles = roles.filter(Role.min_yoe >= yoe)
    elif yoe != None and yoe_param == "lower":
        roles = roles.filter(Role.min_yoe <= yoe)

    if salary != None and salary_param == "exact":
        roles = roles.filter(Role.salary == salary)
    elif salary != None and salary_param == "higher":
        roles = roles.filter(Role.salary >= salary)
    elif salary != None and salary_param == "lower":
        roles = roles.filter(Role.salary <= salary)
    
    if remote == "yes":
        roles = roles.filter(Role.remote == True)

    if sponsorship == "yes":
        roles = roles.filter(Role.sponsorship_provided == True)
    
    return roles


    
        

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