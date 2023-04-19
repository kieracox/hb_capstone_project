from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db 
import crud

from jinja2 import StrictUndefined

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
    
    elif user_type == "recruiter":
        recruiter = crud.create_recruiter(email, password)
        db.session.add(recruiter)
        db.session.commit()
        session["user_email"] = user.email
        session["user_type"] = user_type
        return redirect("/user_dashboard")
    
    else: 
        job_seeker = crud.create_job_seeker( email, password)
        db.session.add(job_seeker)
        db.session.commit()
        session["user_email"] = user.email
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
    
@app.route("/user_profile")
def show_profile():
    """Display a user's profile page."""
    user_type = session.get("user_type")
    user_email = session.get("user_email")

    if user_type == "job_seeker":
        user = crud.get_js_by_email(user_email)
        return render_template("js_profile.html", user=user)
    else:
        user = crud.get_recruiter_by_email(user_email)
        return render_template("recruiter_profile.html", user=user)

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