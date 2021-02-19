import pandas as pd
# df = pd.read_excel(file_location)
text_column = "Ticket Description Detail"
import plotly.express as px

class Text_Categorizer:
    def __init__(self, pandas_dataframe, text_column):
        self.df = pandas_dataframe
        self.df['Found With'] = ""
        self.text_column = text_column
        self.set_category_column("my_label")
        self.df[text_column + '_lower'] = df[text_column].str.lower()
        self.length_of_data = len(self.df)
        self.print_results = True
        self.df['record_count'] = 1
    
    def set_print_results(bool_setting):
        try:
            assert isinstance(bool_setting, bool)
            self.print_results = bool_setting
        except:
            print("Must supply boolean only. Setting not changed")
    
    def set_category_column(self, category_column):
        self.category_column = category_column
        self.df[self.category_column] = ""
    
    def label_data(self, text_search, category_label):
        bool_true = self.df[self.text_column + '_lower'].str.contains(text_search)
        if self.print_results:
            bool_true_sum = bool_true.sum()
            print(f"Labeled {bool_true_sum} out of {self.length_of_data} or ({100 * round(bool_true_sum/self.length_of_data,2)}%)")
        self.df.loc[bool_true, self.category_column] = category_label
        once_as = f"Labeled Once as {category_label}"
        if once_as not in self.df.columns:
            self.df[once_as] = False
        either_condition = bool_true | self.df[once_as]
        self.df.loc[either_condition, once_as] = True
        self.df.loc[bool_true, 'Found With'] = self.df.loc[bool_true, 'Found With'] + text_search + '|'
    
    def summary(self):
        results = self.df.groupby([self.category_column])['record_count'].sum().reset_index()
        results['Percentage'] = round(results['record_count']/self.length_of_data,2)
        print(results)
    
    def plot_labels(self):
        fig = px.sunburst(self.df, path=['my_label','Found With'], values='record_count')
        fig.show()

    def print_unlabeled(self, num=50):
        print(self.df.loc[self.df[self.category_column] == "", self.text_column].sample(num))
    
    def save_data(self, file_location):
        if file_location.endswith(".csv"):
            self.df.to_csv(file_location)
        if file_location.endswith(".xlsx"):
            self.df.to_excel(file_location)
        else:
            print("File didn't save because file location wasn't a csv or xlsx file.")
