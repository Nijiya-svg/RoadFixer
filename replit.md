# Road Safety Management System

## Overview
A Flask-based web application for managing road safety complaints. The system allows users to report road safety issues (potholes, damages, etc.) and tracks them through verification, assignment, and resolution stages.

## Current State
- **Status**: Fully functional MVP
- **Framework**: Flask (Python)
- **Database**: SQLite
- **Theme**: Dark theme UI
- **Last Updated**: October 24, 2025

## Project Architecture

### Database Models
- **User Model**: Handles authentication with three roles (user, admin, contractor)
- **Complaint Model**: Stores road safety complaints with location details and status tracking

### Modules (Route Blueprints)
1. **Authentication Module** (`routes/auth.py`):
   - User registration with role selection
   - Login/logout functionality
   - Role-based redirects

2. **User Module** (`routes/user.py`):
   - Submit complaints with location details
   - View complaint status
   - Track acknowledgements

3. **Admin Module** (`routes/admin.py`):
   - View all complaints
   - Verify complaints and send acknowledgements
   - Assign contractors to verified complaints
   - Dashboard with statistics

4. **Contractor Module** (`routes/contractor.py`):
   - View assigned complaints
   - Acknowledge site visits
   - Mark complaints as resolved

### Folder Structure
```
project/
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── forms.py                    # WTForms definitions
├── routes/                     # Route blueprints
│   ├── auth.py                # Authentication routes
│   ├── user.py                # User module routes
│   ├── admin.py               # Admin module routes
│   └── contractor.py          # Contractor module routes
├── templates/                  # HTML templates
│   ├── base.html              # Base template with dark theme
│   ├── auth/                  # Authentication templates
│   ├── user/                  # User module templates
│   ├── admin/                 # Admin module templates
│   └── contractor/            # Contractor module templates
├── static/
│   ├── css/style.css          # Dark theme styles
│   └── js/main.js             # JavaScript (geolocation)
└── database.db                # SQLite database
```

## Features Implemented

### Core Features
- ✅ User registration and login with three user roles
- ✅ Complaint submission with location capture (geolocation)
- ✅ Complaint status tracking (Submitted → Verified → Assigned → In Progress → Resolved)
- ✅ Admin verification workflow with acknowledgements
- ✅ Contractor assignment system
- ✅ Contractor acknowledgement workflow
- ✅ Dark theme UI with responsive design
- ✅ Role-based access control

### Complaint Details Captured
- District name
- Corporation type (District Corporation, Municipality, Panchayath)
- Road name
- National highway (optional)
- Landmark (school, hospital, etc.)
- GPS coordinates (latitude/longitude)
- Detailed description

## Default Credentials
- **Admin Account**:
  - Username: `admin`
  - Password: `admin123`

## How to Use

### As a User:
1. Register with role "User"
2. Login and navigate to "Submit Complaint"
3. Fill in location details and description
4. Click "Get Current Location" to capture GPS coordinates
5. Submit and track status on dashboard

### As an Admin:
1. Login with admin credentials
2. View all complaints on dashboard
3. Click "Verify" on submitted complaints
4. Provide acknowledgement message to user
5. Assign verified complaints to contractors

### As a Contractor:
1. Register with role "Contractor"
2. Login to view assigned complaints
3. Click "Acknowledge" to confirm site visit
4. Provide acknowledgement details
5. Mark complaint as "Resolved" when completed

## Technical Details

### Dependencies
- Flask (web framework)
- Flask-Login (session management)
- Flask-SQLAlchemy (ORM)
- Flask-WTF (form handling)
- SQLite (database)

### Security
- Password hashing using Werkzeug
- CSRF protection via Flask-WTF
- Session secret from environment variable
- Role-based access control decorators

### Workflow
- **Name**: Flask Server
- **Command**: `python app.py`
- **Port**: 5000
- **Output**: Webview

## Recent Changes
- **2025-10-24**: Initial implementation with all three modules (User, Admin, Contractor)
- **2025-10-24**: Dark theme UI implementation
- **2025-10-24**: Database models and relationship setup
- **2025-10-24**: Geolocation feature for complaint submission
- **2025-10-24**: Complete workflow system (submission → verification → assignment → resolution)

## Future Enhancements (Next Phase)
- Email notifications for status updates
- Photo upload for road damage evidence
- Analytics dashboard with charts
- Search and filter functionality
- Complaint history archive
- Export complaints to PDF/Excel
- Mobile-responsive improvements
