# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 07:19:46 2019

@author: cdurrans
"""

#pandas for data loading and handling
import pandas as pd 
df = pd.read_csv('N:/ReportingAnalysis/Workforce/custom tools/housing_residential.csv',sep='|')
#remember to make the \ slashes \\ or / for your file path names

#Explore Data

#list all columns in panda's dataframe object
df.columns

#top five rows
df.head()

#gives info on each column including datatype and record counts
df.info()

#for iloc [rows,columns] with the following:
#    [:,:] all rows all columns
#    [5:,:] skip rows 0-4
#    [:,3:] skip first couple of columns and keep the rest
df.iloc[:,:6].info() # see info on the first 5 or 6 columns

#Summary function for each column, can be saved as var and viewed in variable explorer
dfDescription = df.describe()


#Replace Data Missing/bad

df['Estimate Mortgage'].replace('[\$,]\s','',regex=True)
#pythex.org Regular Expressions

#chain functions and change data type to int or str or float
df['listedPrice'] = df['Estimate Mortgage'].replace('[\$,]','',regex=True).astype(int)

#get a count of how many missing values in Estimate column
df['Estimate Mortgage'].isna().sum()

#fillna returns all data already there and fills what ever you put into the missing records for that column
df['Estimate Mortgage'].fillna(0)

#filtering syntax df[boolean statement] below shows records that aren't null for Estimate Mortgage
df[df['Estimate Mortgage'].notna()]

# shows percent null for each column
df.isna().sum() / len(df)


for col in df.columns:
    print(col)
    if df[col].dtype == 'object':
        modeForCol = df[col].mode()
        df[col] = df[col].fillna(modeForCol)
        #df[col] = modeForCol
    else:
        meanForCol = df[col].mean()
        df[col] = df[col].fillna(meanForCol)



import pyodbc

def connect_to_w13107_GSC():
    connection = pyodbc.connect('Driver={SQL Server};'
                                    'Server=w13107;'
                                    'Database=GSC;'
                                    'Trusted_Connection=yes')
    return connection

#An example of a function to run a sql statement
def truncate_table(table):
    connection = connect_to_w13107_GSC()
    cursor = connection.cursor()
    #insert whatever sql statement you want in the execute command below. Change the code to whatever
    cursor.execute(" TRUNCATE TABLE " + table)
    connection.commit()
    cursor.close()
    connection.close()

def callStoredProcedure(procedure):
    try:
        connection = connect_to_w13107_GSC()
        connection.autocommit = True
        cursor = connection.cursor()
        if isinstance(procedure,str):
            cursor.execute('SET NOCOUNT ON; exec '+procedure)
            cursor.close()
            connection.close()
        else:
            print("procedure must be a string not a :", type(procedure.dtype))
            cursor.close()
            connection.close()
            return ValueError
    except Exception as e:
        print("Error: {}".format(str(e)))


#An example of how to load data from w13107 into a pandas dataframe
sql = "SELECT * FROM EMP_MAIN;"
conn = connect_to_w13107_GSC()
dfEmp = pd.read_sql(sql,conn)
conn.close()



missingInfoCol = 'Estimate Mortgage'
missingPersonInfoThatWeHave = ''
missPersonAssignedToCol = ''

missingPersonDf = df[df[missingInfoCol].isna()].copy()

for indx in df.index:
    if isinstance(df.at[indx,missingInfoCol],str):
        pass
    else:
        print('missing at: ',indx)
        locations = df.index[df[missPersonAssignedToCol] == df.at[indx,missingPersonInfoThatWeHave]]
        if locations:
            df.at[indx,missingInfoCol] = df.at[locations[0],missingPersonInfoThatWeHave]
        else:
            print("Person not found ", indx)



connection = connect_to_w13107_GSC()
connection.autocommit = True
cursor = connection.cursor()
cursor.execute('UPDATE EMP_MAIN SET ' + missingInfoCol + ' = ' + value + 'where ' + missingInfoCol + ' is null and report colum we have blah balh = ....')
cursor.close()
connection.close()





