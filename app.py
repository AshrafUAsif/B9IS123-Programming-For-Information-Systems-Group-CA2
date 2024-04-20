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

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)

    @property
    def average_rating(self):
        if self.reviews == 0:
            return 0
        return round(self.rating / self.reviews, 2)
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'instructor': self.instructor,
            'rating': self.rating,
            'reviews': self.reviews,
            'price': self.price,
            'image': self.image
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_db():
    try:
        with app.app_context():
            db.create_all()

            with open('sample_data/user.json') as user_file:
                users = json.load(user_file)
                for user_data in users:
                    hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
                    user_data['password'] = hashed_password
                    user = User(**user_data)
                    db.session.add(user)

            with open('sample_data/course.json') as course_file:
                courses = json.load(course_file)
                for course_data in courses:
                    course = Course(**course_data)
                    db.session.add(course)

            db.session.commit()
    except Exception as e:
        print(f"Error creating database: {e}")

create_db()


@app.route('/')
def home():
    courses = Course.query.all() 
    return render_template('home.html', courses=courses)

@app.route('/courses')
def courses():
    courses = Course.query.all() 
    return render_template('courses.html', courses=courses)

@app.route('/course-details')
def course_details():
    return render_template('course-details.html')

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    users = User.query.all()
    courses = Course.query.all()
    return render_template('admin.html', users=users, courses=courses)

@app.route('/about.html')
def about_html():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('log-in.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)