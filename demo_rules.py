#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:31:51 2019
@author: anobles
Takes in a set of askdocs posts and labels for demographics
"""

import os
from read_reddit_data import create_fn_list, create_json_list, exclude_remove_del_posts
from collections import Counter
import re
import pandas as pd


def check_automod(posts):
    """Labels whether a post meets the automod standard as indicated by askdocs"""
    automod_met = []
    doesnt_meet_automod = []
    # patterns that askdocs automod checks for
    automod_pat = ["age", "weight", "height", "male", "female", "lbs", "lbs.", "lb", "pounds", "years old", "year old", "y/o", "yr/old", "yrs", "yrs old", "cm", "kg", "weigh"]
    reg_pat = re.compile(r'\b(?:%s)\b' % '|'.join(automod_pat))
    for post in posts:
        post_text = clean_text(post, 'automod')
        match = re.search(reg_pat, post_text)
        if match != None:
            automod_met.append(True)
        else:
            automod_met.append(False)
    return automod_met, doesnt_meet_automod


def label_gender(posts):
    """Labels gender of poster using regular expressions"""
    gender = []
    #multiple_f = ['female', 'f', 'int_f', 'woman', 'girl']
    multiple_f = ['female']
    #multiple_m = ['male', 'm', 'int_m', 'man', 'boy']
    multiple_m = ['male']
    for post in posts:
        patt_match = []
        post_tot = clean_text(post, 'gender')
        # search for patterns and append the gender
        if re.search(r'\bmale\b', post_tot): # male
            patt_match.append('male')
        if re.search(r'\bm\b', post_tot): # M
            patt_match.append('male')
        if re.search(r'\b[0-9]{1,2}m\b', post_tot):# 24M
            patt_match.append('male')
        if re.search(r'\bman\b', post_tot): # man
            patt_match.append('male')
        if re.search(r'\bboy\b', post_tot):  # boy
            patt_match.append('male')
        if re.search(r'\bfemale\b', post_tot): # female
            patt_match.append('female')
        if re.search(r'\bf\b', post_tot): # F
            patt_match.append('female')
        if re.search(r'\b[0-9]{1,2}f\b', post_tot): # 24F
            patt_match.append('female')
        if re.search(r'\bwoman\b', post_tot): # woman
            patt_match.append('female')
        if re.search(r'\bgirl\b', post_tot): # girl
            patt_match.append('female')
        match = re.search(r'\b(f)(\d{1,2})', post_tot) #F23
        if match != None:
            patt_match.append('female')
        match = re.search(r'\b(m)(\d{1,2})', post_tot) #M23
        if match != None:
            patt_match.append('male')
        if len(patt_match) > 1:
            if set(patt_match).issubset(multiple_f):
                gender.append('female')
            elif set(patt_match).issubset(multiple_m):
                gender.append('male')
            else:
                gender.append('unknown')
        elif len(patt_match) == 1:
            gender.append(patt_match[0])
        else:
            gender.append('unknown')
    return gender


def label_age(posts):
    """Labels age of poster using regular expressions"""
    age = []
    for post in posts:
        patt_match = []
        post_tot = clean_text(post, 'age')
        # search for patterns and append the age
        match = re.search(r'i am\s([0-9]{1,2})\b(?! lb| kg| pound| kilo| percent|%|.| cm| meter)', post_tot) # i am 24
        if match != None:
            patt_match.append(match.group(1))
        match = re.search(r"i'm\s([0-9]{1,2})\b(?! lb| kg| pound| kilo| percent|%|.| cm| meter)", post_tot) # i'm 24
        if match != None:
            patt_match.append(match.group(1))
        match = re.search(r'\b([0-9]{1,2})\s(?:years old|year old|yrs old|yr old|yo|y o)', post_tot) # 24 years old, 24 y/o, 24 yrs old
        if match != None:
            patt_match.append(match.group(1))
        match = re.search(r'\b([0-9]{1,2})\s(?:months old|month old|mos old|mo old)', post_tot) # babies (months)
        if match != None:
            months = int(match.group(1))
            baby_age = months/12
            patt_match.append(baby_age)
        match = re.search(r'\b([0-9]{1,2})\s(?:days old|day old)', post_tot) # babies (days)
        if match != None:
            days = int(match.group(1))
            baby_age = days/365
            patt_match.append(baby_age)
        match = re.search(r'\b([0-9]{1,2})\s(?:weeks old|week old|wk old|wks old)', post_tot) # babies (weeks)
        if match != None:
            weeks = int(match.group(1))
            baby_age = weeks/52
            patt_match.append(baby_age)
        match = re.search(r'\b([0-9]{1,2})(?:m\b|f\b)', post_tot) # 24M/24F
        if match != None:
            patt_match.append(match.group(1))
        match = re.search(r'\b(?:m|f)([0-9]{1,2})', post_tot) # M24/F24
        if match != None:
            patt_match.append(match.group(1))
        match = re.search(r'age\s{1,2}([0-9]{1,2})\b', post_tot) # age: 24, age 24
        if match != None:
            patt_match.append(match.group(1))
        # if we haven't found an age using the above rules, we'll match to a common pattern (but less so than above)
        if patt_match == []:
            # common pattern male 24 or 24 male
            match1 = re.search(r'\b([0-9]{1,2})\s(?:\bmale|female)', post_tot) # 24 male/female
            match2 = re.search(r'\b(?:male|female)\s([0-9]{1,2})', post_tot) # male/female 24
            match3 = re.search(r'\b([0-9]{1,2})\s\b(?:m|f)\b', post_tot) # 24 m/f
            match4 = re.search(r'\b(?:m|f)\s([0-9]{1,2})', post_tot) # m/f 24
            if match1 != None:
                patt_match.append(match1.group(1))
            elif match2 != None:
                patt_match.append(match2.group(1))
            elif match3 != None:
                patt_match.append(match3.group(1))
            elif match4 != None:
                patt_match.append(match4.group(1))
        # omit common errors
        typical_errors = ('0','95','96','97','98','99')
        # check if there was more than one match
        if len(patt_match) > 1:
            # if multiple conflicting "ages" occur, then label unknown
            if len(set(patt_match)) != 1:
                age.append('unknown')
            elif patt_match[0] in typical_errors:
                age.append('unknown')
            else:
                age.append(patt_match[0])
        # if only one match and it is not a typical error, then assign label for age
        elif len(patt_match) == 1 and patt_match[0] not in typical_errors:
            age.append(patt_match[0])
        else:
            age.append('unknown')
    return age


def label_race(posts):
    """Labels race of poster using regular expressions"""
    race = []
    for post in posts:
        patt_match = []
        post_tot = clean_text(post, 'race')
        if re.search(r'\b(?:white|caucasian)\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool| mold)', post_tot):
            patt_match.append('white')
        if re.search(r'\b(?:african|black)\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool| mold)', post_tot):
            patt_match.append('black')
        if re.search(r'\b(?:hispanic|latino|latina)\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('hispanic')
        if re.search(r'\b(?:asian|chinese|japenese|korean|vietnamese)\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('asian')
        if re.search(r'\bindian\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('indian')
        if re.search(r'\bmixed\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('mixed')
        if re.search(r'\bmiddle eastern\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('middle_eastern')
        if re.search(r'\bpacific islander\b(?! bump| skin| spot| area| sore| hair| nail| fingernail| restaurant| food| teeth| tooth| streak| mark | syndrome| fluff| stuff| fluid| pus| bruise| stool)', post_tot):
            patt_match.append('pacific_islander')
        if len(patt_match) > 1:
            # although this ocassionally indicates mixed, there were more false positives than actual mixed race in random sample
            race.append('unknown')
        elif len(patt_match) == 1:
            race.append(patt_match[0])
        else:
            race.append('unknown')
    return race


def clean_text(post, demo):
    # clean up text - join title/body, remove new lines, strip punctuation
    text = post['title'] + ' ' + post['selftext']
    text = text.replace('\n', ' ')
    text = text.lower()
    if demo == 'age':
        # including punc that is common for temp and height 99.0 or 5'11''
        exclude = set('!#$&\()*+,-/:;<=>?@[\\]^_`{|}~')
    else:
        exclude = set('!"#%$&\()*+,-./:;<=>?@[\\]^_`{|}~')
        apostrophe = set("'")
        apostrophe.add(chr(8217))
        apostrophe.add(chr(8216))
        for char in apostrophe:
            text = text.replace(char, '')
    for char in exclude:
        text = text.replace(char, ' ')
    text = re.sub('\s+', ' ', text).strip()
    #text = ''.join(char for char in text if char not in exclude)
    return text


def random_performance_check(posts, gender, age, race):
    # create a df
    attributes_to_retain = ['id', 'created_utc', 'title', 'selftext']
    df = create_df(posts, attributes_to_retain, gender, age, race)
    # randomly sample df for all times
    df_random_all = df.sample(n=50, random_state=42)
    # randomly sample df for known automod time period
    df['created_utc'] = pd.to_numeric(df['created_utc'])
    df_select = df[(df['created_utc'] >= 1543622400) & (df['created_utc'] <= 1546214400)]
    df_random_automod = df_select.sample(n=50, random_state=42)
    return df_random_all, df_random_automod


def create_df(posts, attributes, gender, age, race):
    df = pd.DataFrame(columns=attributes)
    for attribute in attributes:
        attribute_vals = []
        for post in posts:
            if attribute in post:
                attribute_vals.append(post[attribute])
            else:
                attribute_vals.append(None)
        df[attribute] = attribute_vals
    df['gender'] = gender
    df['age'] = age
    df['race'] = race
    return df


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

    # evaluate how many posts achieve askdocs automod
    automod_met, doesnt_meet_automod = check_automod(posts_org)
    Counter(automod_met)

    # label gender
    gender = label_gender(posts_org)
    Counter(gender)

    # label age
    age = label_age(posts_org)
    Counter(age)

    # label race
    race = label_race(posts_org)
    Counter(race)

    # randomly select 100 posts for a performance check (50 from all time; 50 from after automod)
    random_all, random_automod= random_performance_check(posts_org, gender, age, race)
    # save to csv
    #random_all.to_csv(os.path.expanduser('~/Documents/rAskDocs/Results/RandomDemoPerformanceCheck/random_all.csv'), index=False)
    #random_automod.to_csv(os.path.expanduser('~/Documents/rAskDocs/Results/RandomDemoPerformanceCheck/random_automod.csv'), index=False)


if __name__ == "__main__":
    main()
