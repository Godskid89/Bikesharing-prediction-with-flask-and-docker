import os

import pandas as pd
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, 'dataset', 'hour.csv')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'MLPmodel.pk')

def train_bike_model():
    rides = pd.read_csv(DATA_PATH)

    fields_to_drop = ['instant', 'dteday']
    data = rides.drop(fields_to_drop, axis=1)

    features = data.columns[:-3]
    target = data.columns[-1]

    print ("Feature Column(s):\n{}\n".format(features))
    print ("Target Column:\n{}".format(target))

    #Standardization of continuous numerical variables. 
    quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']

    for each in quant_features:
        mean, std = data[each].mean(), data[each].std()
        data.loc[:, each] = (data[each] - mean)/std

    target_fields = ['cnt', 'casual', 'registered']

    X = data.drop(target_fields, axis=1)
    y = data[target_fields]

    # Split the data set into training, testing and validation datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    print("train set: ", X_train.shape)
    print("test set: ", X_test.shape)

    MLPmodel = MLPRegressor(hidden_layer_sizes=(40,), learning_rate='adaptive',max_iter=20000)
    MLPmodel.fit(X_train, y_train)
    y_MLPmodel_pred = MLPmodel.predict(X_test)

    print("model: MLPRegressor, Test score: ", MLPmodel.score(X_test,y_test))
    print("model: MLPRegressor, MAE: ", metrics.mean_absolute_error(y_test, y_MLPmodel_pred))

    joblib.dump(MLPmodel, MODEL_PATH)

def load_bike_model():
    if not (os.path.exists(MODEL_PATH) and os.path.isfile(MODEL_PATH)):
        train_bike_model()
    
    return joblib.load(MODEL_PATH)
