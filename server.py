from flask import (Flask, render_template, request, flash, session, redirect, jsonify, url_for)
from model import connect_to_db, db 
import crud
import os
import cloudinary.uploader
from urllib.parse import urlencode

from jinja2 import StrictUndefined

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dmp5wclf8"


app = Flask(__name__, static_folder='static')
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
        user_id = user.id
        pending_requests = crud.get_pending_js_requests(user_id)
        connections = crud.get_js_connections(user_id)
        return render_template("js_dashboard.html", user=user, requests=pending_requests, connections=connections)
    else:
        user = crud.get_recruiter_by_email(user_email)
        user_id = user.id
        pending_requests = crud.get_pending_rec_requests(user_id)
        connections = crud.get_rec_connections(user_id)
        return render_template("recruiter_dashboard.html", user=user, requests=pending_requests, connections=connections)


@app.route('/logout', methods=['POST'])
def logout():
    """Logs the user out."""
    session.pop('user_email', None)
    session.pop('user_type', None)
    flash('You have been logged out.')
    return redirect("/")

@app.route('/mark_notification_read/<int:notification_id>')
def mark_notification_read(notification_id):
    user_type = session.get("user_type")
    if user_type == "job_seeker":
        notification = crud.get_js_notification(notification_id)
        if notification:
            notification.read_status = True
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notification not found.'})
    else:
        notification = crud.get_rec_notification(notification_id)
        if notification:
            notification.read_status = True
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Notification not found.'})
        
@app.route("/notifications")
def show_notifications():
    """Display a user's notifications."""
    user_type = session.get("user_type")
    if user_type == "job_seeker":
        user = crud.get_js_by_email(session["user_email"])
        return render_template("notifications.html", user=user)
    else:
        user = crud.get_recruiter_by_email(session["user_email"])
        return render_template("notifications.html", user=user)

@app.route("/settings")
def show_settings():
    """Display the user settings page."""
    user_type = session.get("user_type")
    if user_type == "job_seeker":
        user = crud.get_js_by_email(session["user_email"])
        return render_template("settings.html", user=user)
    else:
        user = crud.get_recruiter_by_email(session["user_email"])
        return render_template("settings.html", user=user)

@app.route("/set_notifications", methods=["GET", "POST"])
def update_notifications():
    """Update a user's notifications preferences."""
    user_type = session.get("user_type")
    if user_type == "job_seeker":
        user = crud.get_js_by_email(session["user_email"])
    else:
        user = crud.get_recruiter_by_email(session["user_email"])
    if request.method == 'POST':
        if request.form.get('enable_notifications'):
            user.notifications_enabled = True
            db.session.commit()
            flash('Notifications have been enabled.')
        elif request.form.get('disable_notifications'):
            user.notifications_enabled = False
            db.session.commit()
            flash('Notifications have been disabled.')
    return render_template('settings.html', user=user)

@app.route("/change_password", methods=["POST"])
def change_password():
    """Change a user's password."""
    user_type = session.get("user_type")
    if user_type == "job_seeker":
        user = crud.get_js_by_email(session["user_email"])
    else:
        user = crud.get_recruiter_by_email(session["user_email"]) 

    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")

    if current_password != user.password:
        flash("Incorrect current password. Please try again.")
    else:
        user.password = new_password
        db.session.commit()
        flash("Your password has been updated.")    

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
        
        sponsorship_provided_str = request.form.get('sponsorship_provided')
        if sponsorship_provided_str:
            sponsorship_provided = bool(sponsorship_provided_str == 'True') 
        else:
            sponsorship_provided = None 

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
    result = cloudinary.uploader.upload(file=resume, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
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
    result = cloudinary.uploader.upload(file=jd, api_key=CLOUDINARY_KEY, api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME)
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


@app.route("/search", methods=['GET', 'POST'])
def run_search():
    """Run a new user search."""
    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        role_type = request.form.get("role_type")
        level = request.form.get("level")
        user = crud.get_js_by_email(user_email)

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
        
        search_params = {
            "role_type": role_type,
            "level": level,
            "location": location,
            "yoe": yoe,
            "yoe_param": yoe_param,
            "salary": salary,
            "salary_param": salary_param,
            "remote": remote,
            "sponsorship": sponsorship
        }

        session["search_params"] = search_params
        
        
        return redirect(url_for("js_search_results", **search_params))
    else:
        user = crud.get_recruiter_by_email(user_email)
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
        
        search_params = {
            "location": location,
            "yoe": yoe,
            "yoe_param": yoe_param,
            "skill": skill,
            "role_type": role_type,
            "salary": salary,
            "salary_param": salary_param,
            "remote": remote,
            "sponsorship": sponsorship
        }

        session["search_params"] = search_params
        return redirect(url_for("recruiter_search_results", **search_params))


@app.route("/search/results/js", methods=["GET"])
def js_search_results():
    user = crud.get_js_by_email(session["user_email"])

    role_type = request.args.get("role_type")
    level = request.args.get("level")
    location = request.args.get("location")
    yoe = request.args.get("yoe")
    yoe_param = request.args.get("yoe_param")
    salary = request.args.get("salary")
    salary_param = request.args.get("salary_param")
    remote = request.args.get("remote")
    sponsorship = request.args.get("sponsorship")
    
    roles = crud.js_role_search(role_type, level, location,
                                yoe, yoe_param, salary,
                                salary_param, remote, sponsorship).all()

    existing_connections = crud.get_js_connections(user.id)
    
    return render_template("js_search_results.html", roles=roles, user=user, connections=existing_connections, 
                           search_params=request.args)


@app.route("/search/results/rec", methods=["GET"])
def recruiter_search_results():
    user = crud.get_recruiter_by_email(session["user_email"])
    
    location = request.args.get("location")
    yoe = request.args.get("yoe")
    yoe_param = request.args.get("yoe_param")
    skill = request.args.get("skill")
    role_type = request.args.get("role_type")
    salary = request.args.get("salary")
    salary_param = request.args.get("salary_param")
    remote = request.args.get("remote")
    sponsorship = request.args.get("sponsorship")
    
    candidates = crud.rec_candidate_search(location, yoe, 
                                           yoe_param, skill, role_type, 
                                           salary, salary_param, remote, sponsorship)
    
    existing_connections = crud.get_rec_connections(user.id)
    
    return render_template("recruiter_search_results.html", candidates=candidates, user=user, connections=existing_connections, 
                           search_params=request.args)


@app.route("/send_connect", methods=["POST"])
def send_request():
    """Send a connection request."""
    user_type = session.get("user_type")
    requestor_id = request.form.get("requestor_id")
    requested_id = request.form.get("requested_id")
    status = "pending"

    if user_type == "job_seeker":
        user = crud.get_js_by_email(session["user_email"])
        existing_request = crud.get_js_request_by_id(requested_id, requestor_id)
        if existing_request and existing_request.status == "pending":
            response_data = {"success": False}
            return jsonify(response_data)
        else:
            new_request = crud.js_request_connect(requestor_id, requested_id, status)
            db.session.add(new_request)
            db.session.commit()
            
            notification = crud.create_rec_notification(recruiter_id=requested_id, received_request=new_request.id,
                                                         message=f"{user.fname} {user.lname} wants to connect with you!", read_status=False)
            db.session.add(notification)
            db.session.commit()

            response_data = {"success": True}
            return jsonify(response_data)
        
    else:
        user = crud.get_recruiter_by_email(session["user_email"])
        existing_request = crud.get_rec_request_by_id(requested_id, requestor_id)
        if existing_request and existing_request.status == "pending":
            response_data = {"success": False}
            return jsonify(response_data)
        else:
            new_request = crud.rec_request_connect(requestor_id, requested_id, status)
            db.session.add(new_request)
            db.session.commit()

            notification = crud.create_js_notification(jobseeker_id=requested_id, received_request=new_request.id,
                                                         message=f"{user.fname} {user.lname} wants to connect with you!", read_status=False)
            db.session.add(notification)
            db.session.commit()

            response_data = {"success": True}
            return jsonify(response_data)
    
    
@app.route("/accept_request", methods=["POST"])
def accept_connection():
    """Accept a connection request sent to the user."""
    user_type = session.get("user_type")
    request_id = request.form.get("request_id")
    if request_id:
        if user_type == "job_seeker":
            req = crud.get_rec_request(request_id)
            req.status = "accepted"
            print(req.status)
            db.session.commit()
            flash("Request accepted!")
            return redirect("/user_dashboard")
        else:
            req = crud.get_js_request(request_id)
            req.status = "accepted"
            print(req.status)
            db.session.commit()
            flash("Request accepted!")
            return redirect("/user_dashboard")
    else:
      flash("Invalid request ID.")
      return redirect("/user_dashboard")  
    

@app.route("/reject_request", methods=["POST"])
def reject_connection():
     """Reject a connection request sent to the user."""
     user_type = session.get("user_type")
     request_id = request.form.get("request_id")
     
     if user_type == "job_seeker":
        req = crud.get_rec_request(request_id)
        req.status = "rejected"
        db.session.commit()
        flash("Request rejected.")
        return redirect("/user_dashboard")
     else:
        req = crud.get_js_request(request_id)
        req.status = "rejected"
        db.session.commit()
        flash("Request rejected.")
        return redirect("/user_dashboard")

        




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)