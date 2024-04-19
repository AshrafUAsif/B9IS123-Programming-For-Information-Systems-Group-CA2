from flask import Flask, render_template


app = Flask(__name__)

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