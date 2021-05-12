# -*- coding: utf-8 -*-
"""HousePrediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hYrJsOAB5PILYDE4oD5f3_wqm9IIHA8K
"""

ls

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

house_data=pd.read_csv('train.csv')
house_data.head()

house_data.shape

house_data.columns

house_data['LotFrontage'].isnull().sum()

house_data['LotFrontage'].isnull().mean()

features_null=[features for features in house_data.columns if house_data[features].isnull().sum()>1]
features_null

for feature in features_null:
  print(feature,np.round(house_data[feature].isnull().mean()*100,2))

for feature in features_null:
  data=house_data.copy()
  data[feature]=np.where(data[feature].isnull(),1,0)
  #print(data[feature],'printing 1 if null')
  data.groupby(feature)['SalePrice'].mean().plot.bar()
  plt.title(feature)
  plt.show()

house_data['Exterior1st'].dtype

numerical_features=[feature for feature in house_data.columns if house_data[feature].dtype !='O']
numerical_features

discrete_features=[feature for feature in numerical_features if len(house_data[feature].unique())<30]
discrete_features

continous_feature=[feature for feature in numerical_features if feature not in discrete_features]
continous_feature

for feature in discrete_features:
  data=house_data.copy()
  data.groupby(feature)['SalePrice'].mean().plot.bar()
  plt.title(feature)
  plt.xlabel(feature)
  plt.ylabel('SalePrice')
  plt.show()

for feature in discrete_features:
  data=house_data.copy()
  data[feature].hist()
  plt.title(feature)
  plt.xlabel(feature)
  plt.ylabel('SalePrice')
  plt.show()

categorical_features=[feature for feature in house_data.columns if house_data[feature].dtype=='O']
categorical_features

for feature in categorical_features:
  data=house_data.copy()
  data.groupby(feature)['SalePrice'].mean().plot.bar()
  plt.title(feature)
  plt.show()

house_data[categorical_features]=house_data[categorical_features].fillna('Missing')

house_data[categorical_features].head()

for feature in numerical_features:
  house_data[feature]=house_data[feature].fillna(house_data[feature].median())

house_data[numerical_features].isnull().sum()

year_feature = [feature for feature in numerical_features if 'Yr' in feature or 'Year' in feature]
year_feature

house_data['current_year']=2021

house_data['Number of years built']=house_data['current_year']-house_data['YearBuilt']
house_data['Number of years sold']=house_data['current_year']-house_data['YrSold']
house_data['Number of years RemodAdd']=house_data['current_year']-house_data['YearRemodAdd']
house_data['Number of years GarageYrBlt']=house_data['current_year']-house_data['GarageYrBlt']
house_data.drop(['YearBuilt', 'YearRemodAdd', 'GarageYrBlt', 'YrSold','current_year'],axis=1,inplace=True)

house_data.head()

house_data.drop(['Id'],axis=1,inplace=True)

house_data=pd.get_dummies(house_data,drop_first=True)
house_data.head()

X=house_data.drop(['SalePrice'],axis=1)
y=house_data[['SalePrice']]

from sklearn.model_selection import train_test_split
train_x,test_x,train_y,test_y=train_test_split(X,y,test_size=0.2,random_state=0)

from sklearn import svm

regr=svm.SVR(kernel='rbf')
regr.fit(train_x,train_y)

y_pred=regr.predict(test_x)

from sklearn import metrics

print('MAE:', metrics.mean_absolute_error(test_y, y_pred))
print('MSE:', metrics.mean_squared_error(test_y, y_pred))
print('RMSE:', np.sqrt(metrics.mean_squared_error(test_y, y_pred)))