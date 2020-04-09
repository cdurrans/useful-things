

# import argparse
import sqlite3
import pandas as pd
import os
#Name of Excel xlsx file. SQLite database will have the same name and extension .db
baseFilePath = 'C:/Users/cdurrans/Documents/Unearthed/Unearthed_5_SARIG_Data_Package/SARIG_Data_Package/'
dataFileFolder = 'C:/Users/cdurrans/Documents/Unearthed/Unearthed_5_SARIG_Data_Package/SARIG_Data_Package/'

filename= baseFilePath+"ExploreSA_SARIG" 
con=sqlite3.connect(filename+".db")

for fname in os.listdir(dataFileFolder):
    if fname.endswith('xlsx'):
        df = pd.read_excel(dataFileFolder+fname)
    elif fname.endswith('csv'):
        try:
            df = pd.read_csv(dataFileFolder+fname)
        except Exception as ex:
            df = pd.read_csv(dataFileFolder+fname, encoding='latin1')
    else:
        continue
    df.to_sql(fname,con, index=False)
    con.commit()

con.close()