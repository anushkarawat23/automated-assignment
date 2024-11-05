from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignments.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warnings

# Initialize the SQLAlchemy database
db = SQLAlchemy(app)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)  # Student's email
    assignment_name = db.Column(db.String(100), nullable=False)  # Assignment name
    role = db.Column(db.String(100), nullable=False)  # Role decided by admin
    deadline_date = db.Column(db.String(10), nullable=False)  # Deadline date
    status = db.Column(db.String(10), nullable=False, default="Pending")  # Status: Submitted or Pending

    def __repr__(self):
        return f'<Assignment {self.assignment_name}, {self.status}>'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords for security

    def __repr__(self):
        return f'<Student {self.email}>'

###############################################################################

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')
'''
# Route for file uploads
@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("file")  # Handle multiple file uploads
    email = request.form['email']  # Get the student's email from the form
    internship_type = request.form['internship_type']  # Get the internship type from the form

    upload_folder = "uploads"
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    for file in uploaded_files:
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        # Store the uploaded file information in the database
        new_assignment = Assignment(email=email, internship_type=internship_type, assignment_file=file.filename)
        db.session.add(new_assignment)  # Add the new entry to the session
        db.session.commit()  # Commit the session to save the changes to the database
    
    return "Files uploaded and stored in the database!"

'''

from flask import session, redirect, url_for, flash

@app.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        student = Student.query.filter_by(email=email).first()
        
        # Check if student exists and password matches
        if student and student.password == password:  # Implement password hashing for real applications
            session['student_email'] = student.email
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('student_login.html')


# Route for the student registration page
@app.route('/student/signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if email already exists
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


'''

# Route for the student dashboard page
@app.route('/dashboard')
def student_dashboard():
    # Replace 'student_email' with the logged-in student's email from session or login
    student_email = "student@example.com"
    assignments = Assignment.query.filter_by(email=student_email).all()
    return render_template('dashboard.html', assignments=assignments)
'''

@app.route('/student/dashboard')
def student_dashboard():
    if 'student_email' not in session:
        return redirect(url_for('student_login'))  # Redirect if not logged in
    
    student_email = session['student_email']
    assignments = Assignment.query.filter_by(email=student_email).all()
    return render_template('dashboard.html', assignments=assignments)


#Assignment Upload Page
@app.route('/upload_assignment/<int:assignment_id>', methods=['GET', 'POST'])
def upload_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if request.method == 'POST':
        # Handle file upload
        uploaded_file = request.files['assignment_file']
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)
        
        # Update assignment status to Submitted
        assignment.status = 'Submitted'
        db.session.commit()
        return redirect(url_for('student_dashboard'))
    
    return render_template('upload_assignment.html', assignment=assignment)


    
# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

app.secret_key = 'anushka'  # Replace with a secure key in a real app


if __name__ == "__main__":
    app.run(debug=True)
