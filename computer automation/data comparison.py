import pandas as pd 
import easygui

def pandas_read(file_location):
    if file_location.endswith(".csv"):
        df = pd.read_csv(file_location)
        return df
    elif file_location.endswith(".xlsx"):
        df = pd.read_excel(file_location)
        return df
    elif file_location.endswith(".txt"):
        df = pd.read_csv(file_location, sep="\t", encoding="latin1")
        return df
    else:
        easygui.msgbox("Update the function to read this type of file.", file_location)
        return None


def compare_columns(df1, df2):
    df1_set = set(df1.columns)
    df2_set = set(df2.columns)
    print("The two have the following in common: ")
    print(df1_set.intersection(df2_set))
    print("--"*15)
    print("df1 has the following that df2 doesn't: ")
    print(df1_set.difference(df2_set))
    print("--"*15)
    print("df2 has the following that df1 doesn't: ")
    print(df2_set.difference(df1_set))


first_fname = easygui.fileopenbox("Where is the first File?")
df1 = pandas_read(first_fname)

second_fname = easygui.fileopenbox("Where is the second file?")
df2 = pandas_read(second_fname)


