from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///EnrollmentSystem.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Courses(db.Model):
    c_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_code = db.Column(db.Text, nullable=False)
    c_name = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    c_size = db.Column(db.Integer, nullable=False)
    # vacancy = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    pre_req = db.Column(db.Text)


    def __init__(self, c_id, c_code, c_name, start_date, end_date, c_size, location, description, pre_req):
        self.c_id = c_id
        self.c_code = c_code
        self.c_name = c_name
        self.start_date = start_date
        self.end_date = end_date
        self.c_size = c_size
        # self.vacancy = vacancy
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

        if not request.form['Course Code'] or not request.form['Course Name'] or not request.form['Start Date'] or not request.form['End Date'] or not request.form['Class Size'] or not request.form['Location']:
            flash('Please enter all the fields.', 'Error')
        else:
            c_code = request.form['Course Code']
            c_name = request.form['Course Name']
            start_date = request.form['Start Date']
            end_date = request.form['End Date']
            c_size = request.form['Class Size']
            # vacancy = request.form['Class Size']
            location = request.form['Location']

            if not request.form['Description']:
                description = ''
            else:
                description = request.form['Description']

            if not request.form['Pre-requisites']:
                pre_req = ''
            else:
                pre_req = request.form['Pre-requisites']

            course = Courses(c_code=c_code, c_name=c_name, start_date=start_date, end_date=end_date, c_size=c_size, vacancy=vacancy, location=location, description=description, pre_req=pre_req)

            db.session.add(course)
            db.session.commit()

            flash('Record was successfully added.')
            return redirect(url_for('index_courses'))

    return render_template('create.html')


@app.route('/courses/<int:c_id>/edit', methods=['POST', 'GET'])
def edit_course(c_id):
    if request.method == 'POST':

        record = Courses.query.get(c_id)

        if request.form['Start Date']:
            record.start_date = request.form['Start Date']
        if request.form['End Date']:
            record.end_date = request.form['End Date']
        if request.form['Class Size']:
            record.c_size = request.form['Class Size']
        if request.form['Location']:
            record.location = request.form['Location']
        if request.form['Description']:
            record.description = request.form['Description']
        if request.form['Pre-requisites']:
            record.pre_req = request.form['Pre-requisites']

        db.session.commit()
        return flash('Record was successfully updated.')

    return render_template('edit.html')


@app.route('/courses/<int:c_id>/delete')
def delete_course(c_id):
    course = Courses.query.get(c_id)
    db.session.delete(course)
    db.session.commit()
    flash('Record was successfully deleted.')

    return redirect('courses.html')


if __name__ == '__main__':
    app.run(debug=True)
