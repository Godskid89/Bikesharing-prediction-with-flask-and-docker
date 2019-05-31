import json
import logging

import numpy as np
from flask import Flask, jsonify, request

from models import load_bike_model

log = logging.getLogger(__name__)
bike_model = load_bike_model()

def get_predicted_class(prediction):
    log.debug(prediction)
    casual, registered, total_user = prediction[0]
    scores = {
        'Casual': casual,
        'Registered': registered,
        'Total User': total_user
    }
    max_score = max(casual, registered, total_user)

    if max_score == casual:
        return 'Casual', scores
    
    if max_score == registered:
        return 'Registered', scores
    
    return 'Total User', scores

# Flask Variables
app = Flask(__name__)

'''
Predicting number of users
'''
@app.route('/', methods=['GET', 'POST'])
def predict():
    res = {
        'status': 'OK',
        'message': 'You have reached Bikesharing API.',
        'help': 'To predict, post your data to this endpoint in JSON format.'
    }

    if request.method == 'POST':
        try:
            features = json.loads(request.form.get('features', '[[]]'))
            features = np.array(features)
            features = features.reshape(1, -1)

            prediction = bike_model.predict(features)
            predicted_class, scores = get_predicted_class(prediction)

            res = {
                'status': 'OK',
                'message': 'Prediction: {}'.format(predicted_class),
                'scores': scores
            }
        except Exception as e:
            log.exception(e)
            res = {
                'status': 'Error',
                'error': str(e)
            }
    
    return jsonify(res)

# Main Method in the Server code
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
