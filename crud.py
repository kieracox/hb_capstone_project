"""CRUD operations."""

from model import db, JobSeeker, Recruiter, Role, RoleSkill, JobSeekerSkill, JobSeekerRoleType, JobSeekerConnectionRequest, RecruiterConnectionRequest, JobSeekerNotificaton, RecruiterNotification, connect_to_db
from datetime import datetime

def create_job_seeker(email, password, fname='', lname='',  
                      linkedin='', github='', location='', yoe=0, desired_salary=0,
                      remote_only=False, sponsorship_needed=False, resume_url=''):
    """Create and return a new job seeker."""
    return JobSeeker(email=email, password=password, fname=fname, lname=lname,
                            linkedin=linkedin, github=github, location=location, yoe=yoe,
                            desired_salary=desired_salary, remote_only=remote_only, sponsorship_needed=sponsorship_needed, resume_url=resume_url) 

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
    return Recruiter(fname=fname, lname=lname, email=email, password=password, company=company, linkedin=linkedin)
    
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
                remote=False, sponsorship_provided=False, jd_url=''):
    """Create and return a new role."""
    return Role(recruiter=recruiter, name=name, role_type=role_type, 
                min_yoe=min_yoe, level=level, location=location, 
                salary=salary, remote=remote, sponsorship_provided=sponsorship_provided, jd_url=jd_url)
    
def return_all_roles():
    """Return all roles."""
    return Role.query.all()

def get_role_by_id(id):
    """Get and return a role by its id."""
    return Role.query.get(id)

def create_role_skill(role_id, skill_name):
    """Create and return a new role skill."""
    return RoleSkill(role_id=role_id, skill_name=skill_name)

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
    job_seeker = JobSeeker.query.get(job_seeker_id)
    js_skill = JobSeekerSkill(job_seeker=job_seeker, skill_name=skill_name)

    return js_skill

def add_js_skill(jobseeker_id, skill_names):
    """Add a new skill to a job seeker."""
    jobseeker = JobSeeker.query.get(jobseeker_id)

    for skill_name in skill_names:
        jobseeker.skills.append(JobSeekerSkill(skill_name=skill_name))
    
    db.session.commit()
        
def get_js_skill(job_seeker_id):
    """Get a job seeker's skills."""
    return JobSeekerSkill.query.filter(JobSeekerSkill.job_seeker_id == job_seeker_id).all()

def create_js_roletype(job_seeker_id, role_type):
    """Create and return a new job seeker role type."""
    return JobSeekerRoleType(job_seeker_id=job_seeker_id, role_type=role_type)

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
    """Run a jobseeker's search for matching roles."""
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

def rec_candidate_search(location, yoe, yoe_param, skill, role_type, salary, salary_param, remote, sponsorship):
    """Run a recruiter's search for candidates."""
    candidates = db.session.query(JobSeeker)

    if location != "All":
        candidates = candidates.filter(JobSeeker.location == location)

    if yoe != None and yoe_param == "exact":
        candidates = candidates.filter(JobSeeker.yoe == yoe)
    elif yoe != None and yoe_param == "higher":
        candidates = candidates.filter(JobSeeker.yoe >= yoe)
    elif yoe != None and yoe_param == "lower":
        candidates = candidates.filter(JobSeeker.min_yoe <= yoe)

    if skill != "All":
        candidates = candidates.filter(JobSeeker.skills.any(skill_name=skill))

    if role_type != "All":
        candidates = candidates.filter(JobSeeker.role_types.any(role_type=role_type))
    
    if salary != None and salary_param == "exact":
        candidates = candidates.filter(JobSeeker.desired_salary == salary)
    elif salary != None and salary_param == "higher":
        candidates = candidates.filter(JobSeeker.desired_salary >= salary)
    elif salary != None and salary_param == "lower":
        candidates = candidates.filter(JobSeeker.desired_salary <= salary)
    
    if remote == "no":
        candidates = candidates.filter(JobSeeker.remote_only == False)

    if sponsorship == "no":
        candidates = candidates.filter(JobSeeker.sponsorship_provided == False)
    
    return candidates      

def js_request_connect(requestor_id, requested_id, status="pending"):
    """Create and return a connection request from a job seeker."""
    print(f"requestor_id: {requestor_id}, requested_id: {requested_id}, status: {status}")
    return JobSeekerConnectionRequest(requestor_id=requestor_id, requested_id=requested_id, status=status)

def rec_request_connect(requestor_id, requested_id, status="pending"):
    """Create and return a connection request from a recruiter."""

    return RecruiterConnectionRequest(requestor_id=requestor_id, requested_id=requested_id, status=status)

def get_js_request(request_id):
    """Get and return a connection request sent by a jobseeker."""
    return JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.id == request_id).first()

def get_js_request_by_id(requested_id, requestor_id):
    """Find a request sent by a JS to a particular rec."""
    return JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.requested_id == requested_id, JobSeekerConnectionRequest.requestor_id == requestor_id).first()

def get_rec_request_by_id(requested_id, requestor_id):
    """Find a request sent by a JS to a particular rec."""
    return RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.requested_id == requested_id, RecruiterConnectionRequest.requestor_id == requestor_id).first()

def get_rec_request(request_id):
    """Get and return a connection request sent by a recruiter."""
    return RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.id == request_id).first()

def get_all_js_requests(jobseeker_id):
    """Return all requests sent by a jobseeker."""
    return JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.requestor_id == jobseeker_id).all()

def get_all_rec_requests(recruiter_id):
    """Return all requests sent by a jobseeker."""
    return RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.requestor_id == recruiter_id).all()

def get_pending_js_requests(jobseeker_id):
    """Get a jobseeker's pending connection requests they have received."""
    return RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.requested_id == jobseeker_id, RecruiterConnectionRequest.status == "pending").all()

def get_pending_rec_requests(recruiter_id):
    """Get a recruiter's pending connection requests they have received."""
    return JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.requested_id == recruiter_id, JobSeekerConnectionRequest.status == "pending").all()

def get_js_connections(jobseeker_id):
     """Get the recruiters a jobseeker is connected to."""
     received_requests = RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.requested_id == jobseeker_id, RecruiterConnectionRequest.status == "accepted").all()
     sent_requests = JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.requestor_id == jobseeker_id, JobSeekerConnectionRequest.status == "accepted").all()
     connections = []
     for request in received_requests:
         connections.append(request.sender)
     for request in sent_requests:
         connections.append(request.receiver)
     return connections

def get_rec_connections(recruiter_id):
     """Get the jobseekers a recruiter is connected to."""
     received_requests = JobSeekerConnectionRequest.query.filter(JobSeekerConnectionRequest.requested_id == recruiter_id, JobSeekerConnectionRequest.status == "accepted").all()
     sent_requests = RecruiterConnectionRequest.query.filter(RecruiterConnectionRequest.requestor_id == recruiter_id, RecruiterConnectionRequest.status == "accepted").all()
     connections = []
     for request in received_requests:
         connections.append(request.sender)
     for request in sent_requests:
         connections.append(request.receiver)
     return connections
 
def create_js_notification(jobseeker_id, received_request=None, sent_request=None, created_at=None, message=None, read_status=None):
    """Create a new job-seeker notification."""
    new_notification = JobSeekerNotificaton(js_id=jobseeker_id, received_request=received_request,
                                 sent_request=sent_request, created_at=created_at or datetime.utcnow(), 
                                 message=message, read_status=read_status)
    db.session.add(new_notification)
    db.session.commit()
    return new_notification

def create_rec_notification(recruiter_id, received_request=None, sent_request=None, created_at=None, message=None, read_status=None):
    """Create a new job-seeker notification."""
    new_notification = RecruiterNotification(rec_id=recruiter_id, received_request=received_request,
                                 sent_request=sent_request, created_at=created_at or datetime.utcnow(), 
                                 message=message, read_status=read_status)
    db.session.add(new_notification)
    db.session.commit()
    return new_notification

def get_js_notification(notification_id):
    """Get a jobseeker's notification by its id."""
    return JobSeekerNotificaton.query.get(notification_id)

def get_rec_notification(notification_id):
    """Get a recruiter's notification by its id."""
    return RecruiterNotification.query.get(notification_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)