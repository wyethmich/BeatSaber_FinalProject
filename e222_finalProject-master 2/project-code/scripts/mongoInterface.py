import pymongo
import csvHandler as fiHandl
import pandas as pd
import numpy as np
from pymongo import MongoClient
import pandasCleaning as pdClean
import hashlib
import pickle
from datetime import datetime

# To setup a local db for testing use
# docker run -d -p 27017-27019:27017-27019 --net-alias mongodb --name mongodb mongo
# To stop the instance
# docker stop mongodb
# To start instance again
# docker start mongodb

column = ['song_id','up_votes/total_votes','up_votes','down_votes','difficulty', 'notes', 'bombs','BPM','obstacles','NJS','NJSOffset','length','duration']

client = MongoClient('mongodb', 27017)
db = client.songDatabase
coll = db.songData
dbMdls = db.savedModels

def saveMapData(pandasDataFrame):
  dataDict = pdClean.cleanDictionary(pandasDataFrame)
  funcLog = ''
  #songHashes = cleanDict.apply(lambda x: hash(tuple(x)), axis = 1)

  for i in range(dataDict.shape[0]):
    # _id is the hash of all of the data from that document. Prevents duplicate entries
    # difficulty: easy = 0 and increases to expertPlus = 4
    try:
      entryData = ''.join(map(str,[dataDict.at[i,'song_id'], dataDict.at[i,'difficulty']]))
      #entryData = ''.join(map(str,dataDict.iloc[i].values))
      entryHash = hashlib.md5(entryData.encode())

      # assemble document to enter into mongo
      document = {'_id': entryHash.hexdigest(),
                  'song_id': format(int(dataDict.at[i,'song_id']),'x'),
                  'up_votes/total_votes': dataDict.at[i,'up_votes/total_votes'],
                  'up_votes': int(dataDict.at[i,'up_votes']),
                  'down_votes': int(dataDict.at[i,'down_votes']),
                  'difficulty': int(dataDict.at[i,'difficulty']),
                  'notes': int(dataDict.at[i,'notes']),
                  'bombs': int(dataDict.at[i,'bombs']),
                  'BPM': dataDict.at[i,'BPM'],
                  'obstacles': int(dataDict.at[i,'obstacles']),
                  'NJS': int(dataDict.at[i,'NJS']),
                  'NJSOffset': dataDict.at[i,'NJSOffset'],
                  'length': int(dataDict.at[i,'length']),
                  'duration': dataDict.at[i,'duration']}
      coll.insert_one(document)
      funcLog = funcLog + "Added SongID: {} Diff: {}\n".format(format(int(dataDict.at[i,'song_id']),'x'), dataDict.at[i,'difficulty'])
    except pymongo.errors.DuplicateKeyError:
      funcLog = funcLog + "SongID: {} Diff: {} already present! Comparing New data ".format(format(int(dataDict.at[i,'song_id']),'x'), dataDict.at[i,'difficulty'])
      songHashQuery = {'_id': entryHash.hexdigest()}
      currEntry = coll.find_one(songHashQuery)
      if (currEntry['up_votes'] < dataDict.at[i,'up_votes']) or (currEntry['down_votes'] < dataDict.at[i,'down_votes']):
        # Update the database with new data if lower than given
        funcLog = funcLog + "== <<New Data>> Updating Database...\n"
        newValues = { "$set": { 'up_votes/total_votes': dataDict.at[i,'up_votes/total_votes'],
                                'up_votes': int(dataDict.at[i,'up_votes']),
                                'down_votes': int(dataDict.at[i,'down_votes'])} }
        coll.update_one(songHashQuery, newValues)
      else:
        funcLog = funcLog + "== Skipping: Old Entry\n"
  return funcLog

def getAllMaps(): # Returns a pandas dataframe of all of the documents in the collection
  if "songData" in db.list_collection_names():
    exportDf = pd.DataFrame(columns = column)
    for x in coll.find():
      exportDf = exportDf.append(x, ignore_index = True)
    exportDf = exportDf.drop(columns = ['_id'])
    return exportDf
  else:
    return "Error: No maps in database"

def saveModel(model,model_name):
  pickled_model = pickle.dumps(model)
  currentTime = datetime.now()
  currentTimeStr = currentTime.strftime("%Y-%b-%d %H:%M:%S")
  info = dbMdls.insert_one({'model_data': pickled_model, 'name': model_name, 'time_created': currentTimeStr})
  
  details = {'inserted_id': info.inserted_id,
             'name': model_name,
             'time_created': currentTimeStr}
  return details

def getAllModels(): # Returns a list of all of the documents in the collection
  if "savedModels" in db.list_collection_names():
    models = []
    for x in dbMdls.find():
      diction = x
      modelInfo = {'name': diction['name'], 'time_created': diction['time_created']}
      models.append(modelInfo)
    return models
  else:
    return "Error: No models in database"

def getModel(model_name):
  if "savedModels" in db.list_collection_names():
    json_data = {}
    data = dbMdls.find({'name': model_name})

    for i in data:
      json_data = i
      pickled_model = json_data['model_data']
      return pickle.loads(pickled_model)
  else:
    return "Error: No models in database"

def queryKey(songKey: str):
  if "songData" in db.list_collection_names():
    exportDf = pd.DataFrame(columns = column)
    for x in coll.find({'song_id': songKey}):
      exportDf = exportDf.append(x, ignore_index = True)
    exportDf = exportDf.drop(columns = ['_id'])
    return exportDf
  else:
    return "Error: No data in database"


# === Debug Functions ===

def testSeq():
  # read data from file
  data = fiHandl.readFile('../data/sample_82db-8340.csv')
  # add to database
  saveMapData(data)
  '''
  print("Testing Hash")
  newdata = fiHandl.readFile('../data/sample_82db-8340_hashTest.csv')
  saveMapData(newdata)
  
  print("Testing Duplicates")
  dupes = fiHandl.readFile('../data/sample_82db-8340_modifiedDataTest.csv')
  saveMapData(dupes)
  '''

def mongoDB():
  # for db debug purposes in the console
  return db

def printColl():
  for x in coll.find():
    print(x)

def dropColl():
  coll.drop() 

def queryTest(val):
  query = coll.find({'difficulty': val})
  for x in query:
    print(x)
  return query

  