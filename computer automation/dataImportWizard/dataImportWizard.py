import os 
import sys 
pathToDbTools = 'C:/Users/cdurrans/Desktop/useful-things/'
sys.path.insert(0,pathToDbTools)
import pandas as pd 
from shutil import copyfile
import pyodbc
import shutil
import time
from dbTools import DBTools
import easygui
from datetime import datetime

customTemplateFile = 'path/to/loadCustomFile_TEMPLATE.py'
temp_contentTxt = 'path/to/createScheduledtask_temp_content.txt'
# pwrshellTemplateFile = 'path/to/createScheduledtask.ps1'
runPythonBatTemplate = 'path/to/runPythonFileBatTEMPLATE.bat'

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

def createtaskBatFile():
    f = open(runPythonBatTemplate,'r')
    ftxt = f.read()
    f.close()
    ftxt = ftxt.replace('__pythonFileLocation__', destinationFile)
    f = open(runPythonBatTemplate[:-12]+f"{tableName}"+'.bat','w')
    f.write(ftxt)
    f.close()
    
def createTask():
    f = open(pwrshellTemplateFile,'r')
    ftxt = f.read()
    f.close()
    timeToRun = easygui.integerbox('What time in the morning do you want this to run?','Time')
    ftxt = ftxt.replace('__programFileLocation__', runPythonBatTemplate[:-12]+f"{tableName}"+'.bat')
    ftxt = ftxt.replace('__tableName__', f'_{tableName}')
    ftxt = ftxt.replace('__taskName__',f'Load_{tableName}')
    ftxt = ftxt.replace('__description__',f'Auto_generated_using_dataImportWizard.py')
    ftxt = ftxt.replace('__time__',f'{timeToRun}')
    f = open(pwrshellTemplateFile[:-4]+'_temp.bat','w')
    f.write('call powershell '+ftxt)
    f.close()
    import subprocess, sys
    createtaskBatFile()
    # subprocess.run([pwrshellTemplateFile[:-4]+'_temp.bat'],stdout=sys.stdout)

def createTaskFileForMonitor():
    timeToRun = easygui.integerbox('What time in the morning do you want this to run?','Time')
    createtaskBatFile()
    f = open(temp_contentTxt,'w')
    f.write('Load_' + tableName +' \n') #taskname
    f.write(str(timeToRun)+' \n') #time
    f.write(runPythonBatTemplate[:-12]+f"{tableName}"+'.bat \n') #programFileLocation
    f.close()

def checkAccessToTemplates(currentTemplateFile):
    if os.path.isfile(customTemplateFile) == False:
        easygui.msgbox("It appears that you can't access the files you need for /w17568. Please talk to Chris, you probably need to map the network location. //w17568/Shared Folders/")
        runMain = False

easygui.msgbox('Welcome to the data import wizard')
gsd = False
scheduleAutomatically = True

while gsd == False:
    scheduleAutomatically = False  # This only will work if you have the templates saved to the server you are loading tasks onto.
    serverSelected = easygui.textbox('What is the server name you are connecting to?')
    dbSelected = easygui.textbox('What is the database you want to connect to?')
    try:
        Mydb = DBTools(serverSelected,dbSelected)
        gsd = True
    except Exception as ex:
        easygui.msgbox(f'Error occurred connecting to {serverSelected} {dbSelected}, see error: {ex}')

runMain = True
MainMenuloop = True

# checkAccessToTemplates(currentTemplateFile)

while runMain:
    while MainMenuloop:
        mainSelection = easygui.buttonbox('What would you like to do?','Main Menu',['Load Data','Exit Program'])
        if mainSelection == 'Load Data':
            fileToOpen = easygui.fileopenbox('Please select a csv or xlsx file')
            if fileToOpen == None:
                break #go to main menu
            df = openPandasCsvExcelFileGiven(fileToOpen)
            if type(df) != type(pd.DataFrame()):
                easygui.msgbox('Please make sure you select either a .csv or .xlsx. Talk to Chris about other options.')
                break
            print(df.head())
            currentTableActionCheck = True
            while currentTableActionCheck == True:
                while True:
                    tableName = easygui.enterbox('What do you want the table to be called?')
                    if tableName == None:
                        easygui.msgbox('Please enter a table name or close the black terminal window.(Need to improve this)')
                    else:
                        break
                currentTableAction = easygui.choicebox('What do you want to do if table exists?','Table Option',['replace','append','fail'])
                if currentTableAction == None:
                    easygui.msgbox('Please make a selection or close the black terminal window and restart program.(Need to improve this)')
                elif currentTableAction == 'fail':
                    print('Checking table exists')
                    if Mydb.checkTableExists(tableName):
                        ynexists = easygui.ynbox(f'{tableName} already exists and you selected the option fail. Do you want to continue with the fail option? It will save for future imports as fail, but you will have to do something about it existing already.')
                        if ynexists:
                            currentTableActionCheck = False
                        else:
                            easygui.msgbox('You selected to not continue please change the table name or what to do with it.')
                            continue
                    else:
                        print('Doesnt exist')
                        currentTableActionCheck = False
                else:
                    currentTableActionCheck = False
            while scheduleAutomatically:
                reoccur = easygui.ynbox('Do you want to schedule this upload to reoccur?')
                if reoccur:
                    easygui.msgbox(f"Please make sure that Load_{tableName} doesn't exist already in the task scheduler. Everything else will work fine except it won't overwrite it if it exists already.")
                    today = datetime.today().strftime('%Y_%m_%d')
                    destinationFile = customTemplateFile.replace('_TEMPLATE',f"{tableName}")
                    easygui.msgbox(f'Created custom file at {destinationFile}.')
                    copyfile(customTemplateFile, destinationFile)
                    f = open(destinationFile,'r')
                    ftxt = f.read()
                    f.close()
                    ftxt = ftxt.replace('__fileToOpen__',fileToOpen)
                    ftxt = ftxt.replace('__tableName__',tableName)
                    ftxt = ftxt.replace('__currentTableAction__',currentTableAction)
                    f = open(destinationFile,'w')
                    f.write(ftxt)
                    f.close()
                    reoccurCheck = False
                    createTaskFileForMonitor()
                    break
                elif reoccur == None:
                    easygui.msgbox('Please check yes or no or close the terminal window to quit.')
                else:
                    break
            Mydb.insertTableMssql_sqlalchemy(df,tableName,currentTableAction)
        elif mainSelection == 'Exit Program':
            runMain = False
            MainMenuloop = False
            break
