import json
import unittest

import requests

from models import load_bike_model


def test_api():
    features = {'season': 1, 'yr': 0, 'mnth': 1, 'hr': 16, 'holiday': 0, 'weekday': 6,
            'workingday':0, 'weathersit':2, 'temp':0.42, 'atemp':0.4242, 'hum':0.82, 
            'windspeed':0.2985
            }

    expected_response = {"Casual": 41,	
                         "Registered": 52,	
                         "cnt": 93}
                         },

with models.test_client() as client:
    response = client.get('/', query_string=features)
    assert response.status_code == 200
    assert json.loads(response.data) == expected_response
