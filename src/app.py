from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus_connect_secret_key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_connect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/profile_pictures'
app.config['RESUME_FOLDER'] = 'static/uploads/resumes'
app.config['GALLERY_FOLDER'] = 'static/uploads/gallery'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folders exist
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
os.makedirs(os.path.join(app.root_path, app.config['RESUME_FOLDER']), exist_ok=True)
os.makedirs(os.path.join(app.root_path, app.config['GALLERY_FOLDER']), exist_ok=True)

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'student' or 'college'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False)
    college_profile = db.relationship('CollegeProfile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Student Profile Model
class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    college_name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True, default='default_profile.jpg')
    resume = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    education_details = db.relationship('EducationDetail', backref='student', lazy=True)

    def __repr__(self):
        return f'<StudentProfile {self.first_name} {self.last_name}>'

# Education Details Model
class EducationDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    institution_name = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    field_of_study = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    grade = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<EducationDetail {self.institution_name}>'

# College Profile Model
class CollegeProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campus_name = db.Column(db.String(100), nullable=False)
    campus_location = db.Column(db.String(100), nullable=False)
    established_year = db.Column(db.Integer, nullable=False)
    website = db.Column(db.String(100), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True, default='default_college.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    courses = db.relationship('CollegeCourse', backref='college', lazy=True)
    events = db.relationship('CollegeEvent', backref='college', lazy=True)
    gallery_images = db.relationship('GalleryImage', backref='college', lazy=True)

    def __repr__(self):
        return f'<CollegeProfile {self.campus_name}>'

# College Course Model
class CollegeCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college_profile.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(20), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CollegeCourse {self.course_name}>'

# College Event Model
class CollegeEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college_profile.id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_image = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CollegeEvent {self.event_name}>'

# Gallery Image Model
class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college_profile.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryImage {self.id}>'

# Create database tables
with app.app_context():
    db.create_all()

# Helper function for file uploads
def allowed_file(filename, types):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')  # 'student' or 'college'

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user
        new_user = User(email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if user.role == 'student':
        # Check if student has a profile
        student_profile = StudentProfile.query.filter_by(user_id=user.id).first()
        if not student_profile:
            # If student doesn't have a profile, redirect to create one
            return redirect(url_for('create_profile'))
            
        return render_template('dashboard.html', user=user, profile=student_profile)
    else:
        # For college users
        college_profile = CollegeProfile.query.filter_by(user_id=user.id).first()
        if not college_profile:
            return redirect(url_for('create_college_profile'))
        
        return render_template('dashboard.html', user=user, profile=college_profile)

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is a student
    user = User.query.get(session['user_id'])
    if user.role != 'student':
        flash('Only students can create this type of profile', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if profile already exists
    existing_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    if existing_profile:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        bio = request.form.get('bio')
        college_name = request.form.get('college_name')
        course = request.form.get('course')
        start_year = request.form.get('start_year')
        end_year = request.form.get('end_year')
        
        # File upload handling
        profile_picture = 'default_profile.jpg'  # Default image
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '' and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                filename = secure_filename(f"{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                profile_picture = filename
        
        # Create new profile
        new_profile = StudentProfile(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
            college_name=college_name,
            course=course,
            start_year=start_year,
            end_year=end_year,
            profile_picture=profile_picture
        )
        
        db.session.add(new_profile)
        db.session.commit()
        
        flash('Profile created successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('create_profile.html')

@app.route('/create-college-profile', methods=['GET', 'POST'])
def create_college_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is a college
    user = User.query.get(session['user_id'])
    if user.role != 'college':
        flash('Only colleges can create this type of profile', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if profile already exists
    existing_profile = CollegeProfile.query.filter_by(user_id=user.id).first()
    if existing_profile:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        campus_name = request.form.get('campus_name')
        campus_location = request.form.get('campus_location')
        established_year = request.form.get('established_year')
        website = request.form.get('website')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        description = request.form.get('description')
        
        # File upload handling
        profile_picture = 'default_college.jpg'  # Default image
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '' and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                filename = secure_filename(f"college_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                profile_picture = filename
        
        # Create new profile
        new_profile = CollegeProfile(
            user_id=user.id,
            campus_name=campus_name,
            campus_location=campus_location,
            established_year=established_year,
            website=website,
            contact_email=contact_email,
            contact_phone=contact_phone,
            description=description,
            profile_picture=profile_picture
        )
        
        db.session.add(new_profile)
        db.session.commit()
        
        flash('College profile created successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('create_college_profile.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if user.role == 'student':
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            return redirect(url_for('create_profile'))
        
        education = EducationDetail.query.filter_by(student_id=profile.id).all()
        return render_template('student_profile.html', user=user, profile=profile, education=education)
    else:
        profile = CollegeProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            return redirect(url_for('create_college_profile'))
        
        courses = CollegeCourse.query.filter_by(college_id=profile.id).all()
        events = CollegeEvent.query.filter_by(college_id=profile.id).all()
        gallery = GalleryImage.query.filter_by(college_id=profile.id).all()
        return render_template('college_profile.html', user=user, profile=profile, courses=courses, events=events, gallery=gallery)

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if user.role == 'student':
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            return redirect(url_for('create_profile'))
        
        if request.method == 'POST':
            profile.first_name = request.form.get('first_name')
            profile.last_name = request.form.get('last_name')
            profile.bio = request.form.get('bio')
            profile.college_name = request.form.get('college_name')
            profile.course = request.form.get('course')
            profile.start_year = request.form.get('start_year')
            profile.end_year = request.form.get('end_year')
            
            # Handle file upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename != '' and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                    filename = secure_filename(f"{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Delete old profile picture if it's not the default
                    if profile.profile_picture != 'default_profile.jpg':
                        try:
                            old_file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], profile.profile_picture)
                            if os.path.exists(old_file_path):
                                os.remove(old_file_path)
                        except Exception as e:
                            print(f"Error removing old profile picture: {e}")
                    
                    profile.profile_picture = filename
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        
        return render_template('edit_profile.html', profile=profile)
    else:
        # Handle college profile edits
        profile = CollegeProfile.query.filter_by(user_id=user.id).first()
        if not profile:
            return redirect(url_for('create_college_profile'))
        
        if request.method == 'POST':
            profile.campus_name = request.form.get('campus_name')
            profile.campus_location = request.form.get('campus_location')
            profile.established_year = request.form.get('established_year')
            profile.website = request.form.get('website')
            profile.contact_email = request.form.get('contact_email')
            profile.contact_phone = request.form.get('contact_phone')
            profile.description = request.form.get('description')
            
            # Handle file upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename != '' and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                    filename = secure_filename(f"college_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Delete old profile picture if it's not the default
                    if profile.profile_picture != 'default_college.jpg':
                        try:
                            old_file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], profile.profile_picture)
                            if os.path.exists(old_file_path):
                                os.remove(old_file_path)
                        except Exception as e:
                            print(f"Error removing old profile picture: {e}")
                    
                    profile.profile_picture = filename
            
            db.session.commit()
            flash('College profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        
        return render_template('edit_college_profile.html', profile=profile)

# Education CRUD routes
@app.route('/add-education', methods=['GET', 'POST'])
def add_education():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'student':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return redirect(url_for('create_profile'))
    
    if request.method == 'POST':
        new_education = EducationDetail(
            student_id=profile.id,
            institution_name=request.form.get('institution_name'),
            degree=request.form.get('degree'),
            field_of_study=request.form.get('field_of_study'),
            start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'),
            grade=request.form.get('grade'),
            description=request.form.get('description')
        )
        
        if request.form.get('end_date'):
            new_education.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        
        db.session.add(new_education)
        db.session.commit()
        flash('Education added successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_education.html')

@app.route('/edit-education/<int:edu_id>', methods=['GET', 'POST'])
def edit_education(edu_id):
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'student':
        return redirect(url_for('login'))
    
    education = EducationDetail.query.get_or_404(edu_id)
    profile = StudentProfile.query.filter_by(id=education.student_id).first()
    
    # Security check to ensure user owns this education record
    if profile.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        education.institution_name = request.form.get('institution_name')
        education.degree = request.form.get('degree')
        education.field_of_study = request.form.get('field_of_study')
        education.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d')
        education.grade = request.form.get('grade')
        education.description = request.form.get('description')
        
        if request.form.get('end_date'):
            education.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        else:
            education.end_date = None
        
        db.session.commit()
        flash('Education updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_education.html', education=education)

@app.route('/delete-education/<int:edu_id>')
def delete_education(edu_id):
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'student':
        return redirect(url_for('login'))
    
    education = EducationDetail.query.get_or_404(edu_id)
    profile = StudentProfile.query.filter_by(id=education.student_id).first()
    
    # Security check to ensure user owns this education record
    if profile.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('profile'))
    
    db.session.delete(education)
    db.session.commit()
    flash('Education deleted successfully!', 'success')
    return redirect(url_for('profile'))

# Resume upload
@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'student':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    profile = StudentProfile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return redirect(url_for('create_profile'))
    
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename != '' and allowed_file(file.filename, {'pdf', 'doc', 'docx'}):
            filename = secure_filename(f"resume_{user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
            file_path = os.path.join(app.root_path, app.config['RESUME_FOLDER'], filename)
            file.save(file_path)
            
            # Delete old resume if exists
            if profile.resume:
                try:
                    old_file_path = os.path.join(app.root_path, app.config['RESUME_FOLDER'], profile.resume)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                except Exception as e:
                    print(f"Error removing old resume: {e}")
            
            profile.resume = filename
            db.session.commit()
            flash('Resume uploaded successfully!', 'success')
        else:
            flash('Invalid file format. Please upload a PDF, DOC, or DOCX file.', 'danger')
    else:
        flash('No file selected', 'danger')
    
    return redirect(url_for('profile'))

# College Course CRUD routes
@app.route('/add-course', methods=['GET', 'POST'])
def add_course():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'college':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    profile = CollegeProfile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return redirect(url_for('create_college_profile'))
    
    if request.method == 'POST':
        new_course = CollegeCourse(
            college_id=profile.id,
            course_name=request.form.get('course_name'),
            course_code=request.form.get('course_code'),
            department=request.form.get('department'),
            description=request.form.get('description'),
            duration=request.form.get('duration')
        )
        
        db.session.add(new_course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_course.html')

@app.route('/edit-course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'college':
        return redirect(url_for('login'))
    
    course = CollegeCourse.query.get_or_404(course_id)
    profile = CollegeProfile.query.filter_by(id=course.college_id).first()
    
    # Security check to ensure user owns this course
    if profile.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        course.course_name = request.form.get('course_name')
        course.course_code = request.form.get('course_code')
        course.department = request.form.get('department')
        course.description = request.form.get('description')
        course.duration = request.form.get('duration')
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_course.html', course=course)

@app.route('/delete-course/<int:course_id>')
def delete_course(course_id):
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'college':
        return redirect(url_for('login'))
    
    course = CollegeCourse.query.get_or_404(course_id)
    profile = CollegeProfile.query.filter_by(id=course.college_id).first()
    
    # Security check to ensure user owns this course
    if profile.user_id != session['user_id']:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('profile'))
    
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('profile'))

# College Event CRUD routes
@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session or User.query.get(session['user_id']).role != 'college':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    profile = CollegeProfile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        return redirect(url_for('create_college_profile'))
    
    if request.method == 'POST':
        event_image = None
        if 'event_image' in request.files:
            file = request.files['event_image']
            if file and file.filename != '' and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                filename = secure_filename(f"event_{profile.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.root_path, app.config['GALLERY_FOLDER'], filename)
                file.save(file_path)
                event_image = filename
        
        new_event = CollegeEvent(
            college_id=profile.id,
            event_name=request.form.get('event_name'),
            event_date=datetime.strptime(request.form.get('event_date'), '%Y-%m-%dT%H:%M'),
            event_location=request.form.get('event_location'),
            description=request.form.get('description'),
            event_image=event_image
        )
        
        db.session.add(new_event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_event.html')

@app.route('/edit-event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'user_id' not in session or User
