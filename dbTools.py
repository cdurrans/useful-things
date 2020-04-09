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
