from unicodedata import category
from flask import Blueprint, render_template, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Review
from . import db

views = Blueprint('views' , __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='POST':
        review = request.form.get('review')

        if len(review) < 1:
            flash('Search name is too short brother!', category='error')

            
        else:
            new_review = Review(data=review, user_id=current_user.id)
            db.session.add(new_review)
            db.session.commit()



            flash('Searching...', category='success')

    return render_template("home.html", user=current_user)