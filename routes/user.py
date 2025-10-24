from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Complaint
from forms import ComplaintForm
from datetime import datetime

user_bp = Blueprint('user', __name__)

def user_only(f):
    def decorated_function(*args, **kwargs):
        if current_user.role != 'user':
            flash('Access denied. This page is for users only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return login_required(decorated_function)

@user_bp.route('/dashboard')
@user_only
def dashboard():
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    return render_template('user/dashboard.html', complaints=complaints)

@user_bp.route('/submit-complaint', methods=['GET', 'POST'])
@user_only
def submit_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            user_id=current_user.id,
            district=form.district.data,
            corporation_type=form.corporation_type.data,
            road_name=form.road_name.data,
            national_highway=form.national_highway.data,
            landmark=form.landmark.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            description=form.description.data,
            status='Submitted'
        )
        
        db.session.add(complaint)
        db.session.commit()
        
        flash('Complaint submitted successfully! You will receive an acknowledgement soon.', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/submit_complaint.html', form=form)

@user_bp.route('/complaint/<int:complaint_id>')
@user_only
def view_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/view_complaint.html', complaint=complaint)
