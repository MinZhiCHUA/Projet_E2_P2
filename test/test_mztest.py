from test.conftest import client

def test_should_status_code_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_should_status_code_predict(client):
    response = client.get('/predict')
    assert response.status_code == 200

def test_model_function_predict(client):

    data={'Neighborhood':'GrnHill', 'TotRms_AbvGrd':7, 'Full_Bath':6, 'score_internal':1139, 'Year_Built':1988, 'Lot_Area':186812}

    response = client.post('/predict', data=data)
    assert response.status_code == 200

