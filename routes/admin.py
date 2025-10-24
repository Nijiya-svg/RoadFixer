from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Complaint, User
from forms import AcknowledgementForm
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_only(f):
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. This page is for administrators only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return login_required(decorated_function)

@admin_bp.route('/dashboard')
@admin_only
def dashboard():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    total_complaints = Complaint.query.count()
    pending_complaints = Complaint.query.filter_by(status='Submitted').count()
    verified_complaints = Complaint.query.filter_by(status='Verified').count()
    resolved_complaints = Complaint.query.filter_by(status='Resolved').count()
    
    return render_template('admin/dashboard.html', 
                         complaints=complaints,
                         total_complaints=total_complaints,
                         pending_complaints=pending_complaints,
                         verified_complaints=verified_complaints,
                         resolved_complaints=resolved_complaints)

@admin_bp.route('/complaint/<int:complaint_id>')
@admin_only
def view_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    return render_template('admin/view_complaint.html', complaint=complaint)

@admin_bp.route('/complaint/<int:complaint_id>/verify', methods=['GET', 'POST'])
@admin_only
def verify_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    form = AcknowledgementForm()
    
    if form.validate_on_submit():
        complaint.status = 'Verified'
        complaint.admin_acknowledgement = form.acknowledgement.data
        complaint.verified_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Complaint verified and acknowledgement sent to user.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/verify_complaint.html', complaint=complaint, form=form)

@admin_bp.route('/complaint/<int:complaint_id>/assign', methods=['GET', 'POST'])
@admin_only
def assign_contractor(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    contractors = User.query.filter_by(role='contractor').all()
    
    if request.method == 'POST':
        contractor_id = request.form.get('contractor_id')
        
        if not contractor_id:
            flash('Please select a contractor.', 'danger')
            return redirect(url_for('admin.assign_contractor', complaint_id=complaint_id))
        
        complaint.contractor_id = int(contractor_id)
        complaint.status = 'Assigned'
        complaint.assigned_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Complaint assigned to contractor successfully.', 'success')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/assign_contractor.html', complaint=complaint, contractors=contractors)
