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
            #db.drop_all()
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
    #courses = load_json_data()
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

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

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

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already in use. Please choose a different email.', 'error')
            return redirect(url_for('sign_up'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(fullname=fullname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('sign-up.html')

@app.route('/users', methods=['GET'])
def get_users():
    if request.headers.get('Postman-Token'):
        users = User.query.all()
        return jsonify([user.serialize() for user in users])
    else:
        return "Only accessible via Postman", 403

# Delete User from the admin panel
@app.route('/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/delete-course/<int:course_id>')
@login_required
def delete_course(course_id):
    if not current_user.is_admin:
        return redirect(url_for('home'))
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course has been deleted successfully!', 'success')
    return redirect(url_for('admin'))


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    if request.headers.get('Postman-Token'):
        user = User.query.get_or_404(user_id)
        if request.method == 'GET':
            return jsonify(user.serialize())
        elif request.method == 'PUT':
            data = request.get_json()
            user.fullname = data.get('fullname', user.fullname)
            user.email = data.get('email', user.email)
            user.is_admin = data.get('is_admin', user.is_admin)
            db.session.commit()
            return jsonify(user.serialize())
        elif request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return "User deleted successfully", 204
    else:
        return "Only accessible via Postman", 403

@app.route('/courses', methods=['GET'])
def get_courses():
    if request.headers.get('Postman-Token'):
        courses = Course.query.all()
        return jsonify([course.serialize() for course in courses])
    else:
        return "Only accessible via Postman", 403

@app.route('/courses/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def course_detail(course_id):
    if request.headers.get('Postman-Token'):
        course = Course.query.get_or_404(course_id)
        if request.method == 'GET':
            return jsonify(course.serialize())
        elif request.method == 'PUT':
            data = request.get_json()
            course.title = data.get('title', course.title)
            course.category = data.get('category', course.category)
            course.instructor = data.get('instructor', course.instructor)
            course.rating = data.get('rating', course.rating)
            course.reviews = data.get('reviews', course.reviews)
            course.price = data.get('price', course.price)
            course.image = data.get('image', course.image)
            db.session.commit()
            return jsonify(course.serialize())
        elif request.method == 'DELETE':
            db.session.delete(course)
            db.session.commit()
            return "Course deleted successfully", 204
    else:
        return "Only accessible via Postman", 403

@app.route('/courses', methods=['POST'])
def add_course():
    if request.headers.get('Postman-Token'):
        data = request.get_json()
        new_course = Course(
            title=data['title'],
            category=data['category'],
            instructor=data['instructor'],
            rating=data['rating'],
            reviews=data['reviews'],
            price=data['price'],
            image=data['image']
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.serialize()), 201
    else:
        return "Only accessible via Postman", 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)