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
users = Table(
    'users', meta,
    Column('id', Integer, primary_key = True),
    Column('username', Text),
    Column('hash', Text),
    Column('agency', Text),
    Column('location', Text),
    Column('work', Text),
    Column('phn_no', Text),
    Column('email', Text),
    Column('age', Integer),
    Column('worker', Integer),
)

notification = Table(
    'notification', meta,
    Column('c_id', Integer),
    Column('message', Text),
)


meta.create_all(engine)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


check = 0   #If worker then check = 1, elif if contractor check = 2


# HOME PAGE ----------------------------------------
@app.route("/")
def home():

    '''
    s2 = users.select().where(users.c.id == session['user_id'])
    result = conn.execute(s2)
    worker = 2
    for i in result:
        worker = i[9]
    
    if worker == 0:
        return render_template('index.html', worker = 0)
    elif worker == 1:
        return render_template('index.html', worker = 1)
    else:
        return render_template('index.html', worker = 2)
    
'''
    try:
        s5 = users.select().where(users.c.id == session['user_id'])
        res5 = conn.execute(s5)
        for i in res5:
            location = i[4]
            worker = i[9]
            # location = res5[0][4]
            # worker = res5[0][9]
            s4 = users.select()
            res4 = conn.execute(s4)
            works = []
            c_id = []
            phn_no = []
            for i in res4:
                if i[4].lower() == location.lower() and i[9] == 0:
                    if i[0] != session['user_id']:
                        c_id.append(i[1])
                        works.append(i[5])
                        phn_no.append(i[6])
            works.reverse()
            c_id.reverse()
            phn_no.reverse()
            loop = len(c_id)
            return render_template("index.html",loop = loop, worker = worker, c_id = c_id, noti = works, phn_no = phn_no)
    except:
        return render_template("index.html", worker = 2)
#---------------------------------------------------

'''
@app.route("/trick", methods=["POST", "GET"])
@login_required
def trick():
    try:
        s5 = users.select().where(users.c.id == session['user_id'])
        res5 = conn.execute(s5)
        for i in res5:
            location = i[4]
            worker = i[9]
            # location = res5[0][4]
            # worker = res5[0][9]
            s4 = users.select()
            res4 = conn.execute(s4)
            works = []
            c_id = []
            phn_no = []
            for i in res4:
                if i[4].lower() == location.lower() and i[9] == 0:
                    if i[0] != session['user_id']:
                        c_id.append(i[1])
                        works.append(i[5])
                        phn_no.append(i[6])
            works.reverse()
            c_id.reverse()
            phn_no.reverse()
            loop = len(c_id)
            return render_template("index.html",loop = loop, worker = worker, c_id = c_id, noti = works, phn_no = phn_no)
    except:
        return render_template("index.html", worker = 2)
'''

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
    email = request.form.get('email')
    phn_no = request.form.get('phn_no')
    location = request.form.get('location')
    password = request.form.get('password')
    confirmation = request.form.get('confirmation')

    user = text('SELECT username, id FROM users GROUP BY id')
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
    
    n_msg = 'Job is available for the work : ' + work_req
    ins_n = notification.insert().values(c_id = id + 1, message = n_msg)
    conn.execute(ins_n)

    ins = users.insert().values(username = username, hash = generate_password_hash(password), agency = agency, location = location, work = work_req, phn_no = phn_no, email = email, worker = 0)
    conn.execute(ins)

    session['user_id'] = id

    return render_template("index.html", worker = 0)


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

    user = text('SELECT username, id FROM users')
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
    
    ins = users.insert().values(username = username, hash = generate_password_hash(password), location = address, age = age, work = preffered_work, phn_no = phone_no, worker = 1)
    conn.execute(ins)

    session['user_id'] = id

    # return render_template("/trick")
    try:
        s5 = users.select().where(users.c.id == session['user_id'])
        res5 = conn.execute(s5)
        for i in res5:
            location = i[4]
            worker = i[9]
            # location = res5[0][4]
            # worker = res5[0][9]
            s4 = users.select()
            res4 = conn.execute(s4)
            works = []
            c_id = []
            phn_no = []
            for i in res4:
                if i[4].lower() == location.lower() and i[9] == 0:
                    if i[0] != session['user_id']:
                        c_id.append(i[1])
                        works.append(i[5])
                        phn_no.append(i[6])
            works.reverse()
            c_id.reverse()
            phn_no.reverse()
            loop = len(c_id)
            return render_template("index.html",loop = loop, worker = worker, c_id = c_id, noti = works, phn_no = phn_no)
    except:
        return render_template("index.html", worker = 2)


@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
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

                    s5 = users.select().where(users.c.id == row[2])
                    res5 = conn.execute(s5)
                    for i in res5:
                        location = i[4]
                        worker = i[9]
                    # location = res5[0][4]
                    # worker = res5[0][9]

                    s4 = users.select()
                    res4 = conn.execute(s4)
                    works = []
                    c_id = []
                    phn_no = []
                    for i in res4:
                        if i[4].lower() == location.lower() and i[9] == 0:
                            if i[0] != row[2]:
                                c_id.append(i[1])
                                works.append(i[5])
                                phn_no.append(i[6])
                    works.reverse()
                    c_id.reverse()
                    phn_no.reverse()
                    loop = len(c_id)
                    return render_template("index.html",loop = loop, worker = worker, c_id = c_id, noti = works, phn_no = phn_no)
        
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
