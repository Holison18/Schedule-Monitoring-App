from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from .forms import LoginForm
from .models import Pair, db

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    form.pair.choices = [(p.id, p.pair_name) for p in Pair.query.order_by('pair_name').all()]
    if form.validate_on_submit():
        pair = Pair.query.get(form.pair.data)
        if pair and (pair.user1_email == form.email.data.lower() or pair.user2_email == form.email.data.lower()):
            login_user(pair)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid login credentials.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))