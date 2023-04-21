from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db 
import crud
import os
import cloudinary.uploader

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
    #TODO: finish this function to take in form inputs
    return redirect("/search_results")
    
@app.route("/search_results")
def show_results():
    """Display a user's search results."""
    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        return render_template("js_search_results.html", user=user)
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_search_results.html", user=user)

    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)