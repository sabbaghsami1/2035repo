from flask import Blueprint, render_template, flash, redirect, url_for, session
from accounts.forms import RegistrationForm, LoginForm
from config import User, db, limiter

from flask_limiter.util import get_remote_address

accounts_bp = Blueprint('accounts', __name__, template_folder='templates')




@accounts_bp.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', category="danger")
            return render_template('accounts/registration.html', form=form)

        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        )

        db.session.add(new_user)
        db.session.commit()

        flash('Account Created', category='success')
        return redirect(url_for('accounts.login'))

    return render_template('accounts/registration.html', form=form)


@accounts_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20/minute")  # Allow 3 login attempts per minute
def login():
    # Retrieve invalid authentication count from the session, default is 0
    invalid_Auth = session.get('invalid_Auth', 0)

    # If the user has attempted to log in 3 times and failed, lock them out
    if invalid_Auth >= 3:
        flash(
            'Your account has been locked due to too many failed login attempts. Please reset your account to continue.',
            'danger'
        )
        return render_template('accounts/login.html', form=None)  # Hide the form if locked

    form = LoginForm()

    if form.validate_on_submit():  # Handles POST requests and form validation
        email = form.email.data
        password = form.password.data

        # Query the database for a user with the provided email
        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(password):
            # If user does not exist or password doesn't match
            invalid_Auth += 1
            session['invalid_Auth'] = invalid_Auth  # Store failed attempts in session

            flash(f'Invalid email or password. You have {3 - invalid_Auth} attempts remaining.', 'danger')
            return redirect(url_for('accounts.login'))  # Redirect to login page

        else:
            # If authentication succeeds, reset invalid attempts and log in
            session['invalid_Auth'] = 0  # Reset invalid attempts on successful login
            flash('Login successful!', 'success')
            return redirect(url_for('posts.posts'))  # Redirect to view posts page

    return render_template('accounts/login.html', form=form)


@accounts_bp.route('/reset_account')
def reset_account():
    # Reset the invalid attempts counter in the session
    session['invalid_Auth'] = 0
    flash('Your account has been unlocked. You can now try logging in again.', 'success')
    return redirect(url_for('accounts.login'))


@accounts_bp.route('/account')
def account():
    return render_template('accounts/account.html')
