import pandas as pd
import numpy as np

column = ['song_id','up_votes/total_votes','up_votes','down_votes','difficulty', 'notes', 'bombs','BPM','obstacles','NJS','NJSOffset','length','duration']

def dictSchema():
  data_schema = { 'song_id': int,
                  'up_votes/total_votes': float,
                  'up_votes': int,
                  'down_votes': int,
                  'difficulty': int,
                  'notes': int,
                  'bombs': int,
                  'BPM': float,
                  'obstacles': int,
                  'NJS': int,
                  'NJSOffset': float,
                  'length': int,
                  'duration': float}
  return data_schema

def cleanDictionary(rawDict):
  cleanDict = rawDict[column]
  cleanDict = cleanDict.astype(dictSchema())
  return cleanDict

def columns():
  return column

