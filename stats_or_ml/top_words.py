#python top_words.py --data="C:/Users/cdurrans/Downloads/task (5).xlsx" --text_column=Description --save_location_csv="C:/Users/cdurrans/Downloads/task_top_words.csv" --unique_values="Configuration item_Originating group_Assigned to"

from collections import Counter
from nltk.corpus import stopwords
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True, type=str, help='csv or excel with text to be analyzed')
parser.add_argument('--text_column', required=True, type=str, help='column name of text field')
parser.add_argument('--ngrams', required=True, type=int, help='number of word count')
parser.add_argument('--save_location_csv', required=True, type=str, help='csv File Location')
unique_values = parser.add_argument('--unique_values', required=True, type=str, help='_ seperated list of columns to split on')


args = parser.parse_args()

# unpack
text_column = args.text_column
data_location = args.data
unique_values = args.unique_values
save_location_csv = args.save_location_csv

save_location_csv = "C:/Users/cdurrans/Downloads/task_top_words.csv"
data_location = "C:/Users/cdurrans/Downloads/task.xlsx"
text_column = "Description"
unique_values = "Configuration item_Originating group_Assigned to"


if ".csv" in data_location:
    df = pd.read_csv(data_location)
elif ".xlsx" in data_location:
    df = pd.read_excel(data_location)
else:
    print("Data Location File should be a csv or xlsx file to be understood by current program")
    raise ValueError


assert "I'm not finished " == "please fix this"


def word_frequency(df, text_column, additional_stop_words = None):
    stop_words = list(stopwords.words('english'))
    if additional_stop_words:
        stop_words.append(additional_stop_words)
    c = Counter()
    for x in df[text_column]:
        if isinstance(x, str):
            x = x.lower()
            x = re.sub('[^A-Za-z\s]','',x)
            # print("This is x: ",x)
            tokens = word_tokenize(x)
            # print("Tokens: ", tokens)
            words_kept = [word for word in tokens if word not in stop_words]
            # print("Words Kept: ", words_kept)
            c.update(words_kept)
        else:
            continue
    WordList = pd.DataFrame.from_dict(c, orient='index').reset_index()
    WordList.rename(columns={'index':'Word',0: 'Frequency'}, inplace=True)
    return WordList


def preprocessing_steps(pd_series):
    pd_series = pd_series.str.lower()
    pd_series = pd_series.str.replace('[^A-Za-z\s]','', regex=True)
    return pd_series

def top_n_grams(pd_series, ngram=1 ,custom_stop_words=["http"]):
        pd_series = pd_series[pd_series.notnull()].copy()
        pd_series = preprocessing_steps(pd_series)
        ngram_range_values = (ngram, ngram)
        stops = set(stopwords.words('english')+custom_stop_words)
        stops.remove('not')
        co = CountVectorizer(ngram_range=ngram_range_values,stop_words=stops)
        counts = co.fit_transform(pd_series)
        return pd.DataFrame(counts.sum(axis=0),columns=co.get_feature_names()).T.sort_values(0,ascending=False)



columns_to_have_unique = unique_values.split("_")
print("Data's columns: ", df.columns)
print("Data requested: ",columns_to_have_unique)

# unique_values_of_columns = dict()
unique_list = []

for col in columns_to_have_unique:
    uq = df[col].unique()
    # unique_values_of_columns[col] = uq
    unique_list.append(uq)
#

combined_df = pd.DataFrame()
combo_exists = 0
combo_doesnt_exist = 0

df["row_count_groupby"] = 1
gr = df.groupby(columns_to_have_unique, dropna=False)["row_count_groupby"].sum()
gr = gr.reset_index()
gr = gr.drop("row_count_groupby", axis=1)
gr = gr.set_index(gr.columns[0])

for combo in gr.itertuples():
    if (combo_doesnt_exist + combo_exists) % 10 == 0:
        print(f"Progress: {(combo_exists + combo_doesnt_exist)/len(gr)}")
        # print(f"combo_exists: {combo_exists}")
        # print(f"combo_doesnt_exist: {combo_doesnt_exist}")
    tempdf = df.copy()
    for indx, c in enumerate(combo):
        try:
            # print(f"Instance {indx}:",tempdf.head())
            # print(f"Column: {columns_to_have_unique[indx]}")
            # print(f"value: {c}")
            tempdf = tempdf[tempdf[columns_to_have_unique[indx]] == c].copy()
        except KeyError as key_err:
            combo_doesnt_exist += 1
            # print(f"Combination of: {combo} doesn't exist in dataset")
            break
    #
    combo_exists += 1
    tempdf.reset_index(drop=True, inplace=True)
    wordListdf = word_frequency(tempdf, text_column)
    for indx, c in enumerate(combo):
        wordListdf[columns_to_have_unique[indx]] = c
    #
    if combined_df.empty:
        combined_df = wordListdf
    else:
        combined_df = pd.concat([combined_df, wordListdf])


combined_df.to_csv(save_location_csv, index=False)







