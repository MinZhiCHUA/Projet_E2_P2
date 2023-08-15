from flask import Blueprint
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from .forms import LoginForm, PredictionForm

import numpy as np
import pandas as pd
import joblib
from .feature_eng_func import *


model = joblib.load(open('application/better_model_lasso.joblib', 'rb'))

simple_page = Blueprint('simple_page', __name__)



@simple_page.route('/')
def index():
    return render_template('index.html')

@simple_page.route('/predict')
def predict():
    return render_template('predict.html')

@simple_page.route('/predict', methods=['POST'])
def predict_post():

    X_predict_test=pd.DataFrame()

    print(request.form['Lot_Area'])

    X_predict_test.insert(0, 'score_room', [get_room_score(TotRms_AbvGrd=int(request.form['TotRms_AbvGrd']), Full_Bath=int(request.form['TotRms_AbvGrd']))])
    X_predict_test.insert(0, 'score_internal', [get_internal_score(score_internal=int(request.form['score_internal']))])
    X_predict_test.insert(0, 'score_external', [get_external_score()])
    X_predict_test.insert(0, 'score_condition', [get_condition_score()])
    X_predict_test.insert(0, 'Neighborhood', [get_neighborhood_score(request.form['Neighborhood'])])
    X_predict_test.insert(0, 'score_feature', [get_feature_score()])
    X_predict_test.insert(0, 'score_garage', [get_garage_score()])
    X_predict_test.insert(0, 'score_basement', [get_basement_score()])
    X_predict_test.insert(0, 'score_age', [get_age_score(Year_Built=int(request.form['Year_Built']))])
    X_predict_test.insert(0, 'score_ext_area', [get_ext_area_score(Lot_Area=int(request.form['Lot_Area']))])


    pred = model.predict(X_predict_test)

    return render_template('predict.html', 
        data=int(pred), Neighborhood=request.form['Neighborhood'],
        TotRms_AbvGrd=int(request.form['TotRms_AbvGrd']), 
        Full_Bath=int(request.form['Full_Bath']), 
        score_internal=int(request.form['score_internal']),
        Year_Built=int(request.form['Year_Built']),
        Lot_Area=int(request.form['Lot_Area']))

# @simple_page.route("/login", methods=["GET","POST"])
# def login():
#     # form = LoginForm()
#     # if form.validate_on_submit():
#     #     user = User.query.filter_by(email_address=form.mail.data).first()
#     #     if user and check_password_hash(user.password_hash, form.password.data):
#     #         login_user(user)
#     #         flash("Logged in with success", category="success")
#     #         return redirect(url_for('home'))
#     #     else:
#     #         flash("Mail address or password invalid", category="danger")
#     return render_template('login.html', form=form)

# @simple_page.route("/logout")
# # @login_required
# def logout():
#     logout_user()
#     flash("Logged out with success", category="success")
#     return redirect(url_for("index"))