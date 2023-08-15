from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)
model = joblib.load(open('model.joblib', 'rb'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    X_predict = {}
    for var in ['Year_Built', 'Total_Bsmt_SF', '1st_Flr_SF', 'Gr_Liv_Area','Garage_Area', 'Overall_Qual', 'Full_Bath', 'Exter_Qual',
              'Kitchen_Qual', 'Neighborhood']:
        if var in ['Exter_Qual','Kitchen_Qual', 'Neighborhood']:
            X_predict[var]= request.form[var]
        else:
            X_predict[var]= int(request.form[var])

    pred = model.predict(pd.DataFrame(X_predict, index=[0]))

    return render_template('index.html', data=int(pred))


if __name__ == '__main__':
    app.run(debug=True)
