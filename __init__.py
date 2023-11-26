import os
from flask import Flask, render_template, url_for, redirect, session, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'dev'


class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
    

#willow new addition. sets up DB. 
# look at the link in the issue 6.

#get current directory
basedir = os.path.abspath(os.path.dirname(__file__))

#path for our database file. It will appear in the current directory
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

#this turns of tracking of variables. might be necessary later funcs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#DB object is what we use to interact with the database
db = SQLAlchemy(app)

#id just start at 1 and incrm each time a new user joins
#  or we could do do a unique hashcode from first + last names
class User(db.Model):
    __tablename__ = 'User'

    #user metadata
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    #mood data
    totalmoods = db.Column(db.Integer)
    moods = db.relationship("Mood", back_populates="User")


    def __repr__(self):
        return f'<{self.firstname, self.lastname}>'
    
class Mood(db.Model):
    __tablename__ = 'Mood'
    #metadata
    time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    #establish a relation with user making the mood
    user = db.relationship("User", back_populates="Mood")
    user_id = db.Column(ForeignKey="User.id") #link the tables with a foreign key
    energy = db.Column(db.String(30)) #High-low Pleasant / High-low Unpleasant
    emot = db.Column(db.String(50), nullable=False) # word or short description of emotion for the entry


#inital account creation, 
# first get with username/email to check for existing user
# if get fails, post with given info.
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    #for the post we need to recieve from front end:
    #  a JSON packet with at least each field as defined in the User table
    #  additional data is allowed. 
    # 
    # Once the data is recieved from front end, adding to the DB looks like
    '''
    user_john = User(firstname='john', lastname='doe',
                       email='jd@hotmail.com', age=23,
                       bio='no hoes'
        
        Notice id is ommited from this entry. Because it is set as the
        PrimaryKey, SQL will inherently increm and apply the key to new entries.

    '''

    #Now we have the user_john object which represents our data entry
    #We still need to add the entry to the db session
    #  db.session.add(student_john)

    # We aren't done yet. To finally push the entires to the db
    # we need to commit our additions. It works just like git.
    #   db.session.commit()

    return 0

@app.route('/track')
def track():
    #rename this to 'moods' 
    return render_template('track.html')


'''
Routes for the webpage are listed below
    @Austin give an explanation, u kno betr
'''

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact-us')
def contactus():
    return render_template('ContactUs.html')

@app.route('/how-it-works')
def howitworks():
    return render_template('How_it_works.html')

@app.route('/testingpage')
def testingPage():
    return render_template('testingPage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post-comment', methods=['POST'])
def post_comment():
    selected_image = request.form.get('selected-image')
    comment = request.form.get('comment')

    # Store the data in the session
    session['selected_image'] = selected_image
    session['comment'] = comment

    # Redirect back to the page with the form
    return redirect(url_for('display_comment'))

@app.route('/display_comment', methods=['POST', 'GET'])
def display_comment():
    if request.method == 'POST':
        selected_image = request.form.get('selected_image')
        comment = request.form.get('comment')

        # Store the data in the session
        session['selected_image'] = selected_image
        session['comment'] = comment

        # Redirect to the same page to prevent resubmission on page refresh
        return redirect(url_for('display_comment'))

    # If it's a GET request or after form submission, display the stored data
    selected_image = session.get('selected_image')
    comment = session.get('comment')

    return render_template('display_comment.html', selected_image=selected_image, comment=comment)


if __name__ == '__main__':
    app.run(debug=True)
