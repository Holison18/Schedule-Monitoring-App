from flask import Blueprint, render_template, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from .models import db, School, Schedule
from .forms import ScheduleForm
from datetime import datetime
import csv
from io import StringIO

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard/dashboard.html')

@dashboard.route('/assigned_schools')
@login_required
def assigned_schools():
    return render_template('dashboard/assigned_schools.html', schools=current_user.schools)

@dashboard.route('/schedule')
@login_required
def view_schedule():
    return render_template('dashboard/view_schedule.html', schedules=current_user.schedules)

@dashboard.route('/add_edit_schedule')
@login_required
def add_edit_schedule():
    return render_template('dashboard/add_edit_schedule.html', schools=current_user.schools)

@dashboard.route('/school/<int:school_id>/schedule', methods=['GET', 'POST'])
@login_required
def schedule_for_school(school_id):
    school = School.query.get_or_404(school_id)
    schedule = school.schedule
    if schedule and schedule.created_by != current_user.user1_email and schedule.created_by != current_user.user2_email:
        flash('You are not authorized to edit this schedule.', 'danger')
        return redirect(url_for('dashboard.add_edit_schedule'))

    form = ScheduleForm(obj=schedule)
    
    if form.validate_on_submit():
        if not schedule:
            schedule = Schedule(school_id=school.id, pair_id=current_user.id, created_by=current_user.user1_email) # Or logic to get current user email
            db.session.add(schedule)

        form.populate_obj(schedule)
        schedule.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Schedule has been updated.', 'success')
        return redirect(url_for('dashboard.view_schedule'))

    return render_template('dashboard/schedule_form.html', form=form, school=school)

@dashboard.route('/download_schedule')
@login_required
def download_schedule():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['School Name', 'Scheduled Date', 'Headmaster', 'Contact', 'Created By'])
    for schedule in current_user.schedules:
        writer.writerow([schedule.school.school_name, schedule.scheduled_date, schedule.headmaster_name_on_schedule, schedule.headmaster_contact_on_schedule, schedule.created_by])
    output.seek(0)
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=my_schedule.csv"})