#!/usr/bin/env python

"""server.py -- the main flask server module"""

import dataset
import json
import random
import time
import re
import os
import hashlib

from base64 import b64decode
from functools import wraps

from flask import Flask
from flask import abort
from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__, static_folder='static', static_url_path='')

db = None
lang = None
config = None
user_re = re.compile("^[a-zA-Z0-9-_. &']+$")

def is_valid_username(u):
    if(user_re.match(u)):
        return True
    return False

def login_required(f):
    """Ensures that an user is logged in"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('error', msg='login_required'))
        return f(*args, **kwargs)
    return decorated_function


def during_ctf(f):
    """Ensures that actions can only be done during the CTF"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        cur_time = int(time.time())
        if cur_time <= config['start'] or cur_time >= config['stop']:
            return redirect(url_for('error', msg='only_during_ctf'))
        return f(*args, **kwargs)
    return decorated_function

def notended(f):
    """Ensures that actions can only be done until the CTF is over"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        cur_time = int(time.time())
        if cur_time >= config['stop']:
            return redirect(url_for('error', msg='ctf_over'))
        return f(*args, **kwargs)
    return decorated_function

def get_user():
    """Looks up the current user in the database"""

    login = 'user_id' in session    
    if login:
        return (True, db['users'].find_one(id=session['user_id']))

    return (False, None)

def get_task(category, score):
    """Finds a task with a given category and score"""

    task = db.query('''select t.* from tasks t, categories c, cat_task ct 
        where t.id = ct.task_id and c.id = ct.cat_id 
        and t.score=:score and lower(c.short_name)=:cat''',
        score=score, cat=category)
    return list(task)[0]

def get_flags():
    """Returns the flags of the current user"""

    flags = db.query('''select f.task_id from flags f 
        where f.user_id = :user_id''',
        user_id=session['user_id'])
    return [f['task_id'] for f in list(flags)]

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(400)

def some_random_string():
    return hashlib.sha256(os.urandom(16)).hexdigest()

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']

@app.context_processor
def inject_ctftime():
    start = time.strftime("%Y-%m-%d, %H:%M:%S (%Z)",time.localtime(config['start']))
    stop = time.strftime("%Y-%m-%d, %H:%M:%S (%Z)",time.localtime(config['stop']))
    return dict(ctf_start=start, ctf_stop=stop)

@app.route('/error/<msg>')    
def error(msg):
    """Displays an error message"""

    if msg in lang['error']:
        message = lang['error'][msg]
    else:
        message = lang['error']['unknown']

    login, user = get_user()

    render = render_template('frame.html', lang=lang, page='error.html', 
        message=message, login=login, user=user)
    return make_response(render)

def session_login(username):
    """Initializes the session with the current user's id"""
    user = db['users'].find_one(username=username)
    session['user_id'] = user['id']

@app.route('/login', methods = ['POST'])
def login():
    """Attempts to log the user in"""

    from werkzeug.security import check_password_hash

    username = request.form['user']
    password = request.form['password']

    if not is_valid_username(username):
        return redirect('/error/invalid_credentials')

    user = db['users'].find_one(username=username)
    if user is None:
        return redirect('/error/invalid_credentials')

    if check_password_hash(user['password'], password):
        session_login(username)
        return redirect('/scoreboard')

    return redirect('/error/invalid_credentials')

@app.route('/register')
@notended
def register():
    """Displays the register form"""

    # Render template
    render = render_template('frame.html', lang=lang, 
        page='register.html', login=False)
    return make_response(render) 

@app.route('/register/submit', methods = ['POST'])
@notended
def register_submit():
    """Attempts to register a new user"""

    from werkzeug.security import generate_password_hash

    username = request.form['user']
    password = request.form['password']

    if not username or not is_valid_username(username):
        return redirect('/error/empty_user')

    if len(username) > 25:
	return redirect('/error/empty_user')

    user_found = db['users'].find_one(username=username)
    if user_found:
        return redirect('/error/already_registered')
            
    new_user = dict(hidden=0, username=username, 
        password=generate_password_hash(password))
    db['users'].insert(new_user)

    # Set up the user id for this session
    session_login(username)

    return redirect('/scoreboard')

@app.route('/tasks')
@login_required
@during_ctf
def tasks():
    """Displays all the tasks in a grid"""

    login, user = get_user()
    flags = get_flags()

    categories = db['categories']

    tasks = db.query('''select c.id as cat_id, t.id as id, c.short_name, 
        t.score, t.row from categories c, tasks t, cat_task c_t 
        where c.id = c_t.cat_id and t.id = c_t.task_id''')
    tasks = list(tasks)

    grid = []
    # Find the max row number
    max_row = max(t['row'] for t in tasks)

    for row in range(max_row + 1):

        row_tasks = []
        for cat in categories:

            # Find the task with the correct row
            for task in tasks:
                if task['row'] == row and task['cat_id'] == cat['id']:
                    break
            else:
                task = None

            row_tasks.append(task)

        grid.append(row_tasks)

    # Render template
    render = render_template('frame.html', lang=lang, page='tasks.html', 
        login=login, user=user, categories=categories, grid=grid, 
        flags=flags)
    return make_response(render) 

@app.route('/tasks/<category>/<score>')
@login_required
@during_ctf
def task(category, score):
    """Displays a task with a given category and score"""

    login, user = get_user()

    task = get_task(category, score)
    if not task:
        return redirect('/error/task_not_found')

    flags = get_flags()
    task_done = task['id'] in flags

    solutions = db['flags'].find(task_id=task['id'])
    solutions = len(list(solutions))

    # Render template
    render = render_template('frame.html', lang=lang, page='task.html', 
        task_done=task_done, login=login, solutions=solutions,
        user=user, category=category, task=task, score=score)
    return make_response(render)

@app.route('/task/submit', methods = ['POST'])
@during_ctf
@login_required
def submit():
    """Handles the submission of flags"""

    category = request.form['category']
    score = request.form['score']
    flag = request.form['flag']

    login, user = get_user()

    task = get_task(category, score)
    flags = get_flags()
    task_done = task['id'] in flags

    result = {'success': False, 'csrf': generate_csrf_token() }

    if not task_done and task['flag'] == b64decode(flag):

        timestamp = int(time.time() * 1000)

        # Insert flag
        new_flag = dict(task_id=task['id'], user_id=session['user_id'], 
            score=score, timestamp=timestamp)
        db['flags'].insert(new_flag)

        result['success'] = True

    return jsonify(result)

@app.route('/scoreboard')
def scoreboard():
    """Displays the scoreboard"""

    login, user = get_user()
    scores = db.query('''select u.username, ifnull(sum(f.score), 0) as score, 
        max(timestamp) as last_submit from users u left join flags f 
        on u.id = f.user_id where u.hidden = 0 group by u.username 
        order by score desc, last_submit asc, u.username asc''')

    scores = list(scores)

    # Render template
    render = render_template('frame.html', lang=lang, page='scoreboard.html', 
        login=login, user=user, scores=scores)
    return make_response(render) 

@app.route("/scoreboard.json")
def scoreboard_json():
    """Displays data for ctftime.org in json format"""
    scores = db.query('''select u.username as team, ifnull(sum(f.score), 0) as score, ifnull(max(timestamp), 0) as lastAccept from users
                        u left join flags f on u.id = f.user_id where u.hidden = 0 group by u.username
                        order by score desc, lastAccept asc''')
    scores = list(scores)
    data = map(dict,scores)	
    return jsonify({'standings':data})

@app.route('/rules')
def rules():
    """Displays the rules menu"""

    login, user = get_user()
    # Render template
    render = render_template('frame.html', lang=lang, page='rules.html', 
        login=login, user=user)
    return make_response(render) 

@app.route('/logout')
@login_required
def logout():
    """Logs the current user out"""

    del session['user_id']
    return redirect('/')

@app.route('/')
def index():
    """Displays the main page"""

    login, user = get_user()

    # Render template
    render = render_template('frame.html', lang=lang, 
        page='main.html', login=login, user=user)
    return make_response(render)


app.jinja_env.globals['csrf_token'] = generate_csrf_token 

if __name__ == '__main__':
    """Initializes the database and sets up the language"""

    # Load config
    config_str = open('config.json', 'rb').read()
    config = json.loads(config_str)

    app.secret_key = config['secret_key']

    # Load language
    lang_str = open(config['language_file'], 'rb').read()
    lang = json.loads(lang_str)

    # Only a single language is supported for now
    lang = lang[config['language']]

    # Connect to database
    db = dataset.connect(config['db'])

    # Setup the flags table at first execution
    if 'flags' not in db.tables:
        db.query('''create table flags (
            task_id INTEGER, 
            user_id INTEGER, 
            score INTEGER, 
            timestamp BIGINT, 
            PRIMARY KEY (task_id, user_id))''')

    # Start web server
    app.run(host=config['host'], port=config['port'], 
        debug=config['debug'], threaded=True)

