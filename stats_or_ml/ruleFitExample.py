from sklearn.datasets import load_boston
from rulefit import RuleFit


data = load_boston()
features = data.feature_names
X = data.data
y = data.target

# rf = RuleFit()
# rf.fit(X, y, feature_names=features)


from sklearn.ensemble import GradientBoostingRegressor
gb = GradientBoostingRegressor(n_estimators=500, max_depth=10, learning_rate=0.01)
rf = RuleFit(tree_generator=gb)

rf.fit(X, y, feature_names=features)


rf.predict(X)



rules = rf.get_rules()

rules = rules[rules.coef != 0].sort_values("support", ascending=False)

print(rules)








import sys
# sys.path.insert(0,'/home/chris/Documents/Real-Estate/keras-multi-input')
sys.path.insert(0,'C:/Users/cdurrans/Documents/Real-Estate/keras-multi-input')
import seaborn as sns
import diagnosticPlotLinearRegression as diag_plots
from pyimagesearch import datasets
import pandas as pd
from sklearn.model_selection import train_test_split
import locale
import os
import matplotlib
import numpy as np
import re
from matplotlib import pyplot as plt
import sqlite3
from catboost import CatBoostRegressor

def metricsReport(y_test,y_pred):
    from sklearn.metrics import mean_squared_error, explained_variance_score, r2_score, mean_absolute_error
    print('RMSE ',  (mean_squared_error(y_test, y_pred)**0.5))
    print('explained variance score ',explained_variance_score(y_test, y_pred))
    print('r2score ',r2_score(y_test, y_pred))
    print('MAE ',mean_absolute_error(y_test, y_pred))

def predVsActualPlot(y_test,y_pred,title="Measure Vs Predicted"):
    import matplotlib.pyplot as plt
    # Visualising the Training set results
    fig, ax = plt.subplots()
    ax.scatter(y_test, y_pred, alpha=0.1)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.title(title)
    plt.show()

base_file_location = "C:/Users/cdurrans/Desktop/"
fileSaveLocation = 'UtahHousingCleanedCombined.csv'
file =  base_file_location + fileSaveLocation

y_var = 'Estimate Mortgage'
continousList = ['acres', 'Beds','SqFt', 'Baths','schoolAvgRating','avgDistanceToSchools','Year Built','sqft_floor1','sqft_floor2','sqft_basement']
categoricalList = ['city_st_zip']

df = pd.read_csv(file)
df = df[~df[y_var].isnull()].copy()

from sklearn.preprocessing import LabelEncoder
labelencoder_X_1 = LabelEncoder()
df[categoricalList[0]] = labelencoder_X_1.fit_transform(df[categoricalList[0]])

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(df[continousList+categoricalList], df[y_var], test_size = 0.2, random_state = 0)
X_train, X_test, y_train, y_test = train_test_split(df[continousList], df[y_var], test_size = 0.2, random_state = 0)




features = X_train.columns
X = X_train.values
y = y_train.values

# rf = RuleFit()
# rf.fit(X, y, feature_names=features)


from sklearn.ensemble import GradientBoostingRegressor
gb = GradientBoostingRegressor(n_estimators=500, max_depth=10, learning_rate=0.01)
rf = RuleFit(tree_generator=gb)

rf.fit(X, y, feature_names=features)




preds = rf.predict(X_test.values)

predVsActualPlot(y_test.values,preds)


rules = rf.get_rules()

rules = rules[rules.coef != 0].sort_values("support", ascending=False)

print(rules)



