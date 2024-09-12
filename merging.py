# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 19:02:11 2024

@author: ricky
"""

import pandas as pd

# Load all CSV files into dataframes
file1_df = pd.read_csv('extraction_20k.csv')
file2_df = pd.read_csv('clustering_plus_chat_gpt_titles_extraction_20k.csv')
file3_df = pd.read_csv('bertopic_titles_extraction_20k.csv')
file4_df = pd.read_csv('bertopic_abstr_extraction_20k.csv')


# Merge the columns from file2, file3, and file4 into file1 based on 'id'
file1_df = file1_df.merge(file2_df[['Title','Cluster_Name']], on='Title', how='right')
file1_df = file1_df.merge(file3_df[['Title','CustomName']], on='Title', how='right')
file1_df = file1_df.merge(file4_df[['Title','CustomName']], on='Title', how='right')

file1_df.to_csv('clusters_extract.csv', index=False)
