from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib
from .feature_eng_func import *

app = Flask(__name__)
# model = joblib.load(open('model.joblib', 'rb'))
model = joblib.load(open('application/better_model_lasso.joblib', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict_post():

    X_predict_test=pd.DataFrame()

    print(request.form['Lot_Area'])
# Year_Built=int(request.form['Year_Built']
# Lot_Area=int(request.form['TotRms_AbvGrd'])

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

    # print(X_predict_test)

    pred = model.predict(X_predict_test)
    # model.predict(X_predict_test)
    
    # X_predict = {}
    # for var in ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area','Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
    #           'Kitchen_Qual', 'Neighborhood']:
    #     if var in ['Exter_Qual','Kitchen_Qual', 'Neighborhood']:
    #         X_predict[var]= request.form[var]
    #     else:
    #         X_predict[var]= int(request.form[var])

    # pred = model.predict(pd.DataFrame(X_predict, index=[0]))

    # pred = 99999999
    # return render_template('predict.html', data=int(pred))
    return render_template('predict.html', 
        data=int(pred), Neighborhood=request.form['Neighborhood'],
        TotRms_AbvGrd=int(request.form['TotRms_AbvGrd']), 
        Full_Bath=int(request.form['Full_Bath']), 
        score_internal=int(request.form['score_internal']),
        Year_Built=int(request.form['Year_Built']),
        Lot_Area=int(request.form['Lot_Area']))




if __name__ == '__main__':
    app.run(debug=True)
