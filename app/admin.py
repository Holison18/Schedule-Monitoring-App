from flask import Blueprint, render_template, Response
from flask_login import login_required # In a real app, you would have an admin role
from .models import Schedule
import csv
from io import StringIO

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
# @admin_required # In a real application, you would implement an admin role check
def admin_dashboard():
    schedules = Schedule.query.all()
    return render_template('admin/admin_dashboard.html', schedules=schedules)

@admin.route('/download_all_schedules')
# @admin_required
def download_all_schedules():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Pair Name', 'School Name', 'Scheduled Date', 'Headmaster Name', 'Headmaster Contact', 'Created By'])
    schedules = Schedule.query.all()
    for s in schedules:
        writer.writerow([s.pair.pair_name, s.school.school_name, s.scheduled_date, s.headmaster_name_on_schedule, s.headmaster_contact_on_schedule, s.created_by])
    output.seek(0)
    return Response(output, mimetype='text/csv', headers={'Content-Disposition': 'attachment;filename=all_schedules.csv'})