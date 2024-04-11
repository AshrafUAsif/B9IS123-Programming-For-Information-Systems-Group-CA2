from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

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

@app.route('/courses.html')
def courses():
    return render_template('courses.html')

@app.route('/course-details.html')
def course_details():
    return render_template('course-details.html')

@app.route('/log-in.html')
def log_in():
    return render_template('log-in.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)