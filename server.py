from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db 
import crud
import os
import cloudinary.uploader
from urllib.parse import urlencode

from jinja2 import StrictUndefined

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dmp5wclf8"


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/register', methods=['POST'])
def register_user():
    """Create a new user account."""
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    if user_type == "recruiter":
        user = crud.get_recruiter_by_email(email)
    else:
        user = crud.get_js_by_email(email)

    if user:
        flash("An account already exists with that email. Please enter another email.")
        return redirect("/")
    
    elif user_type == "recruiter":
        recruiter = crud.create_recruiter(email, password)
        db.session.add(recruiter)
        db.session.commit()
        session["user_email"] = recruiter.email
        session["user_type"] = user_type
        return redirect("/user_dashboard")
    
    else: 
        job_seeker = crud.create_job_seeker(email, password)
        db.session.add(job_seeker)
        db.session.commit()
        session["user_email"] = job_seeker.email
        session["user_type"] = user_type
        return redirect("/user_dashboard")
    
@app.route("/login", methods=["POST"])
def log_in_user():
    """Log in a user."""
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(email)
    else:
        user = crud.get_recruiter_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password you entered was incorrect. Please try again.")
        return redirect("/")
    else:
        session["user_email"] = user.email
        session["user_type"] = user_type
        flash(f"Welcome back, {user.fname}!")
    return redirect("/user_dashboard")

@app.route("/user_dashboard")
def show_dashboard():
    """Display a user dashboard."""
    user_email = session.get("user_email")
    user_type = session.get("user_type")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        return render_template("js_dashboard.html", user=user)
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_dashboard.html", user=user)

@app.route('/logout', methods=['POST'])
def logout():
    """Logs the user out."""
    session.pop('user_email', None)
    session.pop('user_type', None)
    flash('You have been logged out.')
    return redirect("/")
    
@app.route("/user_profile")
def show_profile():
    """Display a user's profile page."""
    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        user_id = user.id
        skills = crud.get_js_skill(user_id)
        roletypes = crud.get_js_roletype(user_id)
        return render_template("js_profile.html", user=user, skills=skills, roletypes=roletypes)
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_profile.html", user=user)

@app.route("/update_js_profile", methods=['POST'])
def update_js_profile():
    """Update a jobseeker's profile."""
    user_email = session.get("user_email")
    user = crud.get_js_by_email(user_email)
    user_id = user.id

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    linkedin= request.form.get('linkedin')
    github = request.form.get('github')
    location = request.form.get('location')
    
  
    yoe_str = request.form.get('yoe')
    if yoe_str:
        yoe = int(yoe_str)
    else:
        yoe = None
    
    desired_salary_str = request.form.get('desired_salary')
    if desired_salary_str:
        desired_salary = int(desired_salary_str)
    else:
        desired_salary = None

    remote_only_str = request.form.get("remote_only")
    if remote_only_str:
        remote_only = bool(remote_only_str == 'True') 
    else:
        remote_only = None
    
    sponsorship_needed_str = request.form.get('sponsorship_needed')
    if sponsorship_needed_str:
        sponsorship_needed = bool(sponsorship_needed_str == 'True') 
    else:
        sponsorship_needed = None 

    crud.edit_js_profile(user_id, fname, lname, linkedin, 
                         github, location, yoe, desired_salary, 
                         remote_only, sponsorship_needed)
    
    skill = request.form.get("skill")
    js_skill = crud.get_js_skill(user_id)
    if js_skill:
        js_skill[0].skill_name = skill
    else:
        js_skill = crud.create_js_skill(user_id, skill)
        db.session.add(js_skill)

    roletype = request.form.get("role_type")
    js_roletype = crud.get_js_roletype(user_id)
    if js_roletype:
        js_roletype[0].role_type = roletype
    else:
        js_roletype = crud.create_js_roletype(user_id, roletype)
        db.session.add(js_roletype)

    db.session.commit()
    return redirect("/user_profile")

@app.route("/update_rec_profile", methods=["POST"])
def update_rec_profile():
    """Update a recruiter's profile."""
    user_email = session.get("user_email")
    user = crud.get_recruiter_by_email(user_email)
    user_id = user.id

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    linkedin = request.form.get('linkedin')
    company = request.form.get('company')


    for role in user.roles:

        role_id = role.id

        role_name = request.form.get('role_name')
        location = request.form.get('location')
        role_type = request.form.get("role_type")
        level = request.form.get('level')

        print('sever.py 197',role_name)
        print('server.py 198',location)
    
        yoe_str = request.form.get('yoe')
        if yoe_str:
            yoe = int(yoe_str)
        else:
            yoe = None
    
        min_salary_str = request.form.get('min_salary')
        if min_salary_str:
            min_salary = int(min_salary_str)
        else:
            min_salary = None

        remote_str = request.form.get("remote")
        if remote_str:
            remote = bool(remote_str == 'True') 
        else:
            remote = None
        
        print('server.py 218', remote)
        
        sponsorship_provided_str = request.form.get('sponsorship_provided')
        if sponsorship_provided_str:
            sponsorship_provided = bool(sponsorship_provided_str == 'True') 
        else:
            sponsorship_provided = None 

        print('server.py 226',sponsorship_provided)

    crud.edit_rec_profile(user_id, fname, lname, company, linkedin)
    crud.edit_role(role_id, role_name, role_type, location, yoe, level, min_salary, 
                         remote, sponsorship_provided)
    
    skill = request.form.get("skill")
    role_skill = crud.get_role_skill(role_id)
    if role_skill:
        role_skill[0].skill_name = skill
    else:
        role_skill = crud.create_role_skill(role_id, skill)
        db.session.add(role_skill)
    
    db.session.commit()
    return redirect("/user_profile")

@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    """Upload a jobseeker's resume."""
    resume = request.files['resume']
    result = cloudinary.uploader.upload(resume, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    resume_url = result['secure_url']

    user_email = session.get("user_email")
    user = crud.get_js_by_email(user_email)
    user.resume_url = resume_url
    db.session.commit()
    return redirect("/user_profile")

@app.route("/upload_jd", methods=['POST'])
def upload_jd():
    """Upload a recruiter's job description."""
    jd = request.files['jd']
    result = cloudinary.uploader.upload(jd, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
    jd_url = result['secure_url']

    user_email = session.get("user_email")
    user = crud.get_recruiter_by_email(user_email)
    for role in user.roles:
        if role.jd_url == "":
            role.jd_url = jd_url
    db.session.commit()
    return redirect("/user_profile")

@app.route("/new_search")
def show_search():
    """Display the search page."""
    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        return render_template("js_search.html", user=user)
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_search.html", user=user)
    
@app.route("/search", methods=['POST'])
def run_search():
    """Run a new user search."""

    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        role_type = request.form.get("role_type")
        level = request.form.get("level")

        location = request.form.get("location")
        if location == None or location == "":
            location = "All"

        yoe = request.form.get("yoe")
        yoe_param = request.form.get("yoe_param")
        salary = request.form.get("salary")
        salary_param = request.form.get("salary_param")
        remote = request.form.get("remote")
        sponsorship = request.form.get("sponsorship")


        roles = crud.js_role_search(role_type, level, location,
                                    yoe, yoe_param, salary,
                                    salary_param, remote, sponsorship).all()
        
        
        return render_template("js_search_results.html", roles=roles)
    else:
        
        location = request.form.get("location")
        if location == None or location == "":
            location = "All"

        yoe = request.form.get("yoe")
        yoe_param = request.form.get("yoe_param")
        skill = request.form.get("skill")
        role_type = request.form.get("role_type")
        salary = request.form.get("salary")
        salary_param = request.form.get("salary_param")
        remote = request.form.get("remote")
        sponsorship = request.form.get("sponsorship")

        candidates = crud.rec_candidate_search(location, yoe, 
                                               yoe_param, skill, role_type, 
                                               salary, salary_param, remote, sponsorship)
        return render_template("recruiter_search_results.html", candidates=candidates)

        




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)