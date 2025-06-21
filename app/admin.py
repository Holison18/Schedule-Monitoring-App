# In app/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from functools import wraps
from .models import db, Schedule, Pair, School, Admin
from .forms import AdminLoginForm
import csv
from io import StringIO

admin = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@admin.route('/', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin_user = Admin.query.filter_by(username=form.username.data).first()
        if admin_user and admin_user.check_password(form.password.data):
            session['admin_logged_in'] = True
            session['admin_username'] = admin_user.username
            flash('You were successfully logged in.', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin/admin_login.html', form=form)


@admin.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin.login'))


@admin.route('/dashboard')
@admin_required
def admin_dashboard():
    schedules = Schedule.query.order_by(Schedule.created_at.desc()).all()
    return render_template('admin/admin_dashboard.html', schedules=schedules)


@admin.route('/schedule/<int:schedule_id>/delete', methods=['POST'])
@admin_required
def delete_schedule(schedule_id):
    schedule_to_delete = Schedule.query.get_or_404(schedule_id)
    db.session.delete(schedule_to_delete)
    db.session.commit()
    flash('The schedule has been deleted.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/download_all_schedules')
@admin_required
def download_all_schedules():
    # This function remains the same
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Pair Name', 'School Name', 'Scheduled Date', 'Headmaster Name', 'Headmaster Contact', 'Created By'])
    schedules = Schedule.query.all()
    for s in schedules:
        writer.writerow([s.pair.pair_name, s.school.school_name, s.scheduled_date, s.headmaster_name_on_schedule, s.headmaster_contact_on_schedule, s.created_by])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=all_schedules.csv'})