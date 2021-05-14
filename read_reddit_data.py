#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:11:55 2019

@author: anobles
"""
import json
import os


def create_fn_list(root_dir):
    """Create a list of files in the directory"""
    fn_list = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]
    fn_list = [f for f in fn_list if f.find('txt') != -1]
    return fn_list


def create_json_list(root_dir, fn, json_data):
    """Load files with json entries into a singular list"""
    for line in open(os.path.join(root_dir, fn), 'r'):
        json_data.append(json.loads(line))
    return json_data


def exclude_remove_del_posts(posts):
    """Returns posts excluding those that have been removed or deleted"""
    exclude = {'[removed]','[deleted]'}
    posts_final = [post for post in posts if post['selftext'] not in exclude]
    return posts_final


def exclude_remove_del_comments(comments):
    """Returns comments excluding those that have been removed or deleted"""
    exclude = {'[removed]','[deleted]'}
    comments_final = [comment for comment in comments if comment['body'] not in exclude]
    return comments_final


if __name__ == "__main__":
    main()