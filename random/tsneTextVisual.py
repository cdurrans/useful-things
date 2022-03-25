import os
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE as skTSNE
import pandas as pd
import pyodbc

def connect_to_w13107_GSC():
    connection = pyodbc.connect('Driver={SQL Server};'
                                    'Server=w13107;'
                                    'Database=GSC;'
                                    'Trusted_Connection=yes')
    return connection

def clean_special_chars(text, punct):
    for p in punct:
        text = text.replace(p, '')
    return text

def preprocess(data):
    output = []
    punct = '#$%&*+-/<=>@[\\]^_`{|}~\t\n.,'
    for line in data:
        if isinstance(line,str):
            pline= clean_special_chars(line.lower(), punct)
            output.append(pline)
        else:
            output.append('emptyNonString')
    return output

def create_corpus_labels(df,textColumn,labelColumn):
    corpus = preprocess(df[textColumn])
    corpus = pd.DataFrame(corpus)
    corpus.columns = [textColumn]
    indx = corpus[textColumn] != 'emptyNonString'
    corpus = corpus[indx]
    corpus = list(corpus[textColumn])
    df = df[indx].copy()
    labels = list(df[labelColumn])
    return df, corpus, labels

def runSVD_TSNE(n_clusters, docs):
    svd = TruncatedSVD(n_components=n_clusters)
    new_values = svd.fit_transform(docs)
    print(svd.explained_variance_ratio_)  
    print(svd.explained_variance_ratio_.sum())  
    tsneModel = skTSNE(n_components=3, perplexity=100, learning_rate=150, n_iter=1000, n_iter_without_progress=300)
    tsne_new_values = tsneModel.fit_transform(new_values)
    x = []
    y = []
    z = []
    for value in tsne_new_values:
        x.append(value[0])
        y.append(value[1])
        z.append(value[2])
    #
    # plt.figure(figsize=(16, 16)) 
    # for i in range(len(x)):
    #     plt.scatter(x[i],y[i])
    # plt.show()
    return x, y, z

conn = connect_to_w13107_GSC()
sqlQ3 = """ select *
from Qualtrics_preview
where Q2 != 'no answer'
"""
df = pd.read_sql(sqlQ3, conn)
conn.close()

textField = 'Q2'
df, corpus, labels = create_corpus_labels(df, textField,'ResponseId')

tfidf  = TfidfVectorizer()
docs   = tfidf.fit_transform(corpus)

x,y,z = runSVD_TSNE(5,docs)

df['x'] = x
df['y'] = y
df['z'] = z

import plotly.express as px
fig = px.scatter_3d(df, x='x', y='y', z='z',color='Q2',opacity=0.7)
# fig = px.scatter_3d(df.sample(frac=0.010), x='x', y='y', z='z',hover_data='Q2' ,opacity=0.7)
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.update(layout_showlegend=False)
fig.show()


# base = 'N:/ReportingAnalysis/Workforce/custom tools/Collect Qualtrics/'
# file_to_save = base + 'tsne2_' + textField + 'allDataTillNow.csv'
# df.to_csv(file_to_save,index=False, sep='|')


