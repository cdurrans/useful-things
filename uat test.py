#uat

#TODO make it more reusable by accepting arguments for files


#This was my first attempt to compare two data sets to see if there were differences between them.
#I have since found datacompy which is really good and does a better job. See dataCompare.py in my repo

import pandas as pd
import re
base = 'some/location'
df = pd.read_excel(base + 'uat - prd.xlsx')
df2 = pd.read_csv(base + 'uat -dev.csv')
key = 'data_key'

assert len(df.columns) == len(df2.columns)
print("Number of Columns Matches")

for x in range(0,len(df.columns)):
    assert df.columns[x] == df2.columns[x]
print("Column Names Match")

assert len(df[key]) == len(df2[key])
print("Length Of Datasets Match")

df = df.sort_values(by=[key]).copy().reset_index(drop=True)
df2 = df2.sort_values(by=[key]).copy().reset_index(drop=True)

compareCount = 0
comparedf = pd.DataFrame()

df1_len = len(df[key])

comparedf.at[compareCount,'df1_column'] = ""
comparedf.at[compareCount,'df1_value'] = ""
comparedf.at[compareCount,'df2_value'] = ""
comparedf.at[compareCount,'df1_key'] = ""
comparedf.at[compareCount,'df2_key'] = ""

for indx , row in df.iterrows():
    if indx%100 == 0:
        print(float(indx)/df1_len* 100)
    for col in df.columns:
        if row[col] != df2.at[indx,col]:
            ######################################### for a significant speed boost remove the isnull logic and just know that when two nulls are compared they aren't equal so they are added to the end result.#################
            # if pd.isnull(row[col]) and pd.isnull(df2.at[indx,col]):
            #     continue
            if row[key] != df2.at[indx,key]:
                print("There are different keys. \nThere are the same number of columns and the same number of records. \nThey are both sorted by the key and yet this row has different keys.\n","Key One: ", row[key], "\nKey Two: ",df2.at[indx,key],"\nRow: ",indx )
                raise AssertionError
            else:
                comparedf.at[compareCount,'df1_column'] = str(col)
                comparedf.at[compareCount,'df1_value'] = str(row[col])
                comparedf.at[compareCount,'df2_value'] = str(df2.at[indx,col])
                comparedf.at[compareCount,'df1_key'] = str(row[key])
                comparedf.at[compareCount,'df2_key'] = str(df2.at[indx,key])
                compareCount += 1
        if compareCount > df1_len * 0.9:
            print("More than 10 percent of them have errors")
            break

comparedf.to_csv('differences_uat_test.csv')

if comparedf.empty:
    print("There are no differences")
else:
    print('The number of differences found: ', len(comparedf["df1_key"]))
