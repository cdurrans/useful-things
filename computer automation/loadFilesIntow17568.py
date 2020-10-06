


import sys 
sys.path.insert(0, "//lds/gscnas/gsc_data/ReportingAnalysis/Workforce/custom tools/")
import easygui 
import pandas as pd
import os
import dbTools

def openPandasCsvExcelFileGiven(fname,sheetName=None):
    if '.csv' in fname.lower():
        df = pd.read_csv(fname)
        return df, None
    elif '.xlsx' in fname.lower():
        df = pd.ExcelFile(fname)
        if sheetName == None:
            if len(df.sheet_names) > 1:
                sheetName = easygui.choicebox("Which sheet do you want to use?","Pick an Excel Sheet",df.sheet_names)
            else:
                sheetName = df.sheet_names[0]
        df = df.parse(sheetName)
        return df, sheetName
    else:
        return None, None

mydb = dbTools.DBTools('w17568\S01', 'GSD')

fnamePattern = easygui.fileopenbox('Please select one of the files your interested in adding','Find File')

index = fnamePattern.rfind('\\')
fname = fnamePattern[index+1:]
folderLocation = fnamePattern[:index+1]

allStartWith = easygui.enterbox("Please enter pattern of files. What they all start with:")

sheetName = None
tableName = easygui.enterbox("What should the table name be?")

for f in os.listdir(folderLocation):
    if f.startswith(allStartWith):
        df, sheetName = openPandasCsvExcelFileGiven(folderLocation+f,sheetName)
        df['File Name'] = f
        mydb.insertTableMssql_sqlalchemy(df,tableName,'append')
