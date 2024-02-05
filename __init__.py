from flask import Flask, render_template, url_for, redirect, session, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from .configuration_key import SECRET_KEY
from datetime import datetime

import json

import sqlite3

app = Flask(__name__)

ALLOWED_IMAGE_NAMES = {'great5.png', 'happy4.png', 'neutral3.png', 'upset2.png', 'mad1.png'} # from static pngs

'''
Database
'''
app.secret_key = SECRET_KEY

def get_db():
    db = getattr(g, '_database', None) # The g object is often used to store variables that should be accessible throughout the request-response cycle.
    if db is None:
        db = g._database = sqlite3.connect('test-database.db') # establish connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM test_mood_table')
        all_data = cursor.fetchall()
        #all_data = [str(val[0] for val in all_data)]
    return all_data

def get_db_register():
    db = getattr(g, '_database', None) # The g object is often used to store variables that should be accessible throughout the request-response cycle.
    if db is None:
        db = g._database = sqlite3.connect('test-database.db') # establish connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM test_user_credential_table')
        all_data_register = cursor.fetchall()
        #all_data = [str(val[0] for val in all_data)]
    return all_data_register

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

'''
HTML Routes
'''
@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/track')
def track():
    data = get_db()
    return render_template('track.html', all_data=data)

@app.route('/track-welcome')
def track_welcome():
    return render_template('track-welcome.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact-us')
def contactus():
    return render_template('ContactUs.html')

@app.route('/how-it-works')
def howitworks():
    return render_template('How_it_works.html')

@app.route('/thank-you')
def thankyou():
    return render_template('thankyou.html')

'''
Registering and signing in
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    # Create a SQLite database connection
    conn = sqlite3.connect('test-database.db')
    cursor = conn.cursor()

    # Create a users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_user_credential_table (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    print('test')
    
    if request.method == 'POST':
        print('test2')
        email = request.form['email']
        print('test3')
        password = request.form['password']

        # Check if the user already exists
        cursor.execute('SELECT * FROM test_user_credential_table WHERE email = ?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            return "User already exists!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        cursor.execute('INSERT INTO test_user_credential_table (email, password) VALUES (?, ?)', (email, password))
        conn.commit()

        return "Registration successful!"
    data = get_db_register()
    return render_template('register.html', all_data_register=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # Create a SQLite database connection
    conn = sqlite3.connect('test-database.db')
    cursor = conn.cursor()

    # Create a users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_user_credential_table (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    print('test1')
    if request.method == 'POST':
        print('test2')
        data = request.json
        json.dumps(data)
        print(data)
        email = request.form['email']
        print('test3')
        password = request.form['password']
        print('test4')
        # Retrieve the user from the database
        cursor.execute('SELECT * FROM test_user_credential_table WHERE email = ?', (email,))
        existing_email = cursor.fetchone()
                
        if existing_email[2] == email:
            if existing_email[3] == password:
                return "Login successful!"
            else:
                return "Invalid email or password"

    return render_template('login.html')

'''
mood and comment routes; track -> submit
'''
@app.route('/submit-comment', methods = ['POST']) # the first parameter in the app.route decorator needs to be the form action="THIS HERE" name
def submit():
    if request.method == 'POST':
        submit_comment = request.form['comment']
        submit_image = request.form['selectedImage']
        cleaned_image_name = __extract_image_name(submit_image)
        #------------------------------------------------------------------------------
        # Table Diagram
        #       emotion_id   |   user_id   |   selectedImage   |   comment   |   date 
        #           x               x               x                 x            x
        #           x               x               x                 x            x             
        #           x               x               x                 x            x
        #           x               x               x                 x            x
        #------------------------------------------------------------------------------
        data = (None, None, cleaned_image_name, submit_comment, datetime.now())
        db = g._database = sqlite3.connect('test-database.db') # establish connection
        cursor = db.cursor()
        
        # Insert the new comment into the 'comments' table
        cursor.execute('INSERT INTO test_mood_table (emotion_id, user_id, selectedImage, comment, date) VALUES (?,?,?,?,?)', data)
        db.commit()
        db.close()

        # Redirect to the index page after submitting the comment
        return render_template('thankyou.html')

'''
Testing 
'''
@app.route('/testingPage')
def testingPage():
    return render_template('testingPage.html')

@app.route('/testingPage2')
def testingPagetwo():
    return render_template('testingPage2.html')

@app.route('/show-all-db')
def testDatabase():
    data = get_db()
    return render_template('show-all-db.html', all_data=data)


'''
Helper functions
'''
def __extract_image_name(submit_image):
    # Get the filename part from the path
    _, filename = submit_image.rsplit('/', 1)

    # Check if the filename is in the allowed set
    if filename in ALLOWED_IMAGE_NAMES:
        return filename
    else:
        return None  # Not an allowed image

if __name__ == '__main__':
    app.run(debug=True) #python flask
