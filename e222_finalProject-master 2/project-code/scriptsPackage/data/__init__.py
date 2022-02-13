#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 13:30:40 2020

@author: michaelmitschjr

Imports data from csv in google that is viewable by anyone
"""
import requests
import io
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.svm import SVC
from os import listdir
from flask import Flask, request, send_file, make_response

#will remove when input.txt is set up
#url = 'https://drive.google.com/uc?export=download&id=1DHGZ82GJJA4kLwRqjurEv419tnkcjaNW'

features = ['song_id','up_votes/total_votes','up_votes','down_votes','difficulty','notes','bombs','BPM','obstacles','NJS','NJSOffset','length','duration']

code_dir = os.path.dirname(__file__)

def input_url(id):
   #takes id of google file and writes a link to that file in input
   input_path = code_dir+'/input/input.txt'
   link = 'https://drive.google.com/uc?export=download&id=' + id
   with open(input_path, "w") as f:
      f.write(link)
   return("Input URL changed to " + link) #this should be 

def get_url():
   ''' 
   takes no input
   reads the contents of /input/input.txt and returns that as a string
   '''
   input_path = code_dir+'/input/input.txt'
   input_file = open(input_path, "rt")
   contents = input_file.read()
   url = contents.rstrip()
   input_file.close()
   return str(url)

def google_data():
   '''
   takes no input
   returns a dataframe of data in the google file at the url that get_url returns
   '''
   url = get_url()
   r = requests.get(url, allow_redirects=True)
   string_csv = r.content.decode('utf-8').split('\n')
   data = [eval('['+line+']')[1:] for line in string_csv[1:len(string_csv)-1]]
   df = pd.DataFrame(data, columns = features) 
   return df

def google_data_Server(id):
   url = 'https://drive.google.com/uc?export=download&id=' + id
   r = requests.get(url, allow_redirects=True)
   string_csv = r.content.decode('utf-8').split('\n')
   data = [eval('['+line+']')[1:] for line in string_csv[1:len(string_csv)-1]]
   df = pd.DataFrame(data, columns = features) 
   return df

def load_data(id):
   # Server use cant use local files so natively assemble url in the request 
   return google_data_Server(id)
   #combination of previous functions
   #input_url(id)
   #return google_data()

'''
questions:
   what is the link so that it does not download? bc i dont need to download it i just have to get contents
   
   what file/function sets up input.txt in the example?
'''