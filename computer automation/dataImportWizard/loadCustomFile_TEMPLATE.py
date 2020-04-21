import os 
import sys 
sys.path.insert(0,'//w17568/Shared Folders/Python Scripts/')
import pandas as pd 
import pyodbc
import shutil
import time
from dbTools import DBTools

def openPandasCsvExcelFileGiven(fname):
    if '.csv' in fname.lower():
        df = pd.read_csv(fname)
        return df
    elif '.xlsx' in fname.lower():
        df = pd.read_excel(fname)
        return df
    else:
        return None

def loadFile(baseFolder,fileLooksLike):
    count = 0
    for fname in os.listdir(baseFolder):
        if fileLooksLike in fname:
            print(f'Looking at {fname}')
            fnamedeets = fname.split('_')
            try:
                return openPandasCsvExcelFileGiven(baseFolder+fname)
            except Exception as ex:
                print(ex)
                break
    return None

def setnthRowAsHeader(df, nthRow):
    if nthRow < 0:
        raise ValueError("must be larger than zero")
    else:
        df = df.iloc[nthRow-2:,:].copy()
        df.columns = df.iloc[0,:]
        return df.iloc[1:,:].copy()

def removeAllFilesPatterned(emailedDataFolder,startsWithFile):
    for fname in os.listdir(emailedDataFolder):
        try:
            if fname.startswith(startsWithFile):
                os.remove(emailedDataFolder+fname)
        except Exception as ex:
            print(ex)

fileToOpen = '__fileToOpen__'
tableName = '__tableName__'
currentTableAction = '__currentTableAction__'

Mydb = DBTools('w17568\S01','GSD')
df = openPandasCsvExcelFileGiven(fileToOpen)
if type(df) == type(pd.DataFrame()):
    Mydb.insertTableMssql_sqlalchemy(df,tableName,currentTableAction)
#



