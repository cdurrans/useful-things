import pandas as pd

def Load_data(file_location):
    import pandas as pd
    import easygui
    if ".csv" in file_location:
        df = pd.read_csv(file_location)
        return df
    elif ".xlsx" in file_location:
        df = pd.read_excel(file_location)
        return df
    else:
        easygui.msgbox("Data Location File should be a csv or xlsx file to be understood by current program")
        raise ValueError


def validate_date(date_text):
    import datetime
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
    except ValueError:
        raise ValueError("Incorrect data format, should be MM/DD/YYYY")



def concat_excel_files(base_file_location, file_starts_with):
    import pandas as pd 
    import os
    full_sn_df = pd.DataFrame()
    for fname in os.listdir(base_file_location):
        if fname.startswith(file_starts_with):
            print(fname)
            full_path = os.path.join(base_file_location,fname)
            file_instance = pd.ExcelFile(full_path)
            temp_df = pd.concat([pd.read_excel(full_path, sheet_name=name) for name in file_instance.sheet_names] , axis=0)
            if full_sn_df.empty:
                full_sn_df = temp_df.copy()
            else:
                full_sn_df = pd.concat([full_sn_df, temp_df], axis=0)
    return full_sn_df




def fill_values_from_latest_above(df, col):
    df[col+"_isna"] = df[col].isnull()
    last_seen = ""
    for indx, row in df.iterrows():
        if row[col+"_isna"] == True:
            df.at[indx, col] = last_seen
        else:
            last_seen = row[col]
    df.drop(columns=[col+"_isna"], inplace=True)
    return df



def mdb_connect(db_file, old_driver=False):
    import pandas as pd 
    import pyodbc
    driver_ver = '*.mdb'
    if not old_driver:
        driver_ver += ', *.accdb'
    odbc_conn_str = ('DRIVER={Microsoft Access Driver (%s)}'
                     ';DBQ=%s;' %
                     (driver_ver, db_file))
    return pyodbc.connect(odbc_conn_str)
    # sql = """
    # select *
    # from DATA
    # """s
    # conn = mdb_connect(path_access)  # only absolute paths!
    # cursor = conn.cursor()
    # cursor.execute(sql)
    # recs = cursor.fetchall()
    # df = pd.DataFrame.from_records(recs, columns =['First Agent Name','First Connect Agent User Name','Call Date Time MST (MDY)','Answer To First Transfer Duration (SUM)','First Agent Hold Count (SUM)','Handled Count (SUM)','Handled Duration (SUM)','Offered Count (SUM)']) 
    # conn.close()


def mean_by_key(df, key_col, col):
    df_mean = df.groupby([key_col])[col].mean().reset_index()
    df_mean = df_mean.rename(columns= {col: col + " (Mean)"})
    df = pd.merge(df, df_mean, on=key_col)
    return df

def std_by_key(df, key_col, col):
    df_mean = df.groupby([key_col])[col].std().reset_index()
    df_mean = df_mean.rename(columns= {col: col + " (std)"})
    df = pd.merge(df, df_mean, on=key_col)
    return df

col_of_interest = "Hold Count by Handled Count"

def abnormal(df, col_of_interest, agent_key):
    df = mean_by_key(df, agent_key, col_of_interest)
    df = std_by_key(df, agent_key, col_of_interest)
    values = df[col_of_interest] - df[col_of_interest + " (Mean)"]
    df[f"Abnormal + {col_of_interest}"] = abs(values) > df[col_of_interest + " (std)"]
    return df


# import seaborn as sns
# from matplotlib import pyplot as plt
# sns.scatterplot(data=df, x="days since first call", y=col_of_interest, hue=f"Abnormal + {col_of_interest}")
# plt.show()

# count = 0
# for a in df[agent_key].unique():
#     count += 1
#     if count < 15:
#         sns.scatterplot(data=df[df[agent_key] == a], x="days since first call", y=col_of_interest, hue=f"Abnormal + {col_of_interest}")
#         plt.title(f"{a}")
#         plt.show()
#     else:
#         break

def KaplanMeierByGroup(df, groups_col, duration_col, event_occurred_1_col):
    from lifelines import KaplanMeierFitter
    import plotly.graph_objects as go
    fig = go.Figure()
    save_points = pd.DataFrame()
    for gr in df[groups_col].unique():
        i1 = (df[groups_col] == gr)
        kmf1 = KaplanMeierFitter()
        kmf1.fit(df.loc[i1, duration_col].values, df.loc[i1, event_occurred_1_col].values, label=f'{gr}')
        x1points = kmf1.survival_function_.index
        y1points = kmf1.survival_function_.iloc[:,0]
        fig.add_trace(go.Scatter(x=x1points, y=y1points,
                        mode='lines',
                        name=f'Group = {gr}', 
                        hovertemplate =
                            '<br><b>Probability</b>: %{y:.2f}'+
        '<br><b>Years</b>: %{x:.2f}'))
        save_points_temp = pd.DataFrame()
        save_points_temp.insert(0, f'Group_{gr}_time', list(x1points))
        save_points_temp.insert(1, f'Group_{gr}_prob', list(y1points))
        save_points = pd.concat([save_points, save_points_temp], axis = 1)
        
    fig.update_layout(title = 'Likelihood of Event', hovermode = 'x unified')
    fig.update_xaxes(title_text=f'{duration_col}')
    fig.update_yaxes(title_text="Probability of Survival (Event still hasn't happened.")


# Bayesian T-Test

# #install.packages("devtools")
# #devtools::install_github("rasmusab/bayesian_first_aid")
# library(BayesianFirstAid)
# ```
# ```{r}
# bayes.t.test(qm$Met.Before,qm$Met.After)
# fit=bayes.t.test(qm$Met.Before,qm$Met.After)
# plot(fit)


def compare_groups(df1, df2, keys1, keys2):
    dfsub1 = df1[keys1].copy()
    dfsub2 = df2[keys2].copy()
    dfsub2.columns = keys1
    dfsub1['count'] = 1
    dfsub2['count'] = 1
    gr1 = dfsub1.groupby(keys1)['count'].sum()
    gr2 = dfsub2.groupby(keys1)['count'].sum()
    joint_kb_day = pd.merge(gr1, gr2, how="outer", right_index=True, left_index=True)
    joint_kb_day['count_x'] = joint_kb_day['count_x'].fillna(0)
    joint_kb_day['count_y'] = joint_kb_day['count_y'].fillna(0)
    results = joint_kb_day[joint_kb_day["count_x"].astype(int) != joint_kb_day["count_y"].astype(int)]
    print(results)
    return results



# results = compare_groups(df1, df2, key_cols_df1, key_cols_df2)






import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import argparse
import easygui

custom_stop_words = ['http']

def topNGrams(data_series,ngram_range_values,custom_stop_words):
    stops =  set(stopwords.words('english')+custom_stop_words)
    stops.remove('not')
    co = CountVectorizer(ngram_range=ngram_range_values,stop_words=stops)
    counts = co.fit_transform(data_series)
    return pd.DataFrame(counts.sum(axis=0),columns=co.get_feature_names()).T.sort_values(0,ascending=False)




# import pandas as pd 

# df = pd.read_parquet("C:/Users/cdurrans/Downloads/buyer_data.parquet")
# df.loc[df["Age"] < 1, "Age"] = df["Age"].median()

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
        if props[col].isna().sum() > 0: 
            NAlist.append(col)
            props[col].fillna(mn-1,inplace=True)  
                
        # test if column can be converted to an integer
        asint = props[col].fillna(0).astype(np.int64)
        result = (props[col] - asint)
        result = result.sum()
        if result > -0.01 and result < 0.01:
            IsInt = True
        
        # Make Integer/unsigned Integer datatypes
        try:
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
                if mn > np.finfo(np.float32).min and mx < np.finfo(np.float32).max:
                    props[col] = props[col].astype(np.float32)
                elif mn > np.finfo(np.float64).min and mx < np.finfo(np.float64).max:
                    props[col] = props[col].astype(np.float64)
                elif mn > np.finfo(np.float128).min and mx < np.finfo(np.float128).max:
                    props[col] = props[col].astype(np.float128)    
            # Print new column type
            print("dtype after: ",props[col].dtype)
            print("******************************")
        except Exception as ex:
            print(f"Failed to convert {col} with the following error:")
            print(ex)
            print("******************************")
    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return props, NAlist


# df, nanlist = reduce_mem_usage(df)
# df.to_parquet("C:/Users/cdurrans/Downloads/buyer_data_reduced.parquet")




from dateutil.parser import parse
def check_is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False
