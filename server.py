from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db 
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/users', methods=['POST'])
def register_recruiter():
    """Create a new recruiter account."""
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    if user_type == "recruiter":
        user = crud.get_recruiter_by_email(email)
    else:
        user = crud.get_js_by_email(email)

    if user:
        flash("An account already exists with that email. Please enter another email.")
    
    elif user_type == "recruiter":
        recruiter = crud.create_recruiter(email, password)
        db.session.add(recruiter)
        db.session.add(recruiter)
        db.session.commit()
        flash("Account created! Please log in.")
    
    else: 
        job_seeker = crud.create_job_seeker( email, password)
        db.session.add(job_seeker)
        db.session.add(job_seeker)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/") #change to redirect to user dashboard


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
    #possibly need to add /<id>
    return redirect("/")

@app.route("/user_dashboard")
def show_dashboard():
    """Display a user dashboard"""
    user_email = session.get("user_email")
    user_type = session.get("user_type")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        return render_template("jobseeker_dashboard.html")
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_dashboard.html", user=user)
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)