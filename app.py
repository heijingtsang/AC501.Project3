from datetime import date
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify

app = Flask(__name__)
app.secret_key = "First Code Academy"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EnrollmentSystem.db'
db = SQLAlchemy(app)
# sslify = SSLify(app)

class Courses(db.Model):
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_code = db.Column(db.Text, nullable=False)
    c_name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    instructor = db.Column(db.Text, nullable=False)
    c_size = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    pre_req = db.Column(db.Text)


    def __init__(self, c_code, c_name, start_date, end_date, c_size, instructor, location, description, pre_req):
        self.c_code = c_code
        self.c_name = c_name
        self.start_date = start_date
        self.end_date = end_date
        self.instructor = instructor
        self.c_size = c_size
        self.location = location
        self.description = description
        self.pre_req = pre_req


db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/courses')
def index_courses():
    return render_template('courses.html', courses=Courses.query.all())


@app.route('/courses/<int:c_id>')
def course_details(c_id):
    return render_template('course_details.html', info=Courses.query.filter_by(c_id=c_id).first())


@app.route('/courses/add', methods=['POST', 'GET'])
def add_course():
    if request.method == 'POST':

        if not request.form['course code'] or not request.form['course name'] or not request.form['start-day'] or not request.form['start-month'] or not request.form['start-year'] or not request.form['end-day'] or not request.form['end-month'] or not request.form['end-year'] or not request.form['instructor'] or not request.form['class size'] or not request.form['location']:
            flash('Please enter all the fields.', 'Error')
        else:
            c_code = request.form['course code']
            c_name = request.form['course name']
            start_date = date(year=int(request.form['start-year']), month=int(request.form['start-month']), day=int(request.form['start-day']))
            end_date = date(year=int(request.form['end-year']), month=int(request.form['end-month']), day=int(request.form['end-day']))
            instructor = request.form['instructor']
            c_size = request.form['class size']
            location = request.form['location']

            if not request.form['description']:
                description = ''
            else:
                description = request.form['description']

            if not request.form['pre-req']:
                pre_req = ''
            else:
                pre_req = request.form['pre-req']

            course = Courses(c_code=c_code, c_name=c_name, start_date=start_date, end_date=end_date, instructor=instructor, c_size=c_size, location=location, description=description, pre_req=pre_req)

            db.session.add(course)
            db.session.commit()

            flash('Record was successfully added.')
            return redirect(url_for('index_courses'))

    return render_template('create.html')


@app.route('/courses/<int:c_id>/edit', methods=['POST', 'GET'])
def edit_course(c_id):
    if request.method == 'POST':

        record = Courses.query.filter_by(c_id=c_id).first()

        if request.form['course code']:
            record.c_code = request.form['course code']
        if request.form['course name']:
            record.c_name = request.form['course name']
        if request.form['start-day'] and request.form['start-month'] and request.form['start-year']:
            record.start_date = date(year=int(request.form['start-year']), month=int(request.form['start-month']), day=int(request.form['start-day']))
        if request.form['end-day'] and request.form['end-month'] and request.form['end-year']:
            record.end_date = date(year=int(request.form['end-year']), month=int(request.form['end-month']), day=int(request.form['end-day']))
        if request.form['instructor']:
            record.instructor = request.form['instructor']
        if request.form['class size']:
            record.c_size = request.form['class size']
        if request.form['location']:
            record.location = request.form['location']
        if request.form['description']:
            record.description = request.form['description']
        if request.form['pre-req']:
            record.pre_req = request.form['pre-req']

        db.session.commit()
        flash('Record was successfully updated.')
        return redirect(url_for('index_courses'))

    return render_template('edit.html')


@app.route('/courses/<int:c_id>/delete')
def delete_course(c_id):
    course = Courses.query.filter_by(c_id=c_id).first()
    db.session.delete(course)
    db.session.commit()
    flash('Record was successfully deleted.')

    return redirect(url_for('index_courses'))


if __name__ == '__main__':
    app.run()
