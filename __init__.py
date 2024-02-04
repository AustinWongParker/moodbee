from flask import Flask, render_template, url_for, redirect, session, request, jsonify, g
from .configuration_key import SECRET_KEY
from datetime import datetime

import sqlite3

app = Flask(__name__)

ALLOWED_IMAGE_NAMES = {'great5.png', 'happy4.png', 'neutral3.png', 'upset2.png', 'mad1.png'} # from static pngs

'''
Database
'''
app.secret_key = SECRET_KEY

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('test-database.db') # establish connection
        cursor = db.cursor()
        cursor.execute('SELECT * FROM test_mood_table')
        all_data = cursor.fetchall()
        #all_data = [str(val[0] for val in all_data)]
    return all_data

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

'''
Routes
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/thank-you')
def thankyou():
    return render_template('thankyou.html')

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
