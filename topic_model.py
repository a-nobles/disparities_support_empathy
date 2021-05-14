#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 09:14:52 2019

@author: anobles
"""

import os
import string
from read_reddit_data import create_fn_list, create_json_list, exclude_remove_del_posts
from urlextract import URLExtract
from string import ascii_lowercase
from sklearn.feature_extraction import stop_words
import gensim
import csv
import random
from collections import Counter
import pandas as pd
import re


def clean_text(post, exclude, extractor, stop): 
    """Cleans the text, need to manually set whehter to replace numbers with num_token."""
    # join title/body
    text = post['title'] + ' ' + post['selftext']
    
    # remove new lines
    text = text.replace('\n', ' ')
    
    # swap URLs with URL token
    for url in extractor.gen_urls(text):
        text = text.replace(url, 'urltoken')
    
    # lower text
    text = text.lower()
    
    # strip punctuation
    text = ''.join(char for char in text if char not in exclude)
    
    # strip stop words
    text = [word for word in text.split() if word not in stop]
    text = ' '.join(text)
    
    # replace numbers with num token
    text = re.sub(r'\d+', 'num_token', text)
    
    return text


def create_corpus(posts):
    """Creates the necessary components for a topic model (docs, gen_dict, corpus)"""
    docs = [post['clean_text'].split() for post in posts]
    gen_dict = gensim.corpora.Dictionary(docs)
    corpus = [gen_dict.doc2bow(doc) for doc in docs]
    return docs, gen_dict, corpus


def build_model(corpus, gen_dict, num_of_topics):
    """ Builds a topic model and requires manual setting of a random seed."""
    # model100 - random seed = 99
    # model100_numtoken - random seed = 101
    model = gensim.models.wrappers.LdaMallet(os.path.expanduser('~/mallet-2.0.8/bin/mallet'), corpus=corpus, num_topics=num_of_topics, id2word=gen_dict, random_seed=101)
    return model


def extract_topics(topic_model):
    """Takes in a topic model and outputs the words for each topic."""
    topics = []
    for topic_num in range(topic_model.num_topics):
        words = []
        for entry in topic_model.show_topic(topic_num):
            words.append(entry[0])
        topics.append(words)
    return topics


def find_max_probs(topic_model):
    """
    Iterates through posts and finds the topic with highest probability.
    Returns a list with the topic with max probability.
    """
    # extract the topics and corresponding probabilities for each post
    doc_topics = [item for item in topic_model.load_document_topics()]
    # iterate through the potential topics for each post and select the topic that is most representative (indicated by highest probability)
    representative_topic = []
    for doc_topic in doc_topics:
        # find the maximum probability of a topic
        max_prob = max([item[1] for item in doc_topic])
        # find all topics with the max prob
        candidate_topics = [item[0] for item in doc_topic if item[1] == max_prob]
        # if there is only one topic with the max prob then append the topic
        if len(candidate_topics) == 1:
            representative_topic.append(candidate_topics[0])
        # else randomly select one of the topics
        else:
            representative_topic.append(random.choice(candidate_topics))    
    return representative_topic


def extract_title_text(posts_org, extractor):  
    posts_text = []
    for post in posts_org:
        # join title and text
        text = post['title'] + ' ' + post['selftext']
        # remove new lines
        text = text.replace('\n', ' ')
        # swap URLs with URL token
        for url in extractor.gen_urls(text):
            text = text.replace(url, 'urltoken')    
        posts_text.append(text)
    return posts_text


def save_topics(topic_index, topics, sorted_topic_count, out_fn):
    data_tuples = list(zip(topic_index,topics,sorted_topic_count))
    df= pd.DataFrame(data_tuples, columns=['topic_num','words', 'count'])
    out_fn = os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/Topics/') + out_fn
    df.to_csv(out_fn, index=False)
    
    
def save_random_examples(rep_topics, topic_index, posts, num_examples, fn):
    topic_text = list(zip(rep_topics, posts))
    examples = []
    for topic_num in topic_index:
        temp_list = []
        temp_list.append(topic_num)
        subset_topic_text = [item[1] for item in topic_text if item[0]==topic_num]
        random_examples = random.choices(subset_topic_text,k=num_examples)
        for example in random_examples:
            temp_list.append(example)
        examples.append(temp_list)
        out_path = os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/Topics/') + fn
        with open(out_path, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(examples)   
    

def main():
    # directory with files
    file_dir = os.path.expanduser('~/Documents/rAskDocs/Data/Posts/')
    filenames = create_fn_list(file_dir)
    
    # import data
    posts_org = []
    for filename in filenames:
        posts_org.append(create_json_list(file_dir, filename, posts_org))
    posts_org = list(filter(lambda x: type(x) == dict, posts_org))
    posts_org = exclude_remove_del_posts(posts_org)
        
    
    # instantiiate url locator
    extractor = URLExtract()
    # characters to exclude
    exclude = set(string.punctuation)
    exclude.add(chr(8217)) # left/right single quotations
    exclude.add(chr(8216))
    # stop words
    stop = list(stop_words.ENGLISH_STOP_WORDS)
    stop.extend(['may','also','zero','one','two','three','four','five','six','seven','eight','nine','ten','across','among','beside','however','yet','within','therefore', 'just', 'ive', 'im', 'didnt', 'dont', 'id', 'wasnt', 'ill']+list(ascii_lowercase))
    stop = set(stop)
    
    # clean text
    for post in posts_org:
        post['clean_text'] = clean_text(post, exclude, extractor, stop)
    
    # create corpus
    docs, gen_dict, corpus = create_corpus(posts_org)
    gen_dict.save(os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/Models/gen_dict_numtoken'))
    
    # build model
    model50 = build_model(corpus, gen_dict, num_of_topics=50)
    model75 = build_model(corpus, gen_dict, num_of_topics=75)
    model100 = build_model(corpus, gen_dict, num_of_topics=100)
    model100_numtoken = build_model(corpus, gen_dict, num_of_topics=100)
    
    # load model
    #loaded_model = gensim.utils.SaveLoad.load(os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/Models/model100'))
    
    # save model
#    model50.save(os.path.expanduser('~/Documents/rAskDocs/Results/model50'))
#    model75.save(os.path.expanduser('~/Documents/rAskDocs/Results/model75'))
#    model100_numtoken.save(os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/Models/model100_numtoken'))
    
    # extract topics
    topics_50 = extract_topics(model50)
    topics_75 = extract_topics(model75)
    topics_100 = extract_topics(model100)
    topics_100_numtoken = extract_topics(model100_numtoken)
    
#    with open(os.path.expanduser('~/Documents/rAskDocs/Results/TopicModelResults/model100_numtoken_topics_words.csv'), 'w') as csvFile:
#        writer = csv.writer(csvFile)
#        writer.writerows(topics_100_numtoken)
    
    # create list of indices for topics
    topic_index_50 = list(range(0, len(topics_50)))
    topic_index_75 = list(range(0, len(topics_75)))
    topic_index_100 = list(range(0, len(topics_100)))
    topic_index_100_numtoken = list(range(0, len(topics_100_numtoken)))
    
    # find the representative topic for each post
    representative_topics_50 = find_max_probs(model50)
    representative_topics_75 = find_max_probs(model75)
    representative_topics_100 = find_max_probs(model100)
    representative_topics_100_numtoken = find_max_probs(model100_numtoken)
    
    # count the frequency of each topic in the dataset
    topic_count_dict_50 = Counter(representative_topics_50) # this is a dict with keys and values
    topic_count_dict_75 = Counter(representative_topics_75)
    topic_count_dict_100 = Counter(representative_topics_100)
    topic_count_dict_100_numtoken = Counter(representative_topics_100_numtoken)
    
    # order the counter to make an ordered list of frequency of topic in the dataset
    sorted_topic_count_50 = [value for (key, value) in sorted(topic_count_dict_50.items())]
    sorted_topic_count_75 = [value for (key, value) in sorted(topic_count_dict_75.items())]
    sorted_topic_count_100 = [value for (key, value) in sorted(topic_count_dict_100.items())]
    sorted_topic_count_100_numtoken = [value for (key, value) in sorted(topic_count_dict_100_numtoken.items())]

    # save topic num, words, and frequency to df and write out
#    save_topics(topic_index_50,topics_50,sorted_topic_count_50, 'topics_model50.csv')
#    save_topics(topic_index_75,topics_75,sorted_topic_count_75, 'topics_model75.csv')
#    save_topics(topic_index_100_numtoken,topics_100_numtoken,sorted_topic_count_100_numtoken, 'topics_model100_numtoken.csv')
  
    # randomly select examples for text
    # clean up text for printing
    posts_text_for_printing = extract_title_text(posts_org, extractor)
#    save_random_examples(representative_topics_50, topic_index_50, posts_text_for_printing, 5, 'examples_model50.csv')
#    save_random_examples(representative_topics_75, topic_index_75, posts_text_for_printing, 5, 'examples_model75.csv')
#    save_random_examples(representative_topics_100_numtoken, topic_index_100_numtoken, posts_text_for_printing, 5, 'examples_model100_numtoken.csv')
    

    
if __name__ == "__main__":
    main()   