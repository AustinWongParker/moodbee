
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy


'''
Database
'''
db = SQLAlchemy()

# Define UserCredential model
class UserCredential(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    
    # relationship to mood table
    moods = db.relationship('Mood', backref='user', lazy=True)

# Define Mood model
class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selectedImage = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey(UserCredential.id))

if __name__ == '__main__':
    #db.create_all()
    db.session.commit()