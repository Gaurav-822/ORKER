import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, text, delete, insert
from sqlalchemy.sql.expression import update, select

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure Application
app = Flask(__name__)

# Ensure templates are auto reloded
app.config["TEMPLATES_AUTO_RELOD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Making connection to the database
engine = create_engine("sqlite:///data.db", echo = False, connect_args={"check_same_thread": False})
conn = engine.connect()

# Make Tables:
meta = MetaData()
w_users = Table(
    'w_users', meta,
    Column('w_id', Integer, primary_key = True),
    Column('w_username', Text),
    Column('w_address', Text),
    Column('w_age', Integer),
    Column('w_work', Text),
    Column('w_phone', Text),
    Column('w_hash', Text),
)

c_users = Table(
    'c_users', meta,
    Column('c_id', Integer, primary_key = True),
    Column('c_username', Text),
    Column('c_agency', Text),
    Column('c_work_req', Text),
    Column('c_location', Text),
    Column('c_hash', Text),
)

meta.create_all(engine)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# HOME PAGE ----------------------------------------
@app.route("/")
def home():
    return render_template('index.html')
#---------------------------------------------------

# LOGIN and REGISTER ----------------------------------------------
@app.route("/register_c", methods=["GET", "POST"])
def register_c():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register_c.html")
    username = request.form.get('username')
    agency = request.form.get('agency')
    work_req = request.form.get('work')
    location = request.form.get('location')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    user = text('SELECT c_username, c_id FROM c_users')
    result = conn.execute(user)
    u_l = []
    id = 0
    for row in result:
        u_l.append(row[0])
        id = row[1]
    if username == '' or username in u_l:
        return apology('input is blank or the username already exists.')
    u_l = []
    if password == '' or password != confirmation:
        return apology('Password input is blank or the passwords do not match.')

    ins = c_users.insert().values(c_username = username, c_hash = generate_password_hash(password), c_agency = agency, c_location = location, c_work_req = work_req)
    conn.execute(ins)

    session['user_id'] = id

    return render_template("index.html")


@app.route("/register_w", methods=["GET", "POST"])
def register_w():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register_w.html")
    username = request.form.get('username')
    password = request.form.get('password')

    address = request.form.get('address')
    age = request.form.get('age')
    preffered_work = request.form.get('p_work')
    phone_no = request.form.get('phn_no')

    confirmation = request.form.get('confirmation')

    user = text('SELECT w_username, w_id FROM w_users')
    result = conn.execute(user)
    u_l = []
    id = 0
    for row in result:
        u_l.append(row[0])
        id = row[1]
    if username == '' or username in u_l:
        return apology('input is blank or the username already exists.')
    u_l = []
    if password == '' or password != confirmation:
        return apology('Password input is blank or the passwords do not match.')

    ins = w_users.insert().values(w_username = username, w_hash = generate_password_hash(password), w_address = address, w_age = age, w_work = preffered_work, w_phone = phone_no)
    conn.execute(ins)

    session['user_id'] = id

    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # Query database for username
        #Can make better
        user = text('SELECT username, hash, id FROM users')
        result = conn.execute(user)
        for row in result:
            if row[0] == request.form.get("username"):
                if check_password_hash(row[1], request.form.get("password")):
                    session['user_id'] = row[2]
                    return render_template("index.html")
        
        return apology('Sorry We cannot find you right now')
    
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
# --------------------------------------------------------------
