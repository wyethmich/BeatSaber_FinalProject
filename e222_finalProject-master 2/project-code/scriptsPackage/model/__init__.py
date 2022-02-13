#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:14:24 2020

@author: michaelmitschjr
"""
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import normalize
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import io



def ready_data(df,min_votes=60):
   '''
   takes a DataFrame of the data and a minimum amount of votes to train/test on
      weeds out accounts with total votes < min_votes
      creates an np array of the data
      normalizes each feature in the data
   returns numpy ndarray of normalized data set with instances that have more than min_votes votes      
   '''
   data = df[df.up_votes+df.down_votes > min_votes].values
   data = data[:,1:]
   data[:,5:] = normalize(data[:,5:])  
   return data

def split_data(data):
   x_train, x_test, y_train, y_test = train_test_split(data[:,5:], data[:,1], test_size=0.25, random_state=9)
   return x_train, x_test, y_train, y_test

def tree_regression(x_train, x_test, y_train, y_test,max_depth = 5):
   '''
   takes in date (np ndarray)
      splits data into test and training sets
      trains decision tree regression on train data
      gets R2 score for model predictions on test data
   returns trained model, R2 score for the model
   '''
   #x_train, x_test, y_train, y_test = train_test_split(data[:,5:], data[:,1], test_size=0.25, random_state=9)
   tree_model= DecisionTreeRegressor(max_depth = max_depth, max_leaf_nodes = 20)
   tree_model.fit( x_train, y_train )
   prediction = tree_model.predict( x_test )
   
   score = r2_score( y_test, prediction)

   return tree_model, score

def charts(tree_model,x_test,y_test):
   prediction = tree_model.predict(x_test)
   f, plots = plt.subplots(3,2,figsize=(10,20))  
   x_axes = [[[0,"Notes"],[1,"Bombs"]],
             [[2,"BPM"],  [3,"Obstacles"]],
             [[4,"NJS"],  [5,"Length"]]
            ] 
   for i in range(3):
      for j in range(2):
         plots[i,j].scatter(x_test[:,x_axes[i][j][0]], y_test, s=20, edgecolor="black",c="darkorange", label="data")
         plots[i,j].scatter(x_test[:,x_axes[i][j][0]], prediction, color="cornflowerblue",label="decision tree regression (depth=3)")
         plots[i,j].set(xlabel = x_axes[i][j][1],ylabel = "upvotes/votes")
         plots[i,j].set_title("Prediction and " + x_axes[i][j][1])
         plots[i,j].legend()
   #f.savefig('plots.png')
   bytes_image = io.BytesIO()
   bytes_image
   f.savefig(bytes_image, format='png')
   bytes_image.seek(0)
   return bytes_image
'''
in the main app part:
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

in the html:
<img src="/plot.png" alt="my plot">
'''


'''
#testing
filename = '../data/1000_samples_.csv'

df = pd.read_csv(filename)

data = ready_data(df)

x_train, x_test, y_train, y_test = split_data(data)

model, score = tree_regression(x_train, x_test, y_train, y_test)

print(score)

charts(model,x_test,y_test)
'''