from flask import Blueprint
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from flask_login import login_required, current_user

from .forms import LoginForm, PredictionForm

import numpy as np
import pandas as pd
import joblib
from .feature_eng_func import *
from application.models import User, Predict


model = joblib.load(open('application/better_model_lasso.joblib', 'rb'))

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict')
def predict():
    return render_template('predict.html')

@main.route('/predict', methods=['POST'])
def predict_post():

    X_predict_test=pd.DataFrame()



    # Put all request.form into the correct variable
    TotRms_AbvGrd=int(request.form['TotRms_AbvGrd'])
    Full_Bath=int(request.form['TotRms_AbvGrd'])
    score_internal=int(request.form['score_internal'])
    Neighborhood = request.form['Neighborhood']
    Year_Built=int(request.form['Year_Built'])
    Lot_Area=int(request.form['Lot_Area'])

    X_predict_test.insert(0, 'score_room', [get_room_score(TotRms_AbvGrd=TotRms_AbvGrd, Full_Bath=Full_Bath)])
    X_predict_test.insert(0, 'score_internal', [get_internal_score(score_internal=score_internal)])
    X_predict_test.insert(0, 'score_external', [get_external_score()])
    X_predict_test.insert(0, 'score_condition', [get_condition_score()])
    X_predict_test.insert(0, 'Neighborhood', [get_neighborhood_score(Neighborhood=Neighborhood)])
    X_predict_test.insert(0, 'score_feature', [get_feature_score()])
    X_predict_test.insert(0, 'score_garage', [get_garage_score()])
    X_predict_test.insert(0, 'score_basement', [get_basement_score()])
    X_predict_test.insert(0, 'score_age', [get_age_score(Year_Built=Year_Built)])
    X_predict_test.insert(0, 'score_ext_area', [get_ext_area_score(Lot_Area=Lot_Area)])


    pred = model.predict(X_predict_test)

    if 'save' in request.form.keys():
        if request.form['save'] == 'on':
     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_predict = Predict(TotRms_AbvGrd=TotRms_AbvGrd, 
                                    Full_Bath=Full_Bath, 
                                    score_internal=score_internal,
                                    Neighborhood=Neighborhood,
                                    Year_Built=Year_Built,
                                    Lot_Area=Lot_Area,
                                    result= int(pred),
                                    id_user=current_user.id)

            new_predict.save_to_db() 

    return render_template('predict.html', 
        data=int(pred), Neighborhood=request.form['Neighborhood'],
        TotRms_AbvGrd=int(request.form['TotRms_AbvGrd']), 
        Full_Bath=int(request.form['Full_Bath']), 
        score_internal=int(request.form['score_internal']),
        Year_Built=int(request.form['Year_Built']),
        Lot_Area=int(request.form['Lot_Area']))
        # Lot_Area=int(request.form['Lot_Area']), name=current_user.name)


@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    return redirect(render_template('login.html'))   

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)