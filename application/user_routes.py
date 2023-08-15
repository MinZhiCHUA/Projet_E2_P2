from flask import Blueprint
from flask import Flask, render_template, request
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

from flask_login import login_user, login_required, logout_user, current_user

# from .forms import LoginForm, PredictionForm

from werkzeug.security import generate_password_hash, check_password_hash
from application.models import User, Predict
#from . import db

import numpy as np
import pandas as pd
import joblib
from .feature_eng_func import *
from .extension import db

# from application import app

# from application.models import *

# from application import create_app
# app = create_app()

# with app.app_context():
#     #user = db.engine.table_names()

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(email="email2", name="name22222", password=generate_password_hash("password", method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()
    
#     user = User.query.filter_by(name="name").all()
# print(user)


model = joblib.load(open('application/better_model_lasso.joblib', 'rb'))
db = SQLAlchemy()
auth = Blueprint('auth', __name__)

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    print ('starting the signing up')
    # code to validate and add user to database goes here
    email = request.form.get('email')
    print(email)
    name = request.form.get('name')
    print(name)
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    new_user.save_to_db()

    # add the new user to the database
    # db.session.add(new_user)
    # db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
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
    # return redirect(url_for('main.profile'))
    return render_template('index.html', name=current_user.name)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/predict')
def predict():
    # return render_template('predict.html', name=current_user.name)
    return render_template('predict.html')


@auth.route('/predict', methods=['POST'])
# @login_required
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

@auth.route('/history', methods=['GET'])
# @login_required
def history():

    # perdict_lst = Predict.query.filter_by(id_user=current_user.id).with_entities(Predict.result).all()
    # print (perdict_lst)
    title = ['Construction Year', 'Lot size (SF)', 'Living area (SF)','Number of rooms', 'Number of bathrooms', 'Neighborhood', 'Predicted house price']
    predict_list=[]
    for prediction in Predict.query.filter_by(id_user=current_user.id).with_entities(Predict.id,
                                                                                        Predict.id_user,
                                                                                        Predict.Year_Built,
                                                                                        Predict.Lot_Area,
                                                                                        Predict.score_internal,
                                                                                        Predict.TotRms_AbvGrd,
                                                                                        Predict.Full_Bath,
                                                                                        Predict.Neighborhood,
                                                                                        Predict.result,).all():

    # for prediction in Predict.query.filter_by(id_user=current_user.id).all():
        # print( prediction)
        predict_list.append(prediction)

    # print (predict_list)
    # return render_template('predict.html', name=current_user.name)
    return render_template('history.html', lenght=len(title), title=title, predict_list=predict_list)

@auth.route('/predict_delete', methods=['GET','POST'])
def predict_delete():

    print('delete function')

    predict_id = request.args.get('id')
    print(predict_id)
    
    Predict.query.filter_by(id=predict_id).first().delete_from_db()
    # print(answer)

    return redirect(url_for('auth.history'))