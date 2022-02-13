#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:28:03 2020

@author: michaelmitschjr
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score 

filename = '../data/1000_samples_.csv'

df = pd.read_csv(filename)

best_scores = {'linear regression':[-1,-5],'SVR regression':[-1,-5],'ridge regression':[-1,-5],'knn regression':[-1,-5],'tree regression':[-1,-5]}

for i in range(50,70):
   data = df[df.up_votes+df.down_votes > i].values
   data = data[:,1:]

   data[:,5:] = normalize(data[:,5:])
   x_train, x_test, y_train, y_test = train_test_split(data[:,5:], data[:,1], test_size=0.25, random_state=9)

   reg = LinearRegression().fit(x_train,y_train)
   score = reg.score(x_test,y_test)
   if best_scores['linear regression'][1] < score:
      best_scores['linear regression'][1] = score
      best_scores['linear regression'][0] = i
   
   clf = SVR(gamma = 'scale')
   clf.fit(x_train, y_train)
   score = clf.score(x_test,y_test)
   
   if best_scores['SVR regression'][1] < score:
      best_scores['SVR regression'][1] = score
      best_scores['SVR regression'][0] = i
      
   clf = Ridge(alpha=1.0)
   clf.fit(x_train, y_train)
   score = clf.score(x_test,y_test)
   
   if best_scores['ridge regression'][1] < score:
      best_scores['ridge regression'][1] = score
      best_scores['ridge regression'][0] = i
   
   neigh = KNeighborsRegressor(n_neighbors=2)
   neigh.fit(x_train,y_train)
   score = neigh.score(x_test,y_test)
   
   if best_scores['knn regression'][1] < score:
      best_scores['knn regression'][1] = score
      best_scores['knn regression'][0] = i
   
   tree_model= DecisionTreeRegressor(max_depth=5, max_leaf_nodes = 20);
   tree_model.fit( x_train, y_train ); 
   prediction = tree_model.predict( x_test )
   
   score = r2_score( y_test, prediction)
   
   if best_scores['tree regression'][1] < score:
      best_scores['tree regression'][1] = score
      best_scores['tree regression'][0] = i

for mod in best_scores:
   best_scores[mod][1] = round(best_scores[mod][1],2)
print(best_scores)