
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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

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
    # Relationship
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False)

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<StudentProfile {self.first_name} {self.last_name}>'

# Create database tables
with app.app_context():
    db.create_all()

# Helper function for file uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password_hash, password) and user.role == role:
            session['user_id'] = user.id
            session['role'] = user.role
            session['email'] = user.email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        role = request.form.get('role')
        
        # Validate password match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))
            
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        # Hash password and create new user
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password_hash=password_hash, role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

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
        return render_template('dashboard.html', user=user)

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is a student
    user = User.query.get(session['user_id'])
    if user.role != 'student':
        flash('Only students can create profiles', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if profile already exists
    existing_profile = StudentProfile.query.filter_by(user_id=user.id).first()
    if existing_profile:
        return redirect(url_for('edit_profile'))
    
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
            if file and file.filename != '' and allowed_file(file.filename):
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
        return redirect(url_for('dashboard'))
    
    return render_template('create_profile.html')

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
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
            if file and file.filename != '' and allowed_file(file.filename):
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
        return redirect(url_for('dashboard'))
    
    return render_template('edit_profile.html', profile=profile)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
