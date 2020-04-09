import pandas as pd
import docx2txt
import os

def connect_to_w13107_new(database):
    import sqlalchemy as sa
    engine = sa.create_engine('mssql+pyodbc://w13107/'+database+'?driver=SQL+Server+Native+Client+11.0')
    dbConnection = engine.connect()
    return dbConnection


def insertTableMssql(df,tableName,database,if_exists='fail'):
    dbConnection = connect_to_w13107_new(database)
    try:
        frame = df.to_sql(tableName, dbConnection, if_exists=if_exists);
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        print("Table %s inserted successfully."%tableName);
    finally:
        dbConnection.close()

base = 'C:/Users/cdurrans/Downloads/EmailDocuments/Email - Recording Attendance on the Quarterly Report - Translations/'

def addTagAroundText(txt,taginside):
    return '<'+taginside+'>' + txt + '</'+taginside +'>'

def addTagAtStart(txt,taginside):
    return '<'+taginside+'>' + txt

languages = []
allOutputs = []
subjects = []
textTag = 'p'

for fname in os.listdir(base):
    EndOfEmail = False
    try:
        if fname.endswith('docx'):
            result = docx2txt.process(base+fname)
            results = result.split('\n')
            while True:
                if results[0] == '':
                    del results[0]
                else:
                    break
            subjects.append(results[2])
            count = 0
            listCounter = 0
            output = []
            for r in results:
                if r != '':
                    # if 'S. Smith' in r:
                    if 0 != 1:
                        EndOfEmail = True
                        output.append(addTagAtStart(r,textTag) + '<br>')
                        continue
                    elif EndOfEmail:
                        output.append(r + '<br>')
                    else:
                        output.append(addTagAroundText(r,textTag))
            output[-1] = output[-1] + '</p>'
            allOutputs.append(''.join(output))
            languages.append(fname.split()[-1][:-5])
    except Exception as ex:
        print(ex)
        print(fname)


df = pd.DataFrame(zip(allOutputs,languages,subjects))
# df.reset_index(inplace=True)
df.columns = ['Body','Language','Subject']
df['Type'] = "Church Attendance Q1"
df.set_index('Language',inplace=True)

# df.to_excel(base+'PleaseWork.xlsx')



df = pd.read_excel(base+'PleaseWork.xlsx')

insertTableMssql(df,'Qtr_temp','MLU',if_exists='append')




# languages = []
# allOutputs = []
# for fname in os.listdir(base):
#     try:
#         if fname.endswith('docx'):
#             result = docx2txt.process(base+fname)
#             results = result.split('\n')
#             count = 0
#             listCounter = 0
#             output = []
#             for r in results:
#                 if r != '':
#                     if count == 0:
#                         output.append(addTagAroundText(r,'p'))
#                     elif count == 1:
#                         output.append(addTagAroundText(r,'p'))
#                     else:
#                         if listCounter == 0:
#                             output.append('<ul>')
#                             output.append(addTagAroundText(r,'li'))
#                             listCounter += 1
#                         else:
#                             output.append(addTagAroundText(r,'li'))
#                     count += 1
#             output.pop()
#             output.append('</ul>')
#             output.append(addTagAroundText(r,'p'))
#             allOutputs.append(''.join(output))
#             languages.append(fname[:-5])
#     except Exception as ex:
#         print(ex)
#         print(fname)

tag = 'WindowsSevenAgain'

allOutputs = []
def appendEmailToList(emailPath):
    fname = open(emailPath,'r')
    ftext = fname.read()
    allOutputs.append(ftext)
    fname.close()


appendEmailToList(base+'Win7Eng.html')
appendEmailToList(base+'Win7Port.html')


languages = []
languages.append('English')
languages.append('Portuguese')


df = pd.DataFrame(allOutputs,languages)
df.reset_index(inplace=True)
df.columns = ['Language','Body']
df['Type'] = tag

df['Subject'] = "El apoyo de Windows 7 ha sido descontinuado"

df.loc[df['Language'] == 'English','Subject'] = 'Windows 7 Support is Discontinued'
df.loc[df['Language'] == 'Portuguese','Subject'] = 'O suporte ao Windows 7 foi descontinuado'

df.set_index('Language',inplace=True)
insertTableMssql(df,'Qtr_temp','MLU',if_exists='append')




df.loc[df['Language'] == 'Albanian','Subject'] = 'Transfertat në Burimet e Udhëheqësit dhe Nëpunësit (LCR) [BUN]'
df.loc[df['Language'] == 'Croatian','Subject'] = 'Prijenosi u Izvorima za vođe i bilježnike'
df.loc[df['Language'] == 'Czech','Subject'] = 'Převody prostředků v aplikaci Zdroje pro vedoucí a referenty'
df.loc[df['Language'] == 'Danish','Subject'] = 'Overførsler i Hjælpekilder for ledere og sekretærer'
df.loc[df['Language'] == 'Dutch','Subject'] = 'Overboekingen in Hulpmiddelen leiders en administrateurs'
df.loc[df['Language'] == 'Finnish','Subject'] = 'Siirrot johtohenkilön ja kirjurin työvälineissä'

# Umbuchungen in LCR
# All units in Portugal and Cape Verde : Portuguese for Portugal and Cape Verde.docx : Subject line : Transferências nos Recursos para Líderes e Secretários

df.loc[df['Language'] == 'Greek','Subject'] = 'Μεταφορές στο Πόροι Ηγέτη και Γραφέα'
df.loc[df['Language'] == 'Hungarian','Subject'] = 'Átutalások a Leader and Clerk Resourcesban'
df.loc[df['Language'] == 'Italian','Subject'] = 'Trasferimenti nelle Risorse per i dirigenti e per l’archivista'
df.loc[df['Language'] == 'Norwegian','Subject'] = 'Overføringer i Ressurser for ledere og sekretærer'
df.loc[df['Language'] == 'Polish','Subject'] = 'Przelewy w Zasobach przywódcy i pisarza'
df.loc[df['Language'] == 'Romanian','Subject'] = 'Transferuri în LCR (Resursele conducătorului și ale funcționarului)'
df.loc[df['Language'] == 'Serbian','Subject'] = 'Преноси средстава у Изворе за вође и књиговође'
df.loc[df['Language'] == 'Slovak','Subject'] = 'Prevody v Zdrojoch pre vedúcich a tajomníkov'
df.loc[df['Language'] == 'Slovenian','Subject'] = 'Prenosi v sistemu Viri za voditelje in tajnike'
df.loc[df['Language'] == 'Spanish','Subject'] = 'Transferencias en Fuentes de recursos para líderes y secretarios'
df.loc[df['Language'] == 'Swedish','Subject'] = 'Överföringar i Resurser för ledare och kamrerer'
df.loc[df['Language'] == 'English','Subject'] = 'Transfers in the Leader and Clerk Resources'


df.loc[df['Language'] == 'German for Austria Switzerland Germany','Subject'] = 'Umbuchungen in LCR'
df.loc[df['Language'] == 'French for Belgium and Switzerland','Subject'] = 'Transferts dans la Documentation pour dirigeants et greffiers'
df.loc[df['Language'] == 'French for France','Subject'] = 'Transferts dans la Documentation pour dirigeants et greffiers'
df.loc[df['Language'] == 'Portuguese for Portugal and Cape Verde','Subject'] = 'Transferências nos Recursos para Líderes e Secretários'




df.set_index('Language',inplace=True)
insertTableMssql(df,'Qtr_temp','MLU',if_exists='append')








import pandas as pd
import docx2txt
import os

def connect_to_w13107_new(database):
    import sqlalchemy as sa
    engine = sa.create_engine('mssql+pyodbc://w13107/'+database+'?driver=SQL+Server+Native+Client+11.0')
    dbConnection = engine.connect()
    return dbConnection


def insertTableMssql(df,tableName,database,if_exists='fail'):
    dbConnection = connect_to_w13107_new(database)
    try:
        frame = df.to_sql(tableName, dbConnection, if_exists=if_exists);
    except ValueError as vx:
        print(vx)
    except Exception as ex:
        print(ex)
    else:
        print("Table %s inserted successfully."%tableName);
    finally:
        dbConnection.close()


base = 'C:/Users/cdurrans/Downloads/'
# read in word file

def addTagAroundText(txt,taginside):
    return '<'+taginside+'>' + txt + '</'+taginside +'>'

languages = []
allOutputs = []

result = docx2txt.process(base+"FP Decision Letters Announcement - Email.docx")
results = result.split('\n')
listCounter = 0
output = []
for r in results:
    if r != '':
        output.append(addTagAroundText(r,'p'))


''.join(output)
tag = 'MemoJan8th'

df = pd.DataFrame()
df.at[0,'Language'] = 'English'
df['Type'] = tag
df.at[0,'Subject'] = 'Confidential Communications from Church Headquarters in LCR'
df.at[0,'Body'] = ''.join(output)

df.set_index('Language',inplace=True)
insertTableMssql(df,'Qtr_temp','MLU',if_exists='append')

