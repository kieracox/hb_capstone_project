"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb jobs")
os.system("createdb jobs")

model.connect_to_db(server.app)
model.db.create_all()

role_types = ['Backend', 'Frontend', 'Fullstack', 'Devops', 'Security', 'Data', 'Machine Learning', 'Management', 'Mobile', 'QA']

skills = ['Python', 'Javascript', 'React', 'Flask', 'AWS', 'Kubernetes', 'Agile', 'SQL', 'Swift', 'Selenium']

levels = ['Entry Level', 'Mid Level', 'Senior', 'Staff', 'Manager']

locations = ['San Francisco', 'Seattle', 'New York', '']


with open('data/roles.json') as f:
    roles_data = json.loads(f.read())
    roles_in_db = []
    
    for n in range(10):
        email = f'recruiter{n}@test.com'
        password = 'test'
        fname = f'Recruiter{n}'
        lname = f'Test{n}'
        company = 'Hackbright'
        linkedin = 'linkedin.com'

        db_recruiter = crud.create_recruiter(email, password, fname, lname, company, linkedin)
        model.db.session.add(db_recruiter)

    for role in roles_data:
        recruiter_id = db_recruiter.id
        name = role["name"]
        role_type = role["role_type"]
        min_yoe = role["min_yoe"]
        level = role["level"]
        location = role["location"]
        remote = role["remote"]
        sponsorship_provided = role["sponsorship_provided"]
        salary = role["salary"]

        db_role = crud.create_role(recruiter_id, name, role_type, min_yoe, level, location, salary, remote, sponsorship_provided)
        roles_in_db.append(db_role)
    
    model.db.session.add_all(roles_in_db)
    model.db.session.commit()

with open('data/role_skills.json') as g:
    skills_data = json.loads(g.read())
    skills_in_db = []

    for skill in skills_data:
        role_id = skill["role_id"]
        skill_name = skill["skill_name"]

        db_skill = crud.create_role_skill(role_id, skill_name)
        skills_in_db.append(db_skill)
    
    model.db.session.add_all(skills_in_db)
    model.db.session.commit()

for n in range(10):
    email = f'candidate{n}@test.com'
    password = 'test'
    fname = f'Candidate{n}'
    lname = f'Test{n}'
    linkedin = 'linkedin.com'
    github = 'github.com'
    location = choice(locations)
    yoe = randint(1, 20)
    remote_only = choice([True, False])
    sponsorship_needed = choice([True, False])
    desired_salary = choice([None, 100000, 150000, 200000])

    db_job_seeker = crud.create_job_seeker(email, password, fname, lname,  
                                           linkedin, github, location, yoe, desired_salary, 
                                           remote_only, sponsorship_needed,)
    model.db.session.add(db_job_seeker)

    for _ in range(10):
        random_skill = choice(skills)
        js_id = db_job_seeker.id
        js_skill = crud.create_js_skill(js_id, random_skill)
        model.db.session.add(js_skill)


    model.db.session.commit()
    

