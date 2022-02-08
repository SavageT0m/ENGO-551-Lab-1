from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Review
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth' , __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect (url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')


    return render_template("login.html" , user=current_user)
            


    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))






@auth.route('/sign-up', methods=['GET' , 'POST'])
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        #last_name  = request.form.get('lastName')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

        user = User.query.filter_by(email=email).first()

        if user:
            flash ('Email already being used, sorry about that mate!', category='error')
        elif len(email)< 4:
            flash('Email must include more than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name has to be more than 1 characters', category='error')
        #elif len(last_name) < 2:
            #flash('Last Name has to be more than 1 characters', category='error')
        elif len(password) < 5:
            flash('Password needs to be more than 4 characters', category='error')
        elif password != password_check:
            flash('Passwords do not match', category='error')

        else:
            #add user
            new_user=User(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created, Great Job Einstein!', category='success')
            return redirect(url_for('views.home'))
           
    return render_template("sign_up.html" , user=current_user)