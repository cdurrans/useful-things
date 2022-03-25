import os 
import pandas as pd 
import pyodbc
import shutil
import time

class DBTools:
    def __init__(self, server, database):
        self.database = database
        self.server = server
        self.connection = None
    
    def connect_to_Server(self):
        if self.connection != None:
            self.close_connection()
        self.connection = pyodbc.connect('Driver={SQL Server};'
                                    f'Server={self.server};'
                                    f'Database={self.database};'
                                    'Trusted_Connection=yes')
    #
    def connect_to_Server_sqlalchemy(self):
        if self.connection != None:
            self.close_connection()
        import sqlalchemy as sa
        engine = sa.create_engine(f'mssql+pyodbc://{self.server}/{self.database}?driver=SQL+Server+Native+Client+11.0')
        self.connection = engine.connect()
    #
    def close_connection(self):
        try:
            self.connection.close()
        except Exception as ex:
            print(ex)
        finally:
            self.connection = None
    #
    def insertTableMssql_sqlalchemy(self,df,table,if_exists):
        self.connect_to_Server_sqlalchemy()
        try:
            # df = df.set_index(df.columns[0])
            frame = df.to_sql(table, self.connection, if_exists=if_exists);
        except ValueError as vx:
            print(vx)
        except Exception as ex:
            print(ex)
        else:
            print("Table %s inserted successfully."%table);
        finally:
            self.close_connection()
    #
    def checkTableExists(self,tableName):
        self.connect_to_Server()
        cur = self.connection.cursor()
        sqlExists = f'''SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tableName}' '''
        cur.execute(sqlExists)
        result = cur.fetchall()
        cur.close()
        self.close_connection()
        if len(result) > 0:
            return True
        else:
            return False
    #
    def truncateTable(self,tableName):
        if self.checkTableExists(tableName):
            self.connect_to_Server()
            cur = self.connection.cursor()
            cur.execute(f"TRUNCATE TABLE {tableName}")
            cur.commit()
            cur.close()
    #
    def executeQuery_nonData(self,query):
        self.connect_to_Server()
        cur = self.connection.cursor()
        cur.execute(query)
        cur.commit()
        cur.close()
    #
    def commaSeperateItemsForSQL(self,items):
        apos = "'"
        if items:
            itemsStr= "','".join(items)
            itemsStr = "%s%s%s" % (apos,itemsStr,apos) 
            return itemsStr
        else:
            return "%s%s%s" % (apos,items,apos)
    #
    def bulkInsertTable(self, df, tableName, fileFolderLocation,ROWTERMINATOR='\n',FIELDTERMINATOR=',',FIRSTROW=2):
        for col in df.columns:
            df[col] = df[col].astype(str)
        while True:
            try:
                if self.checkTableExists(tableName):
                    self.truncateTable(tableName)
                    df.to_csv(fileFolderLocation+tableName+'.csv',sep=FIELDTERMINATOR)
                    sql = f'''
                                BULK INSERT  [{self.database}].[dbo].[{tableName}]  FROM '{fileFolderLocation}{tableName}.csv' WITH (
                                DATAFILETYPE = 'char',
                                FIELDTERMINATOR = '{FIELDTERMINATOR}' ,
                                ROWTERMINATOR = '{ROWTERMINATOR}',
                                KEEPNULLS,
                                ERRORFILE ='{fileFolderLocation}{tableName}_errors.csv',
                                MAXERRORS = 2000,
                                FIRSTROW = {FIRSTROW} )
                    '''
                    # print(sql)
                    if os.path.exists(f'{fileFolderLocation}{tableName}_errors.csv.Error.Txt'):
                        os.remove(f'{fileFolderLocation}{tableName}_errors.csv.Error.Txt')
                    if os.path.exists(f'{fileFolderLocation}{tableName}_errors.csv'):
                        os.remove(f'{fileFolderLocation}{tableName}_errors.csv')
                    self.connect_to_Server()
                    cur = self.connection.cursor()
                    cur.execute(sql)
                    cur.commit()
                    cur.close()
                    os.remove(fileFolderLocation+tableName+'.csv')
                    break
                else:
                    self.insertTableMssql_sqlalchemy(df.head(),tableName,'replace')
                    # raise ValueError("The sql table doesn't exist")
            except Exception as ex:
                print(ex)
                raise ex
                break

def test_checkTableExists():
    Mydb = DBTools('w13107','gsc')
    assert Mydb.checkTableExists('EMP_MAIN') == True
    assert Mydb.checkTableExists('EMP_MAIN_made_up_table') == False
    print('Check Table Exists Test successful')





# def truncate_table(table):
#     connection = connect_to_w13107_GSC()
#     cursor = connection.cursor()
#     cursor.execute(" TRUNCATE TABLE " + table)
#     connection.commit()
#     cursor.close()
#     connection.close()

# def callStoredProcedure(procedure):
#     try:
#         connection = connect_to_w13107_GSC()
#         connection.autocommit = True
#         cursor = connection.cursor()
#         if isinstance(procedure,str):
#             cursor.execute('SET NOCOUNT ON; exec '+procedure)
#             cursor.close()
#             connection.close()
#         else:
#             print("procedure must be a string not a :", type(procedure.dtype))
#             cursor.close()
#             connection.close()
#             return ValueError
#     except Exception as e:
#         print("Error: {}".format(str(e)))



####Delete duplicates sql
# delete x from (
#   select *, rn=row_number() over (partition by [key Col] order by (SELECT NULL))
#   from tb_GIS_SN 
# ) x
# where rn > 1;





#####Connect to Access

# import pandas as pd 
# import pyodbc

# def mdb_connect(db_file, old_driver=False):
#     driver_ver = '*.mdb'
#     if not old_driver:
#         driver_ver += ', *.accdb'
#     odbc_conn_str = ('DRIVER={Microsoft Access Driver (%s)}'
#                      ';DBQ=%s;' %
#                      (driver_ver, db_file))
#     return pyodbc.connect(odbc_conn_str)

# conn = mdb_connect(path)  # only absolute paths!
# cursor = conn.cursor()
# cursor.execute(sql)
# recs = cursor.fetchall()
# df = pd.DataFrame.from_records(recs, columns =['list','of','columns']) 













#Another method for inserting data. Good at handling errors because you have full control one record at a time. Slow insert speed though. Also annoying to code up.

# connection = mt.connect_to_w13107_GSC()
#     cursor = connection.cursor()
#     row_added = 0
#     for index, row in df.iterrows():
#         if row['ResponseId'] not in list(already_ResponseId['ResponseId']) and pd.notna(row['ResponseId'] and pd.notna(row["ticket"])):
#             try:
#                 row_added +=1
#                 cursor.execute("INSERT INTO dbo.[Qualtrics_preview]( \
#                        [StartDate] \
#                       ,[EndDate] \
#                       ,[Status] \
#                       ,[IPAddress] \
#                       ,[Progress] \
#                       ,[Duration (in minutes)] \
#                       ,[Finished] \
#                       ,[RecordedDate] \
#                       ,[ResponseId] \
#                 ,[LocationLatitude] \
#                 ,[LocationLongitude] \
#                 ,[DistributionChannel] \
#                 ,[UserLanguage] \
#                 ,[Q1] \
#                 ,[Q2] \
#                 ,[Q3] \
#                 ,[Q4] \
#                 ,[ticket] \
#                 ,[Q2 - Topics]) \
#                 values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
#                 row['StartDate']
#                 ,row['EndDate']
#                 ,row['Status']
#                 ,row['IPAddress']
#                 ,row['Progress']
#                 ,row['Duration (in seconds)']
#                 ,row['Finished']
#                 ,row['RecordedDate']
#                 ,row['ResponseId']
#                 ,row['LocationLatitude']
#                 ,row['LocationLongitude']
#                 ,row['DistributionChannel']
#                 ,row['UserLanguage']
#                 ,row['Q1']
#                 ,row['Q2']
#                 ,row['Q3']
#                 ,row['Q4']
#                 ,row['ticket']
#                 ,row['Q2 - Topics'])
#                 connection.commit()
#             except Exception as ex:
#                 print(row)
#                 print(ex)
#                 continue
#     print("Number of rows added survey: ",row_added)
#     cursor.close()
#     connection.close()