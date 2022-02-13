import scrape
import mongoInterface as mi
import model as mDriver
import data as googData
from pandas import DataFrame

from flask import send_file,jsonify
import json

def availMaps():
  jsonRet = {}
  songList = []

  dbRet = mi.getAllMaps()
  if isinstance(dbRet, DataFrame):
    # Jsonifys the dataframe to a managable format similar to a beatsaver api response
    for i in range(dbRet.shape[0]):
      songData = {'song_id': dbRet.at[i,'song_id'],
                  'difficulty': int(dbRet.at[i,'difficulty']),
                  'up_votes/total_votes': dbRet.at[i,'up_votes/total_votes'],
                  'up_votes': int(dbRet.at[i,'up_votes']),
                  'down_votes': int(dbRet.at[i,'down_votes']),
                  'notes': int(dbRet.at[i,'notes']),
                  'bombs': int(dbRet.at[i,'bombs']),
                  'BPM': dbRet.at[i,'BPM'],
                  'obstacles': int(dbRet.at[i,'obstacles']),
                  'NJS': int(dbRet.at[i,'NJS']),
                  'NJSOffset': dbRet.at[i,'NJSOffset'],
                  'length': int(dbRet.at[i,'length']),
                  'duration': dbRet.at[i,'duration']}
      songList.append(songData)

    jsonRet['availSongs'] = songList
  else:
      jsonRet['availSongs'] = dbRet
  return jsonRet

def availModels():
  jsonRet = {}
  modelsInfo = mi.getAllModels()
  jsonRet['models'] = modelsInfo
  return jsonRet

def runPrediction(modelName):
  theModel = mi.getModel(modelName) # Same name as stored in db
  data = mi.getAllMaps()
  data = mDriver.ready_data(data)
  x_train, x_test, y_train, y_test = mDriver.split_data(data)
  byte_image = mDriver.charts(theModel,x_test,y_test)
  return send_file(byte_image, attachment_filename='plot.png', mimetype='image/png')

def getNewBeatSaverMaps(startKey, stopKey):
  newData = scrape.scrape(startKey,stopKey)
  log = mi.saveMapData(newData)
  return {'retrevalLog': log}

def importDataFromGoogle(urlID):
  newData = googData.load_data(urlID)
  log = mi.saveMapData(newData)
  return {'databaseLog': log}

def trainModel(modelName):
  data = mi.getAllMaps()
  data = mDriver.ready_data(data)
  x_train, x_test, y_train, y_test = mDriver.split_data(data)
  model, score = mDriver.tree_regression(x_train, x_test, y_train, y_test)
  details = mi.saveModel(model,modelName)
  return jsonify({"msg": "Model Trained and Saved!"})

