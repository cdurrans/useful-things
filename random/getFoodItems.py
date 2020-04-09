

import requests
import pandas as pd 
import json
import time

dtypesDF = {'date': 'object', 'time': 'object', 'time_zone': 'object', 'format': 'object', 'text': 'int64', 'notes': 'float64', 'favorite': 'int64', 'date_utc': 'object', 'time_utc': 'object', 'metadata': 'float64','responseData':'object'}
df = pd.read_csv('C:/Users/cdurrans/Downloads/pantry 3_14_2020_combined.csv', dtype=dtypesDF)
# df.dtypes.apply(lambda x: x.name).to_dict()
df['responseData'].fillna('',inplace=True)
url_base = 'https://api.upcitemdb.com/prod/trial/lookup?upc='
count = 0
alreadyGathered = []
time_sleep = 10
for indx, row in df.iterrows():
    if count > 90:
        break
    elif df.at[indx,'responseData'] != '':
        print('Already Gathered', row['text'])
        alreadyGathered.append(row['text'])
        continue
    else:
        print('Not blank')
        if row['text'] not in alreadyGathered:
            count += 1
            print('Request #',str(count))
            res = requests.get(url_base+str(row['text']))
            time.sleep(time_sleep)
            txt = json.loads(res.text)
            if txt['code'] == 'OK':
                df.at[indx,'responseData'] = txt
            elif txt['code'] == 'TOO_FAST':
                print('It is too fast I guess even at ',time_sleep)
                time_sleep += 2
                time.sleep(time_sleep+15)
                res = requests.get(url_base+str(row['text']))
                txt = json.loads(res.text)
                df.at[indx,'responseData'] = txt
            elif txt['code'] == 'INVALID_UPC':
                df.at[indx,'responseData'] = txt
            else:
                print(txt)
                import sys
                sys.quit()
            alreadyGathered.append(row['text'])
        else:
            print('Already Gathered')
            continue


df.to_csv('C:/Users/cdurrans/Downloads/pantry 3_14_2020_combined.csv',index=False)



