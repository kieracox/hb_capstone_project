from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db 
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined