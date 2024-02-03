from flask import Flask, render_template, url_for, redirect, session, request, jsonify
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class selectedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    # Add more fields as needed
    selected = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Image(id={self.id}, filename={self.filename})"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(200), nullable=False)



@app.route('/testingPage')
def test_query_comments():
    comments = Comment.query.all()
    return render_template('testingPage.html', comments=comments)

@app.route('/testingPage2')
def testingPage():
    return render_template('testingPage2.html')

@app.route('/track')
def query_comments():
    comments = Comment.query.all()
    return render_template('track.html', comments=comments)

@app.route('/track')
def query_emotion():
    Emotions = Emotion.query.all()
    return render_template('track.html', Emotions=Emotions)

@app.route('/select_image', methods=['POST'])
def select_image():
    image_id = request.json.get('image_id')
    selected_image = selectedImage.query.get(image_id)

    if selected_image:
        # Mark the selected image as selected
        selected_image.selected = True
        db.session.commit()

        # Unselect all other images
        selectedImage.query.filter(selectedImage.id != image_id).update({selectedImage.selected: False})
        db.session.commit()

        return jsonify({'success': True, 'message': 'Image selected successfully'})
    else:
        return jsonify({'success': False, 'message': 'Image not found'}), 404

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

@app.route('/login')
def login():
    return render_template('login.html')

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
    db.create_all() #sqlalchemy
    app.run(debug=True) #python flask
