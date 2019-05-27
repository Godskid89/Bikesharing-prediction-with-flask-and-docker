import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
import pickle


data_path = 'dataset/hour.csv'
rides = pd.read_csv(data_path)

rides[:24*10].plot(x='dteday', y='cnt')

#Creating Dummy variable
dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
for each in dummy_fields:
    dummies = pd.get_dummies(rides[each], prefix=each, drop_first=False)
    rides = pd.concat([rides, dummies], axis=1)

fields_to_drop = ['instant', 'dteday', 'season', 'weathersit', 
                  'weekday', 'atemp', 'mnth', 'workingday', 'hr']
data = rides.drop(fields_to_drop, axis=1)
data.head()

#Standardization of continuous numerical variables. 
quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']

scaled_features = {}
for each in quant_features:
    mean, std = data[each].mean(), data[each].std()
    scaled_features[each] = [mean, std]
    data.loc[:, each] = (data[each] - mean)/std

target_fields = ['cnt', 'casual', 'registered']

X = data.drop(target_fields, axis=1)
y = data[target_fields]

# Split the data set into training, testing and validation datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
print("train set: ", X_train.shape)
print("test set: ", X_test.shape)


MLPmodel = MLPRegressor(hidden_layer_sizes=(40,), learning_rate='adaptive',max_iter=17000).fit(X_train, y_train)
y_MLPmodel_pred = MLPmodel.predict(X_test)

print("model: MLPRegressor, Test score: ", MLPmodel.score(X_test,y_test))
print("model: MLPRegressor, MAE: ", metrics.mean_absolute_error(y_test, y_MLPmodel_pred))


filename = 'MLPmodel.pk'
with open('models/'+filename, 'wb') as file:
    pickle.dump(MLPmodel, file)