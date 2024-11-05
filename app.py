from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os

from models import db, Assignment, Student, Admin, Question

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'anushka'  # Replace with a secure key in production

# Initialize the SQLAlchemy database with app context
db.init_app(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()

        # Check if student exists and password matches
        if student and student.password == password:
            session['student_email'] = student.email
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password')

    return render_template('student_login.html')

@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash("Email already registered. Please log in.")
            return redirect(url_for('student_login'))

        # Create a new student entry
        new_student = Student(email=email, password=password)
        db.session.add(new_student)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('student_login'))

    return render_template('student_signup.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = Admin.query.filter_by(email=email).first()

        # Check if admin exists and password matches
        if admin and admin.password == password:
            session['admin_email'] = admin.email
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password')

    return render_template('admin_login.html')

@app.route('/admin/signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        existing_admin = Admin.query.filter_by(email=email).first()
        if existing_admin:
            flash("Email already registered. Please log in.")
            return redirect(url_for('admin_login'))

        # Create a new admin entry
        new_admin = Admin(email=email, password=password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('admin_login'))

    return render_template('admin_signup.html')



from werkzeug.utils import secure_filename

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        assignment_topic = request.form['assignment_topic']
        role = request.form['role']
        submission_date = request.form['submission_date']
        
        # Process file upload
        uploaded_file = request.files['file']
        upload_folder = 'uploads/questions'  
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(upload_folder, filename)
        uploaded_file.save(file_path)
        
        # Create a new Question entry
        new_question = Question(
            assignment_topic=assignment_topic,
            role=role,
            submission_date=datetime.strptime(submission_date, '%Y-%m-%d'),
            file_path=file_path
        )
        db.session.add(new_question)
        db.session.commit()
        
        flash("Question paper added successfully!")
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_dashboard.html')



@app.route('/student/dashboard')
def student_dashboard():
    if 'student_email' not in session:
        return redirect(url_for('student_login'))

    student_email = session['student_email']
     # Fetch all question papers
    questions = Question.query.all()
    return render_template('dashboard.html', questions=questions, enumerate=enumerate)



@app.route('/logout')
def logout():
    session.pop('student_email', None)  # Remove student_email from the session
    flash("You have been logged out.")
    return redirect(url_for('student_login'))

@app.route('/upload_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def upload_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if request.method == 'POST':
        uploaded_file = request.files['assignment_file']

        # Ensure the upload folder exists
        upload_folder = "uploads"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)

        assignment.status = 'Submitted'
        db.session.commit()
        return redirect(url_for('student_dashboard'))

    return render_template('upload_assignment.html', assignment=assignment)

# Initialize the database if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)