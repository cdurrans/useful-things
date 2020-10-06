import os
import argparse
import time
import lda
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.manifold import TSNE
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

"""
  Train an lDA model on text data
  usage --n_topics=20 --n_iter=1000 --top_n=10 --threshold=0.4 --data="/qualtrics.xlsx" --textColum=Q2 --twoOrThreeDim=3d --saveLocationcsv="/labelq2SentimentAnalysis.csv"
"""


if __name__ == '__main__':

  ##############################################################################
  # setup

  base_dir = 'ldaTSNE'
  if not os.path.exists(base_dir):
    os.makedirs(base_dir)

  parser = argparse.ArgumentParser()
  parser.add_argument('--n_topics', required=True, type=int, default=20,
                      help='number of topics')
  parser.add_argument('--n_iter', required=True, type=int, default=500,
                      help='number of iteration for LDA model training')
  parser.add_argument('--top_n', required=True, type=int, default=5,
                      help='number of keywords to show for each topic')
  parser.add_argument('--threshold', required=True, type=float, default=0.0,
                      help='threshold probability for topic assignment')
  parser.add_argument('--data', required=True, type=str, help='csv or excel with text to be analyzed')
  parser.add_argument('--textColumn', required=True, type=str, help='column name of text field')
  parser.add_argument('--twoOrThreeDim', required=True, type=str, help='select 2d or 3d')
  parser.add_argument('--saveLocationcsv', required=True, type=str, help='csv File Location')
  parser.add_argument('--fileDelimiter', required=False, type=str, help='what is your text file delimiter , | \t', default=',')
  args = parser.parse_args()

  # unpack
  n_topics = args.n_topics
  n_iter = args.n_iter
  n_top_words = args.top_n
  threshold = args.threshold
  dataLocation = args.data
  textColumn = args.textColumn
  twoOrThreeDim = args.twoOrThreeDim.lower()
  fileDelimiter = args.fileDelimiter
  
  t0 = time.time()

  ##############################################################################
  # train an LDA model
  if ".csv" in dataLocation:
      df = pd.read_csv(dataLocation, sep=fileDelimiter)
  elif ".xlsx" in dataLocation:
      df = pd.read_excel(dataLocation, sep=fileDelimiter)
  else:
      print("Data Location File should be a csv or xlsx file to be understood by current program")
      raise ValueError
  
  print("Number of records before dropping nulls: ", len(df))
  df = df[~pd.isna(df[textColumn])].reset_index(drop=True)
  df = df[df[textColumn] != 'no answer'].reset_index(drop=True)
  print("Number of records after dropping nulls: ", len(df))
  corpus = [' '.join(filter(str.isalpha, raw.lower().split())) for raw in df[textColumn]]

  cvectorizer = CountVectorizer(min_df=5, stop_words='english')
  cvz = cvectorizer.fit_transform(corpus)

  lda_model = lda.LDA(n_topics=n_topics, n_iter=n_iter)
  X_topics = lda_model.fit_transform(cvz)

  t1 = time.time()

  print( '\n>>> LDA training done; took {} mins\n'.format((t1-t0)/60.))

  np.save(base_dir + '/lda_doc_topic_{}corpus_{}topics.npy'.format(
    X_topics.shape[0], X_topics.shape[1]), X_topics)

  np.save(base_dir + '/lda_topic_word_{}corpus_{}topics.npy'.format(
    X_topics.shape[0], X_topics.shape[1]), lda_model.topic_word_)

  print ('\n>>> doc_topic & topic word written to disk\n')

  ##############################################################################
  # threshold and plot

  _idx = np.amax(X_topics, axis=1) > threshold  # idx of corpus that > threshold
  print("Number of records before dropping below threshold: ", len(X_topics))
  _topics = X_topics[_idx]
  print("Number of records after dropping below threshold: ", len(_topics))

  corpus_pd = pd.Series(corpus)
  matchingCorpus = corpus_pd[_idx]
  matchingCorpus = matchingCorpus.reset_index(drop=True)

  reduced_df = df[_idx].copy().reset_index(drop=True)

  num_example = len(_topics)

  # t-SNE: 50 -> 2D
  if twoOrThreeDim == '2d':
    tsne_model = TSNE(n_components=2, verbose=1, random_state=0, angle=.99,
                        init='pca')
    tsne_lda = tsne_model.fit_transform(_topics[:num_example])
    TwoDimColumnList = ['content','topic','x','y']
  elif twoOrThreeDim == '3d':
    tsne_model = TSNE(n_components=3, verbose=1, random_state=0, angle=.99,
                        init='pca')
    tsne_lda = tsne_model.fit_transform(_topics[:num_example])
    TwoDimColumnList = ['content','topic','x','y','z']
  else:
    print("2dor3d error")
    raise ValueError

  # find the most probable topic for each corpus
  _lda_keys = []
  for i in range(_topics.shape[0]):
    _lda_keys += _topics[i].argmax(),

  # show topics and their top words
  topic_summaries = []
  topic_word = lda_model.topic_word_  # get the topic words
  vocab = cvectorizer.get_feature_names()
  for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))

  # 20 colors
  colormap = np.array([
    "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c",
    "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f",
    "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"
  ])

  _lda_keys_pd = pd.Series(_lda_keys)
  tsne_lda_pd = pd.DataFrame(tsne_lda)
  combined = pd.concat([matchingCorpus, _lda_keys_pd,tsne_lda_pd,reduced_df], axis=1, join='inner')
  
  combined.columns = list(TwoDimColumnList) + list(df.columns)
  assert len(combined) == len(matchingCorpus)
  # plot
  for topic in range(len(topic_summaries)):
    combined.loc[combined['topic'] == topic, 'topic_summary'] = topic_summaries[topic]
  
  combined.to_csv(args.saveLocationcsv,index=False)
  t2 = time.time()
  print ('\n>>> whole process done; took {} mins\n'.format((t2 - t0) / 60.))

  
  if twoOrThreeDim == '2d':
    fig = px.scatter(combined, x="x", y="y",color="topic",hover_data=['content','topic_summary'])
    fig.show()
  else:
    my_text=[textColumn + ' text: '+ surText + '<br>Summary Words: '+ summaryWords +'<br>Topic#:'+ str(topicNum)
    for surText, summaryWords, topicNum in zip(list(combined[textColumn]), list(combined['topic_summary']), list(combined['topic'])) ]
    
    fig = go.Figure(data=[go.Scatter3d(
                    x=combined['x'],
                    y=combined['y'],
                    z=combined['z'],
                    mode='markers',
                    marker=dict(
                        color=combined['topic']
                    ),
            hovertext=my_text
            ,hoverinfo='text')])
    fig.show()
  
  

