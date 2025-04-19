
# Campus Connect

A web application that connects students across campuses with two user roles: Student and College.

## Features

- Clean, responsive landing page with role selection
- User authentication (login/signup) with role-based access
- Flask backend with SQLite database
- Secure password handling with bcrypt hashing

## Project Structure

```
campus_connect/
├── app.py                  # Main Flask application
├── static/                 # Static files
│   ├── css/                # CSS stylesheets
│   │   ├── styles.css      # Main stylesheet
│   │   └── error.css       # Error styles
│   ├── js/                 # JavaScript files
│   │   └── script.js       # Main JavaScript file
│   └── images/             # Image files
├── templates/              # HTML templates
│   ├── index.html          # Landing page
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   └── dashboard.html      # User dashboard
└── requirements.txt        # Python dependencies
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd campus_connect
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the application at http://localhost:5000

## Database

The application uses SQLite with Flask-SQLAlchemy for the database. The database file `campus_connect.db` will be created automatically when you run the application for the first time.

## User Authentication

- Passwords are securely hashed using Flask-Bcrypt
- Users can register as either "Student" or "College"
- User sessions are managed using Flask's built-in session management

## Customization

- To modify the styling, edit the CSS files in the `static/css` directory
- To change the behavior of the application, edit the JavaScript files in the `static/js` directory
- To modify the database schema, edit the models in `app.py`

## Future Improvements

- Add profile pages for users
- Implement more features for students and colleges
- Add admin dashboard
- Implement password reset functionality
- Add email verification

## License

[MIT License](LICENSE)
