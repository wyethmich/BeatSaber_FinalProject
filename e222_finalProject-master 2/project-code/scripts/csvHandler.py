from pandas import read_csv
import numpy as np
import pandasCleaning as pdClean

# File Col Format: rownumber,song id, upvotes/total votes, upvotes, downvotes, difficulty, notes, bombs, bpm, obstacles, njs, njs offset, length, and duration
# song id is stored as decimal representation of the hex key
# difficulty: easy = 0 and increases to expertPlus = 4

def readFile(fpath):
  #Imports from csv, sanitizes to working data types
  importedData = read_csv(fpath)
  retData = pdClean.cleanDictionary(importedData)
  return retData

def exportData(fpath, dataDict):
  dataDict.to_csv(fpath)