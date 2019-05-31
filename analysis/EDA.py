import calendar as cal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pandas import DataFrame

# Fetching Dataset
bike_data = pd.read_csv("dataset/hour.csv")

# Calculating the Mean Absolute Deviation for the targetted variables
series = pd.Series(bike_data['casual'])
mad_cas = series.mad()

series = pd.Series(bike_data['registered'])
mad_reg = series.mad()

series = pd.Series(bike_data['cnt'])
mad_cnt = series.mad()

MAD_table = {'Targetted Features': ['Casual','Registered','Count'],
        'Mean Absolute Deviation': [mad_cas,mad_reg,mad_cnt]
        }

df = DataFrame(MAD_table,columns= ['Targetted Features', 'Mean Absolute Deviation'])

print (df)

#Mapping the variables with their actual values
bike_data['season'] = bike_data['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
bike_data['weekday'] = bike_data['weekday'].map({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})

bike_data['weathersit'] = bike_data['weathersit'].map({
    1: 'Clear, Few clouds, Partly cloudy, Partly cloudy',
    2: 'Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist',
    3: 'Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds',
    4: 'Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog'
})
column_indices = [1, 3, 4, 5, 10, 11, 12]
new_names = ['dateday','year','month','hour','temperature','humidity']
old_names = bike_data.columns[column_indices]
bike_data.rename(columns=dict(zip(old_names, new_names)), inplace=True)

category_list = ['hour','weekday', 'month', 'season', 'weathersit', 'holiday', 'workingday']

for cat in category_list:
    bike_data[cat] = bike_data[cat].astype('category')

# Handling outliers
bike_data = bike_data[np.abs(bike_data['cnt'] - bike_data['cnt'].mean()) <= (3 * bike_data['cnt'].std())]
# Data Visualization
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(19.20, 10.80))

# Avg. Count by month

months = []
for i in range(1, 13):
    months.append(cal.month_name[i])
month_avg = pd.DataFrame(bike_data.groupby('month')['cnt'].mean()).reset_index()
f1 = sns.barplot(x='month', y='cnt', data=month_avg, ax=axs[0][0])
for i in f1.get_xticklabels():
    i.set_rotation(35)
axs[0][0].set(xlabel='Month', ylabel='Average Count', title='Average Count by Month')

# Avg. User count by hour of day across seasons
hour_avg = pd.DataFrame(bike_data.groupby(['hour', 'season'])['cnt'].mean()).reset_index()
sns.pointplot(x='hour', y='cnt', hue='season', data=hour_avg, ax=axs[0][1])
axs[0][1].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Seasons')

# Avg. User count by hour of day across weekdays
weekday_avg = pd.DataFrame(bike_data.groupby(['hour', 'weekday'])['cnt'].mean()).reset_index()
sns.pointplot(x='hour', y='cnt', hue='weekday', data=weekday_avg, ax=axs[1][0])
axs[1][0].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Weekdays')

# Avg. User count by hour of day across users

users_avg = pd.melt(bike_data[['hour', 'casual', 'registered']], id_vars=['hour'], value_vars=['casual', 'registered'],
                    var_name='users', value_name='cnt')
users_avg = pd.DataFrame(users_avg.groupby(['hour', 'users'])['cnt'].mean()).reset_index()
sns.pointplot(x='hour', y='cnt', hue='users', data=users_avg, ax=axs[1][1])
axs[1][1].set(xlabel='Hour', ylabel='Average Count', title='Average Count by Hour of day across Users')

plt.savefig('analysis/data.jpg')