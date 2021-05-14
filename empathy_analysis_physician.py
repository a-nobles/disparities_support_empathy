#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 08:20:23 2019

@author: anobles
"""

import pandas as pd
import os
import numpy as np
import json
from read_reddit_data import create_fn_list, create_json_list, exclude_remove_del_comments

def read_liwc_posts(path_in):
    df = pd.read_csv(path_in)
    df.rename(columns={'A':'parent_id', 'B':'content'}, inplace=True)
    return df


def read_liwc_comments(path_in):
    df = pd.read_csv(path_in)
    df.rename(columns={'A':'parent_id', 'B':'comment_id', 'C':'content'}, inplace=True)
    df['parent_id'] = df['parent_id'].apply(lambda x: x.split('_')[1])
    return df


def keep_columns(df, keep_columns):
    return df[keep_columns]


def retain_posts_comments(posts, comments):
    post_parent_ids = posts['parent_id']
    comment_parent_ids = comments['parent_id']
    matches = set(post_parent_ids) & set(comment_parent_ids)
    posts = posts[posts['parent_id'].isin(matches)]
    comments = comments[comments['parent_id'].isin(matches)]
    posts.reset_index(inplace=True)
    comments.reset_index(inplace=True)
    return posts, comments


def retain_posts_answered_doc(posts, doc_parent_ids):
    posts = posts[posts['parent_id'].isin(doc_parent_ids)]
    return posts


def retain_comments_answered_doc(comments, doc_comment_ids):
    comments = comments[comments['comment_id'].isin(doc_comment_ids)]
    return comments


def calculate_lsm(cat_post, cat_comment):
    lsm = 1 - ((abs(cat_post - cat_comment))/(cat_post + cat_comment + 0.001))
    return lsm


def score_lsm_each_interaction(posts, comments):
    parent_ids, comment_ids, lsm_ppron, lsm_ipron, lsm_article, lsm_prep, lsm_auxverb, lsm_adverb, lsm_conj, lsm_negate, lsm_quant = [], [], [], [], [], [], [], [], [], [], []
    for index, row in comments.iterrows():
        parent_id = row['parent_id']
        # find matching post
        iloc_val = np.where(posts['parent_id'] == parent_id)[0][0]
        post_match = posts.iloc[iloc_val]
        #post_match = posts[posts['parent_id'] == parent_id]
        # calculate lsms
        ppron = calculate_lsm(post_match['ppron'],row['ppron'])
        #ppron = calculate_lsm(post_match['ppron'].values[0],row['ppron'])
        ipron = calculate_lsm(post_match['ipron'],row['ipron'])
        article = calculate_lsm(post_match['article'],row['article'])
        prep = calculate_lsm(post_match['prep'],row['prep'])
        auxverb = calculate_lsm(post_match['auxverb'],row['auxverb'])
        adverb = calculate_lsm(post_match['adverb'],row['adverb'])
        conj = calculate_lsm(post_match['conj'],row['conj'])
        negate = calculate_lsm(post_match['negate'],row['negate'])
        quant = calculate_lsm(post_match['quant'],row['quant'])
        # put values in dataframe
        parent_ids.append(parent_id)
        comment_ids.append(row['comment_id'])
        lsm_ppron.append(ppron)
        lsm_ipron.append(ipron)
        lsm_article.append(article)
        lsm_prep.append(prep)
        lsm_auxverb.append(auxverb)
        lsm_adverb.append(adverb)
        lsm_conj.append(conj)
        lsm_negate.append(negate)
        lsm_quant.append(quant)
        if index % 1000 == 0:
            print(index)
    list_of_tuples = list(zip(parent_ids, comment_ids, lsm_ppron, lsm_ipron, lsm_article, lsm_prep, lsm_auxverb, lsm_adverb, lsm_conj, lsm_negate, lsm_quant))
    df = pd.DataFrame(list_of_tuples, columns = ['parent_id', 'comment_id', 'lsm_ppron', 'lsm_ipron', 'lsm_article', 'lsm_prep', 'lsm_auxverb', 'lsm_adverb', 'lsm_conj', 'lsm_negate', 'lsm_quant'])
    return df


def mean_lsm(lsm_post_comment):
    lsm_means = lsm_post_comment[['lsm_ppron', 'lsm_ipron', 'lsm_article', 'lsm_prep', 'lsm_auxverb', 'lsm_adverb', 'lsm_conj', 'lsm_negate', 'lsm_quant']].mean(axis=1)
    comment_ids = lsm_post_comment['comment_id']
    parent_ids = lsm_post_comment['parent_id']
    df = pd.concat([parent_ids, comment_ids, lsm_means], axis=1)  
    df.rename(columns={0:'mean_lsm'}, inplace=True)
    return df


def mean_conversational_lsm(lsm_means):
    df = lsm_means.drop('comment_id', axis=1)
    grouped = df.groupby('parent_id')
    parent_ids = []
    conversational_lsm = []
    for name, group in grouped:
        parent_ids.append(name)
        conversational_lsm.append(group['mean_lsm'].mean())
    list_of_tuples = list(zip(parent_ids, conversational_lsm))
    df = pd.DataFrame(list_of_tuples, columns = ['parent_id', 'conversational_lsm'])
    return df 


def main():
    # **********************************************************
    # identify comments (parent_id, comment_id) by a physician
    # **********************************************************
    
    # read original comments
    comment_dir = os.path.expanduser('~/Documents/rAskDocs/Data/Comments/')
    comment_fns = create_fn_list(comment_dir)
    comments_org = []
    for fn in comment_fns:
        comments_org.append(create_json_list(comment_dir, fn, comments_org))
    comments_org = list(filter(lambda x: type(x) == dict, comments_org))
    comments_org = exclude_remove_del_comments(comments_org)
    
    # retain a list of parent_ids and comment_ids authored by a doc
    doc_parent_ids = []
    doc_comment_ids = []
    for entry in comments_org:
        if entry['author_flair_css_class'] == 'verified-doc':
                doc_parent_ids.append(entry['parent_id'])
                doc_comment_ids.append(entry['id'])
    doc_parent_ids = [entry.split('_')[1] for entry in doc_parent_ids]
    doc_parent_ids = set(doc_parent_ids)
    doc_comment_ids = set(doc_comment_ids) 
    
    # read liwc data for posts
    directory = '~/Documents/rAskDocs/Results/LIWC_Scores/Posts/'
    fn = 'posts_titles_selftext_LIWC.csv'
    path_in = os.path.join(os.path.expanduser(directory),fn)
    posts = read_liwc_posts(path_in)
    
    # read liwc data for comments
    directory = '~/Documents/rAskDocs/Results/LIWC_Scores/Comments/'
    fn = 'comments_body_LIWC.csv'
    path_in = os.path.join(os.path.expanduser(directory),fn)
    comments = read_liwc_comments(path_in)

    # retain relevant columns
    keep = ['parent_id', 'content', 'ppron', 'ipron', 'article', 'prep', 'auxverb', 'adverb', 'conj', 'negate', 'quant']
    posts = keep_columns(posts, keep)
    
    keep = ['parent_id', 'comment_id', 'content', 'ppron', 'ipron', 'article', 'prep', 'auxverb', 'adverb', 'conj', 'negate', 'quant']
    comments = keep_columns(comments, keep)
    
    # retain posts with comments (and comments with posts)
    posts, comments = retain_posts_comments(posts, comments)
    
    # retain the posts in the doc_parent_ids
    posts = retain_posts_answered_doc(posts, doc_parent_ids) 
    posts.reset_index(inplace=True)
    
    # retain the comments in the doc_comment_ids
    comments = retain_comments_answered_doc(comments, doc_comment_ids)
    comments.reset_index(inplace=True)
    
    # apply the lsm function to find LSM for every post-comment interaction
    lsm_post_comment = score_lsm_each_interaction(posts,comments)
    #lsm_post_comment.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/lsm_post_comment_doc.csv', index=False)
    #lsm_post_comment = pd.read_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/lsm_post_comment_doc.csv')
    
    # find mean lsm of each post-comment interaction
    lsm_means = mean_lsm(lsm_post_comment)
    lsm_means_post_comment = lsm_post_comment[['lsm_ppron', 'lsm_ipron', 'lsm_article', 'lsm_prep', 'lsm_auxverb', 'lsm_adverb', 'lsm_conj', 'lsm_negate', 'lsm_quant']].mean(axis=1)
    #lsm_means_post_comment.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/mean_lsm_post_comment_doc.csv')
    
    # find mean converstaional lsm
    conversational_lsm = mean_conversational_lsm(lsm_means)
    #conversational_lsm.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/mean_conversational_lsm_doc.csv')
    
    # read post meta
    directory = '~/Documents/rAskDocs/Results/ModelingInR/'
    fn = 'df_modeling_R_update_race_gender_binnedage.csv'
    path_in = os.path.join(os.path.expanduser(directory),fn)
    post_meta = pd.read_csv(path_in)
    post_meta.drop('Unnamed: 0', axis=1, inplace=True)
    
    # merge conversational_lsm with csv with post meta
    conversational_lsm_post_meta = pd.merge(conversational_lsm, post_meta, left_on='parent_id', right_on='parent_id')
    #conversational_lsm_post_meta.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/mean_conversational_lsm_doc_post_meta.csv')
    
    # merge the new topic labels with the conversational lsm
    directory = '~/Documents/rAskDocs/Results/TopicModelResults/'
    fn = 'topics_model100_numtoken_labels_relabel.csv'
    path_in = os.path.join(os.path.expanduser(directory),fn)
    new_labels = pd.read_csv(path_in)
    
    # can merge on either on topic number or label
    conversational_lsm_post_meta_newlabel = pd.merge(conversational_lsm_post_meta, new_labels[['topic_num', 'new_label']], left_on='topic_num', right_on='topic_num')
    #conversational_lsm_post_meta_newlabel.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/mean_conversational_lsm_doc_post_meta_new_labels.csv')
    
    
    
    
    # just saving out some potentially useful counts
    temp = conversational_lsm_post_meta.groupby(['gender','race'])['race'].count()
    #temp.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/gender_race_counts.csv')
    temp = conversational_lsm_post_meta.groupby(['race','gender'])['gender'].count()
    #temp.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/race_gender_counts.csv')
    temp = conversational_lsm_post_meta.groupby(['race','topic_label'])['topic_label'].count()
    #temp.to_csv('/Users/anobles/Documents/rAskDocs/Results/ICWSM_AddOn/race_topic_label.csv')
    
