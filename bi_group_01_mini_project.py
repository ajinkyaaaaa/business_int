# -*- coding: utf-8 -*-
"""BI group 01 Mini project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qxhp1vEY1GHdngDwKjjzUPDXyoe07ZK0

# Group 01 BI mini project
### Group members:
###### Ajinkya Karnik PD29 1032180678
###### Dhwanit Kapur PD30 1032180715
###### Rushit Patel PE45 1032181258
###### Shrirang Zavar PE38 1032191720
In this study, we examine the Housing Prices in California to figure out what factors influence prices the most. The intelligence will be relevant for the companies to determine the income of the household, which can then be utilized to incorporate targeted ads.
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from plotly import express as px
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'svg')

pd.set_option('max.column', None)

data = pd.read_csv("CaliDataset.csv")

"""# Data Exploration"""

#list down the columns
data.keys()

"""*   Let's check the random ten number of data samples, so we can easly understand the behaviour and what types of data type stored in particular features.



"""

#list down random samples of data
data.sample(10)

"""*   Target Feature"""

#adding target_feature to Y
TARGET_FEATURE = 'median_house_value'

Y = data[TARGET_FEATURE]

Y.head(10)

#gives information about the dataset
data.info()

"""

As we can see in the output.

1.    There are 20640 entries
2.    There are total 10 features (0 to 9)
3.    There are two types of datatype dtypes: float64(8) and object(1)
5.    Also, we can check how many missing values are there in the Non-Null Count column. We can observe that one column has missing values. (total_bedrooms)

"""

#desribes the dataset. gives count, mean, std and box plot values
data.describe()

"""*   Numerical Features"""

numeric_features = data.select_dtypes(['int', 'float']).columns
numeric_features , len(numeric_features)

"""*   Categorical Features"""

categorical_features = data.select_dtypes('object').columns
categorical_features, len(categorical_features)

print("Number of 'Numerical' Features are:", len(numeric_features) )
print("Number of 'Categorical' Features are:", len(categorical_features) )

"""# Data Pre-Processing and ML models"""

missing = data.isna().sum().sort_values(ascending=False)
missing.plot.bar(figsize=(16,5))
plt.xlabel('Columns with missing values')
plt.ylabel('Count')

missing

"""*    Clearly we have to fill some statastical values in the col - total_bedrooms

*   Filling Missing Values
"""

data[['total_bedrooms']].describe(include='all')

"""*   As we can see there is only one feature that has categorical values and rest all have numerical features."""

data['total_bedrooms'] = data['total_bedrooms'].fillna(data['total_bedrooms'].mode()[0])
data.isna().any()

"""*   Getting total number of unique values and removing columns which have huge number of unique values."""

print("Total Records :", len(data) )

for col in categorical_features:
    print("Total Unique Records of "+ col + " =",  len(data[col].unique()))

"""*   Now, we convert categorical values into numerical values."""

data[categorical_features].value_counts()

from sklearn.preprocessing import LabelEncoder
for column in categorical_features:
    l_encoder = LabelEncoder()
    data[column] = l_encoder.fit_transform(data[column])

data.head(10)

training_features = list(numeric_features) + list(categorical_features)

# Remove 'Price' Feature from list
training_features.remove('median_house_value')

# Final list of Training Features
training_features

"""*   Now, we use MinMaxScaler to normalize our dataset."""

from sklearn.preprocessing import MinMaxScaler
minMaxNorm = MinMaxScaler()
minMaxNorm.fit(data[training_features])
X = minMaxNorm.transform(data[training_features]) 
X

Y = data['median_house_value']  
Y

"""Prediction is the data mining task which is needed to solve the problem statement, as we need to predict the price of a house based on several factors like its location, number of bedroom, etc,. As we need to predict a specific price and not a price range, classification is not the major task.

*   Splitting Train and Test Dataset
"""

from sklearn.model_selection import train_test_split
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2)
print("Total size: ", data.shape[0])
print("Train size: ", train_X.shape, train_Y.shape)
print("Test size: ", test_X.shape, test_Y.shape)

models_summary = pd.DataFrame([],
                              columns=['Model_name', 
                                       'Prediction_Score',
                                       'Mean_Absolute_error'
                                      ])
models_summary

from sklearn.ensemble import  AdaBoostRegressor
from sklearn.ensemble import  GradientBoostingRegressor
from sklearn.ensemble import  RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error

ADB_model = AdaBoostRegressor(n_estimators=400, learning_rate=0.25)
ADB_model.fit(train_X,train_Y)
y_train = ADB_model.predict(train_X)
print("The train accuracy score : {} ".format(r2_score(train_Y, y_train)))
y_adb_predict = ADB_model.predict(test_X)
print("The test accuracy score : {} ".format(r2_score(test_Y, y_adb_predict)))
score = ADB_model.score(test_X, test_Y)
score

mae = mean_absolute_error(test_Y, y_adb_predict)
models_summary = models_summary.append({
    'Model_name': ADB_model.__class__.__name__,
    'Prediction_Score': r2_score(test_Y, y_adb_predict),
    'Mean_Absolute_error' : mae
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

Dtree_model = DecisionTreeRegressor(random_state=1, max_depth=6, min_samples_split=6)
Dtree_model.fit(train_X, train_Y)
y_train = Dtree_model.predict(train_X)
print("The train accuracy score : {} ".format(r2_score(train_Y, y_train)))
y_dtree_predict = Dtree_model.predict(test_X)
print("The test accuracy score : {} ".format(r2_score(test_Y, y_dtree_predict)))

models_summary = models_summary.append({
    'Model_name': Dtree_model.__class__.__name__,
    'Prediction_Score': r2_score(test_Y, y_dtree_predict),
    'Mean_Absolute_error' : mean_absolute_error(test_Y, y_dtree_predict)
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

GBR_model = GradientBoostingRegressor(n_estimators=250, random_state=1, learning_rate=0.27, max_depth=6, min_samples_split=6)
GBR_model.fit(train_X, train_Y)
y_train = GBR_model.predict(train_X)
print("The train accuracy score : {} ".format(r2_score(train_Y, y_train)))
y_gbr_predict = GBR_model.predict(test_X)
print("The test accuracy score : {} ".format(r2_score(test_Y, y_gbr_predict)))

models_summary = models_summary.append({
    'Model_name': GBR_model.__class__.__name__,
    'Prediction_Score': r2_score(test_Y, y_gbr_predict),
    'Mean_Absolute_error' : mean_absolute_error(test_Y, y_gbr_predict)
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

RFR_model = RandomForestRegressor(random_state=1,n_estimators=250, max_depth=18, min_samples_split=4)
RFR_model.fit(train_X, train_Y)
y_train = RFR_model.predict(train_X)
print("The train accuracy score : {} ".format(r2_score(train_Y, y_train)))
y_rfr_predict = RFR_model.predict(test_X)
print("The test accuracy score : {} ".format(r2_score(test_Y, y_rfr_predict)))

models_summary = models_summary.append({
    'Model_name': RFR_model.__class__.__name__,
    'Prediction_Score': r2_score(test_Y, y_rfr_predict),
    'Mean_Absolute_error' : mean_absolute_error(test_Y, y_rfr_predict)
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

XGBR_model = XGBRegressor(n_estimators=300, learning_rate=0.15, max_depth=6)
XGBR_model.fit(train_X, train_Y)
y_train = XGBR_model.predict(train_X)
print("The train accuracy score : {} ".format(r2_score(train_Y, y_train)))
y_xgbr_predict = XGBR_model.predict(test_X)
print("The test accuracy score : {} ".format(r2_score(test_Y, y_xgbr_predict)))

models_summary = models_summary.append({
    'Model_name': XGBR_model.__class__.__name__,
    'Prediction_Score': r2_score(test_Y, y_xgbr_predict),
    'Mean_Absolute_error' : mean_absolute_error(test_Y, y_xgbr_predict)
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
xgbr_model = XGBRegressor() # {'objective': 'reg:squarederror' }

params = {
    'n_estimators': [110, 120, 130, 140], 
    'learning_rate': [ 0.05, 0.075, 0.1],
    'max_depth': [ 7, 9],
    'reg_lambda': [0.3, 0.5]
}

xgb_reg = GridSearchCV(estimator=xgbr_model, param_grid=params, cv=5, n_jobs=-1)

xgb_reg.fit(train_X, train_Y)

xgbr_model_score = xgb_reg.best_score_

xgbr_model_pred = xgb_reg.predict(test_X)

mae = mean_absolute_error(test_Y, xgbr_model_pred)

print("Best score: %0.3f" % xgb_reg.best_score_)
print("Best parameters set:", xgb_reg.best_params_)

print("mean_absolute_error :", mae)

models_summary = models_summary.append({
    'Model_name': 'XGBRegressor_HyperParamsTunning',
    'Prediction_Score': xgbr_model_score,
    'Mean_Absolute_error' : mae
}, ignore_index=True)

models_summary.sort_values('Prediction_Score', ascending=False)

"""# Data Visualisation"""

import plotly.express as ex
ex.pie(data,names='ocean_proximity',title='Proportion of Locations of the house w.r.t ocean/sea')

"""We can see here that majority of the houses are close to the sea."""

from pandas.plotting import scatter_matrix
sct_features = ["median_house_value", "median_income","total_rooms","housing_median_age"]
scatter_matrix(data[sct_features],figsize=(12,8))

"""This visualization gives us an idea about the relation of median_house_value with other attributes."""

from plotly.subplots import make_subplots
import plotly.graph_objs as go
fig = make_subplots(1,2)
fig.add_trace(go.Histogram(x=data['median_house_value']),1,1)
fig.add_trace(go.Box(y=data['median_house_value'],boxpoints='all',line_color='orange'),1,2) 
fig.update_layout(height=500, showlegend=False,title_text="Median income distribution and Box Plot")

"""* The correlation matrix shows the relation between median_housing_value and Other Variables."""

corr_mat = data[['housing_median_age','total_rooms','total_bedrooms','population','households']].corr()
f, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(corr_mat, vmax=1 , square=True,annot=True,linewidths=.5);

"""Now, we plot the housing data with respect to the latitude and longitude given. With this, we come to know the population density and the median house vale, which we observe that they go hand-in-hand."""

import matplotlib.image as mpimg

california_img=mpimg.imread('./california.png')

housing_plot = data[['longitude','population','latitude','median_house_value']]
housing_plot.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4,
				s=housing_plot['population']/100, label='population', figsize=(10,7),
				c='median_house_value', cmap=plt.get_cmap('jet'), colorbar=True)


plt.imshow(california_img, extent=[-124.55, -113.80, 32.45, 42.05], alpha=0.5)
plt.ylabel("Latitude", fontsize=14)
plt.xlabel("Longitude", fontsize=14)
plt.legend() 
plt.show()

"""* It helps you to know the density by overlapping the circle if this area have a lot of house there, also other area that have small number of house will be appear because of its opacity will be low.

* Not just alpha, other parameters of the graph can help you discover more pattern


"""

data.plot(kind="scatter", x="longitude", y = "latitude", alpha=.05)