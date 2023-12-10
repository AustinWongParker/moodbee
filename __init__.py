from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

@app.route('/testingPage')
def query_comments():
    comments = Comment.query.all()
    return render_template('testingPage.html', comments=comments)

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

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/home', methods = ['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/track')
def track():
    return render_template('track.html')

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

'''
@app.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    return 'hi'
'''

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        comment_content = data.get('comment')

        # Create a new Comment object
        new_comment = Comment(content=comment_content)

        # Add the new comment to the database
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({'success': True, 'comment': new_comment.content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
