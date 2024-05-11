from flask import Flask, render_template, url_for, redirect, session, request, jsonify, g, flash
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from werkzeug.security import generate_password_hash, check_password_hash
from .configuration_key import SECRET_KEY
from datetime import datetime
from .models import UserCredential, Mood, db

import os
import sqlite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
#db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ALLOWED_IMAGE_NAMES = {'great5.png', 'happy4.png', 'neutral3.png', 'upset2.png', 'mad1.png'} # from static pngs

def get_db():
    db = getattr(g, '_database', None) # The g object is often used to store variables that should be accessible throughout the request-response cycle.
    if db is None:
        db = g._database = sqlite3.connect('database.db') # establish connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Mood')
        all_data = cursor.fetchall()
        #all_data = [str(val[0] for val in all_data)]
    return all_data

def get_db_register():
    db = getattr(g, '_database', None) # The g object is often used to store variables that should be accessible throughout the request-response cycle.
    if db is None:
        db = g._database = sqlite3.connect('database.db') # establish connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM UserCredential')
        all_data_register = cursor.fetchall()
        #all_data = [str(val[0] for val in all_data)]
    return all_data_register


class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = UserCredential.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
            
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

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
Registering and logging in
'''
@login_manager.user_loader
def load_user(user_id):
    return UserCredential.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print('test1')

    if form.is_submitted():
        print('submitted')
        
    print(form.errors)
    
    if form.validate():
        print("valid")
    
    print(form.errors)
    
    try:
        print(form.username.data)
        print(form.email.data)
        print(form.password.data)
    except:
        print('got stuck here')



    if form.validate_on_submit():
        print(form.username.data)
        print('test2')
        #hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = UserCredential(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('Track'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if form.validate_on_submit():
    #     user = UserCredential.query.filter_by(username=form.username.data).first()

    #     if user and bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user)
    #         flash('Login successful!', 'success')
    #         return redirect(url_for('home'))
    #     else:
    #         flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)

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
        #          id       |   user_id    |   selectedImage   |   comment    |   date 
        #           x               x               x                 x            x
        #           x               x               x                 x            x             
        #           x               x               x                 x            x
        #           x               x               x                 x            x
        #------------------------------------------------------------------------------
        data = (None, cleaned_image_name, submit_comment, datetime.now())
        db = g._database = sqlite3.connect('database.db') # establish connection
        cursor = db.cursor()
        
        # Insert the new comment into the 'comments' table
        cursor.execute('INSERT INTO Mood (id, selectedImage, comment, date) VALUES (?,?,?,?)', data)
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
    return render_template('show-all-db.html')


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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
