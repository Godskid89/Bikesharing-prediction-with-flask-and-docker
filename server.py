from gevent import monkey
import json
from flask import Flask, request, Response, render_template, abort, url_for, jsonify
import gevent
from sklearn.externals import joblib
#from flask_httpauth import HTTPDigestAuth
import pandas as pd
import traceback
import numpy as np

# Flask Variables
app = Flask(__name__)

# # Randomised SVR for Casual Users 
# svr_cas = joblib.load('models/models_new_cas.pk')
# # Randomised SVR for Regular Users 
# svr_reg = joblib.load('models/models_new_reg.pk')

bike_model = joblib.load('models/MLPmodel.pk')

# Monkey Patch the server
monkey.patch_all()

'''
Predicting number of casual and regular users
'''
@app.route('/predict', methods=['POST'])
def predict():
    print(request.json)
    features = request.json['data']
    features = np.array(features);
    features = features.reshape(1, -1)
    print(bike_model.predict(features))
    r = {
        'b_model': bike_model.predict(features)[0]
        # 'y_reg': svr_reg.predict(features)[0]
    }
    return json.dumps(r)

'''
Home Page which describes the visualisation and the 
necessary input and output for the same
'''
@app.route('/')
def index():
    return render_template('index.html')

# Main Method in the Server code
if __name__ == '__main__':
    # Set server address 0.0.0.0:5000/
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
