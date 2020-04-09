"""
This code makes it easy to do topicModeling for any data. There's probably an easier way using the lda package but
this is what I've used for a while and it works for me as of present.

#Update 4/9/2020 there are shorter simpler ways but some of these functions are nice to have, so I'm keeping it for now.
"""
import numpy as np
import pandas as pd
import re
import os
import nltk

from collections import Counter
from nltk.corpus import stopwords
from nltk import word_tokenize
import re

#nltk.download('stopwords')
# nltk.download('wordnet')
import gensim
from gensim.models.coherencemodel import CoherenceModel

#https://www.datacamp.com/community/tutorials/discovering-hidden-topics-python
#https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24

remove_words_smaller_than_me = 3
remove_words_not_occuring_less_than = 2
remove_words_occurring_in_more_than_x_percentage_of_documents = 0.75
keep_top_n_words = 100000

def prep_data_for_topic_modeling(df,column):
    print("Prepping data for topic modeling")
    from gensim import corpora, models
    df_text = preprocess_text_column_with_given_function(df,column,preprocess,returnType="series")
    dictionary = gensim.corpora.Dictionary(df_text)
    dictionary.filter_extremes(no_below=remove_words_not_occuring_less_than, no_above=remove_words_occurring_in_more_than_x_percentage_of_documents, keep_n=keep_top_n_words)
    bow_corpus = [dictionary.doc2bow(doc) for doc in df_text] #also known as doc_term_matrix
    tfidf = models.TfidfModel(bow_corpus)
    corpus_tfidf = tfidf[bow_corpus]
    print("Finished Prep for topic modeling")
    return df_text, dictionary, bow_corpus, tfidf, corpus_tfidf

def preprocess_text_column_with_given_function(df,column,processingFunction,returnType="dataframe"):
    print('preprocessing text with given function')
    if returnType == "dataframe":
        #keep rows that are not null
        newdf = df[df[column].notnull()].copy()
        newdf = newdf.reset_index(drop=True)
        #apply supplied preprocessingfunction to column
        newdf[column+'_processed'] = newdf[column].map(processingFunction)
        return newdf
    if returnType == "series":
        newcorpura = df[column][df[column].notnull()].copy()
        newcorpura = newcorpura.reset_index(drop=True)
        newcorpura = newcorpura.map(processingFunction)
        return newcorpura
    else:
        raise ValueError('In preprocess_text_column_with_given_function I need more outputs or use one of these ["dataframe","series"]')

def preprocess(text):
    # print("selected preprocessing function 1")
    result = []
    from gensim.utils import simple_preprocess
    from gensim.parsing.preprocessing import STOPWORDS
    for token in gensim.utils.simple_preprocess(text):
        # if len(token) > remove_words_smaller_than_me:
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > remove_words_smaller_than_me:
            result.append(lemmatize_and_stem_words(token))
    return result

def lemmatize_and_stem_words(text,language="english"):
    from nltk.stem import WordNetLemmatizer
    from nltk.stem import SnowballStemmer
    stemmerChosen = SnowballStemmer(language)
    return stemmerChosen.stem(WordNetLemmatizer().lemmatize(text, pos='v'))


def Topic_Each_question(df,Column_Name,category_label,n_topics):
    """
    df: Pandas Dataframe with Column_Name,
    Column_Name: column with text data to be analyzed,
    category_label: Label in case you filtered data and want to have multiple instances joined later into a dataset,
    n_topics: Number of topics for Topic Modeling
    """
    try:
        df, lda_model_tfidf_Q3 = run_topic_model(df,Column_Name,num_topics=n_topics)
        df = get_topic_words_and_add_to_df(lda_model_tfidf_Q3, df, Column_Name+"_topic_number")
        df.dropna(subset=[Column_Name+"_topic_number"],inplace=True)
    except Exception as ex:
        print(ex, "/n Category ", category_label, '. With df'+Column_Name)
        df = pd.DataFrame()
    return df


def run_topic_model(df,column,num_topics):
    df_text, dictionary, bow_corpus, tfidf, corpus_tfidf = prep_data_for_topic_modeling(df,column)
    #plot_graph(df_text,dictionary,bow_corpus,num_topics, num_topics+20, 2)
    lda_model_tfidf = gensim.models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary, iterations=200, passes=100, workers=4)
    print("Updating df with predictions")
    df = update_df_with_predictions(df,column,dictionary,lda_model_tfidf)
    return df, lda_model_tfidf

def update_df_with_predictions(df,column,dictionary,model):
    for indx, x in enumerate(df[column]):
        topics_info, topic_number, topic_score = what_topic_is_it(x,dictionary,model)
        df.at[indx, column+"_topic_number"] = topic_number
        df.at[indx, column+"_topic_score"] = topic_score
    return df

def what_topic_is_it(unseen_string,dictionary,model):
    if isinstance(unseen_string,str):
        bow_vector = dictionary.doc2bow(preprocess(unseen_string))
        topics_info = sorted(model[bow_vector], key=lambda tup: -1*tup[1])
        topic_number = topics_info[0][0]
        topic_score = topics_info[0][1]
        return topics_info, topic_number, topic_score
    else:
        # print(unseen_string)
        return None, None, None

def get_topic_words_and_add_to_df(model, df, topic_num_column, text_column_preface="",num_words=5):
    x = model.show_topics(num_words=num_words,formatted=False)
    # print("Model topic data x: ", x)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]
    # print(topics_words)
    for indx, x in enumerate(df[topic_num_column]):
        try:
            if isinstance(x,str):
                df.at[indx, text_column_preface+"topic_words"] = " ".join(topics_words[int(x)][1])
        except Exception as ex:
            print(ex)
    return df


# The compute_coherence_values is one way to determine how many topics should be chosen. Uncomment the line above if you wish to use it.
def compute_coherence_values(dictionary, doc_term_matrix, doc_clean, stop, start=2, step=3):
    """
    Input   : dictionary : Gensim dictionary
              corpus : Gensim corpus
              texts : List of input texts
              stop : Max num of topics
    purpose : Compute c_v coherence for various number of topics
    Output  : model_list : List of LSA topic models
              coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, stop, step):
        # generate LSA model
        model = gensim.models.LdaMulticore(doc_term_matrix, num_topics=num_topics, id2word = dictionary, passes=2, workers=4)  # train model
        # model = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary)  # train model
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=doc_clean, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

def plot_graph(doc_clean,dictionary,doc_term_matrix,start, stop, step):
    model_list, coherence_values = compute_coherence_values(dictionary, doc_term_matrix,doc_clean,
                                                            stop, start, step)
    # Show graph
    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()



