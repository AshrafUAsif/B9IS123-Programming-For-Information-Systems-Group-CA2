import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'newpass123'
db_path = os.path.join(os.path.dirname(__file__), 'edu.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'id': self.id,
            'fullname': self.fullname,
            'email': self.email,
            'is_admin': self.is_admin
        }




@app.route('/')
def home():
    return render_template('home.html', courses=courses)

@app.route('/courses')
def courses():
    return render_template('courses.html', courses=courses)

@app.route('/course-details')
def course_details():
    return render_template('course-details.html')

#Adding routes for the all other pages
@app.route('/about.html')
def about_html():
    return render_template('about.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/pricing.html')
def pricing():
    return render_template('pricing.html')

@app.route('/log-in.html')
def log_in():
    return render_template('log-in.html')

@app.route('/sign-up.html')
def sign_up():
    return render_template('sign-up.html')

@app.route('/careers.html')
def careers():
    return render_template('careers.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/instructor.html')
def instructor():
    return render_template('instructor.html')

@app.route('/admin.html')
def admin():
    return render_template('admin.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)