import pandas as pd 
import pyodbc
import datetime
import math
import sys

def reduce_mem_usage(props):
    import numpy as np
    start_mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in. 
    for col in props.select_dtypes(include=[np.number]).columns:
        # Print current column type
        print("******************************")
        print("Column: ",col)
        print("dtype before: ",props[col].dtype)
        
        # make variables for Int, max and min
        IsInt = False
        mx = props[col].max()
        mn = props[col].min()
        
        # Integer does not support NA, therefore, NA needs to be filled
        if not np.isfinite(props[col]).all(): 
            NAlist.append(col)
            props[col].fillna(mn-1,inplace=True)  
                
        # test if column can be converted to an integer
        asint = props[col].fillna(0).astype(np.int64)
        result = (props[col] - asint)
        result = result.sum()
        if result > -0.01 and result < 0.01:
            IsInt = True
        
        # Make Integer/unsigned Integer datatypes
        if IsInt:
            if mn >= 0:
                if mx < 255:
                    props[col] = props[col].astype(np.uint8)
                elif mx < 65535:
                    props[col] = props[col].astype(np.uint16)
                elif mx < 4294967295:
                    props[col] = props[col].astype(np.uint32)
                else:
                    props[col] = props[col].astype(np.uint64)
            else:
                if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                    props[col] = props[col].astype(np.int8)
                elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                    props[col] = props[col].astype(np.int16)
                elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                    props[col] = props[col].astype(np.int32)
                elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                    props[col] = props[col].astype(np.int64)    
        
        # Make float datatypes 32 bit
        else:
            props[col] = props[col].astype(np.float32)
        
        # Print new column type
        print("dtype after: ",props[col].dtype)
        print("******************************")

    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return props, NAlist

# https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65
# I modified it to ignore dates

# dfReduced, NAlist = reduce_mem_usage(df)
# print("_________________")
# print("")
# print("Warning: the following columns have missing values filled with 'df['column_name'].min() -1': ")
# print("_________________")
# print("")
# print(NAlist)





#load datasets with smaller datatypes if you've already determined their properties
#the following allows you to directly output the sizes 
# dfChat.dtypes.apply(lambda x: x.name).to_dict()

#example:

# dfChat.dtypes.apply(lambda x: x.name).to_dict()

# dftest = pd.read_excel('N:/ReportingAnalysis/Workforce/CSReporting/PEF/CRM 2019/Data/Chat Activity Advanced Find View 06-Mar-20 7-45-13 AM.xlsx'
# , dtype = {'(Do Not Modify) Chat Activity': 'object', '(Do Not Modify) Row Checksum': 'object'
# , '(Do Not Modify) Last Updated': 'datetime64[ns]'
# , 'Subject': 'object', 'Date Created': 'datetime64[ns]', 'Owner': 'object'
# , 'Chat Duration': 'float32', 'Chat Transcript': 'object', 'End Reason': 'object'
# , 'Regarding': 'object', 'Visitor City': 'object', 'Visitor Country': 'object'
# , 'Visitor Device': 'object', 'Visitor Language': 'object'
# , 'Channel': 'object', 'Description': 'object', 'Skill': 'object'
# , 'Social Channel': 'object', 'Status Reason': 'object', 'Chat Origin': 'object'
# , 'Chat Session ID': 'int32', 'Created By': 'object', 'Created By (Delegate)': 'object'
# , 'Customer': 'object', 'Modified By': 'object', 'Organizer': 'object', 'Record Created On': 'object'})


