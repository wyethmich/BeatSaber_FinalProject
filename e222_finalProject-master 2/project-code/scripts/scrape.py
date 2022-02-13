#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:28:20 2020

@author: michaelmitschjr
"""
import requests
import pandas as pd
import numpy as np
import time

#test url
#url = 'https://beatsaver.com/api/maps/detail/6777'

url = 'https://beatsaver.com/api/maps/detail/'

#fake user agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#use duration from metadata
#duration starts at 71d0
#difficultys: 0 = easy, 1 = normal, 2 = hard, 3 = expert, 4 = expert+
diff_dict = {'easy':0,'normal':1,'hard':2,'expert':3,'expertPlus':4}
columns = ['song_id','up_votes/total_votes','up_votes','down_votes','difficulty', 'notes', 'bombs','BPM','obstacles','NJS','NJSOffset','length','duration']

def scrape(start,stop):
   '''
   Inputs: start value given as a hex string. example: '82db'
           stop value given as a hex string. example: '8340'
   
   Outputs a 13 column dataframe with information on the beat saber maps from start to stop
   
   This scrapes the web so there is delay to gather data
   '''
   data = np.zeros((1,len(columns)))
   
   start = int(start,16)
   stop = int(stop,16)
   if stop > 39000: #there are ~39000 songs right now
      stop = 39000
   count = 0
   not_count = 0
   # testing song IDs 0x82db - 0x833f 
   for i in range(start, stop+1):
   
      time.sleep(.1)
      
      #search for the url with hex song id appended to the end
      r = requests.get(url+hex(i).split('x')[1],headers = headers)
      
      if r.status_code != 200: #status code 200 is success. Move to another url on failure
         not_count += 1
         #print("bad status", r.status_code, ", for the", not_count,'time')
         continue
      #Parse strings to get them in format of a Python dictionary
      string_dictionary = r.text
      string_dictionary = string_dictionary.replace('false','False')
      string_dictionary = string_dictionary.replace('true','True')
      string_dictionary = string_dictionary.replace('null','None')
      
      dictionary = eval(string_dictionary)
      
      for dif in dictionary['metadata']['difficulties']:
         
         if dictionary['metadata']['difficulties'][dif] == True and dictionary['stats']['upVotes'] + dictionary['stats']['downVotes'] != 0:
            try: #using try execp in case there is an unexpected structure
               ls = [int(dictionary['key'],16), #song number (as decimal integer)
                  (dictionary['stats']['upVotes']/(dictionary['stats']['upVotes']+dictionary['stats']['downVotes'])), #ratio upvotes/total votes
                  dictionary['stats']['upVotes'], #up votes
                  dictionary['stats']['downVotes'], #down votes               
                  diff_dict[dif], #difficulty
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['notes'], #notes
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['bombs'], #bombs
                  dictionary['metadata']['bpm'], #BPM
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['obstacles'], #obstacles
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['njs'], #njs
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['njsOffset'], #njs offset
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['length'], #length
                  dictionary['metadata']['characteristics'][0]['difficulties'][dif]['duration'] #duration                            
                  ]
            except: #move to a different url
               #print("failed")
               continue
            data = np.append(data,[ls],axis=0)
            
            count += 1
            #print("added", count, 'things to data')           
   #Turn data into a dataFrame
   df = pd.DataFrame(data[1:], columns = columns) 
   #df.to_csv('../../data_sets/1000_samples_.csv')
   return df
