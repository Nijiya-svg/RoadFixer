from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Complaint
from forms import AcknowledgementForm
from datetime import datetime

contractor_bp = Blueprint('contractor', __name__)

def contractor_only(f):
    def decorated_function(*args, **kwargs):
        if current_user.role != 'contractor':
            flash('Access denied. This page is for contractors only.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return login_required(decorated_function)

@contractor_bp.route('/dashboard')
@contractor_only
def dashboard():
    complaints = Complaint.query.filter_by(contractor_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    assigned_complaints = Complaint.query.filter_by(contractor_id=current_user.id, status='Assigned').count()
    in_progress_complaints = Complaint.query.filter_by(contractor_id=current_user.id, status='In Progress').count()
    resolved_complaints = Complaint.query.filter_by(contractor_id=current_user.id, status='Resolved').count()
    
    return render_template('contractor/dashboard.html', 
                         complaints=complaints,
                         assigned_complaints=assigned_complaints,
                         in_progress_complaints=in_progress_complaints,
                         resolved_complaints=resolved_complaints)

@contractor_bp.route('/complaint/<int:complaint_id>')
@contractor_only
def view_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.contractor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('contractor.dashboard'))
    
    return render_template('contractor/view_complaint.html', complaint=complaint)

@contractor_bp.route('/complaint/<int:complaint_id>/acknowledge', methods=['GET', 'POST'])
@contractor_only
def acknowledge_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.contractor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('contractor.dashboard'))
    
    form = AcknowledgementForm()
    
    if form.validate_on_submit():
        complaint.contractor_acknowledgement = form.acknowledgement.data
        complaint.status = 'In Progress'
        
        db.session.commit()
        
        flash('Acknowledgement submitted successfully.', 'success')
        return redirect(url_for('contractor.dashboard'))
    
    return render_template('contractor/acknowledge_complaint.html', complaint=complaint, form=form)

@contractor_bp.route('/complaint/<int:complaint_id>/resolve', methods=['POST'])
@contractor_only
def resolve_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    
    if complaint.contractor_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('contractor.dashboard'))
    
    complaint.status = 'Resolved'
    complaint.resolved_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Complaint marked as resolved.', 'success')
    return redirect(url_for('contractor.dashboard'))
