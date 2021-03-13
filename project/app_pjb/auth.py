from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash, make_response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, Permission, RoleNeed
from .permission import admin_authority 

auth = Blueprint('auth', __name__)

headers = {"Content-Type": "application/json"}

admin_permission = Permission(RoleNeed('admin'))

def validate_password_input(req_form):
    fields = ['old_password', 'new_password', 'confirm_password']
    for field in fields:
        if field not in req_form:
            return False
    return True

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.not_found'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    if User.query.count() > 0:
        return redirect(url_for('main.not_found'))
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    if User.query.count() > 0:
        return make_response(jsonify({'msg': 'Not Found'}), 404, headers) 
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email already exist')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, role=role, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    # code to validate and add user to database goes here
    return redirect(url_for('auth.login'))

# Profile page route
@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    user_info = {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }
    return render_template('profile.html', data={'user_info': user_info})

# Change name route
@auth.route('/change-name', methods=['POST'])
@login_required
def change_name():
    if 'name' in request.form and request.form.get('name') != '':
        user = User.query.filter_by(id=current_user.id).first()
        user.name = request.form.get('name')
        db.session.commit()
        flash('Name changed successfully', 'name_success')
        return redirect(url_for('auth.profile'))
    flash('No name provided', 'name_error')
    return redirect(url_for('auth.profile'))

# Change password route
@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    if not validate_password_input(request.form):
        flash('No password provided', 'password_error')
        return redirect(url_for('auth.profile'))

    user = User.query.filter_by(id=current_user.id).first()
    if not check_password_hash(user.password, request.form.get('old_password')):
        flash('Wrong old password', 'password_error')
        return redirect(url_for('auth.profile'))

    if request.form.get('new_password') != request.form.get('confirm_password'):
        flash("Confirm password doesn't match new password", 'password_error')
        return redirect(url_for('auth.profile'))

    user.password = generate_password_hash(request.form.get('new_password'), method='sha256')
    db.session.commit()
    flash('Password changed successfully', 'password_success')
    return redirect(url_for('auth.profile'))
            
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('main.index'))