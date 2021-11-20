#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

COUNTY_VOTING_DATA_FILEPATH = 'data/countypres_2000-2020.csv'


COLUMNS = ['year', 'state', 'state_po', 'county_name', 'party', 'candidatevotes', 'totalvotes']
YEAR = '2020'

COUNTY_DF = pd.read_csv(COUNTY_VOTING_DATA_FILEPATH, usecols=COLUMNS, index_col=False)
COUNTY_DF['year'] = COUNTY_DF['year'].astype(str)
COUNTY_DF = COUNTY_DF[(COUNTY_DF['year'] == YEAR)]

# finally fill na with 0
COUNTY_DF['candidatevotes'].fillna(0, inplace=True)

# Address the county with no NaN values
PROBLEM_COUNTY = COUNTY_DF[COUNTY_DF['county_name'] == 'SAN JOAQUIN']
TOT_VOTES = PROBLEM_COUNTY['candidatevotes'].sum()
COUNTY_DF['totalvotes'].fillna(TOT_VOTES, inplace=True)

# Only keep democrat or republican
COUNTY_DF = COUNTY_DF[
    (COUNTY_DF['party'] == 'DEMOCRAT') |
    (COUNTY_DF['party'] == 'REPUBLICAN')
]

COUNTY_DF.sort_values(by=['state', 'county_name', 'party'], inplace=True)

# Aggregate by state
STATES_DF = COUNTY_DF.groupby(['state', 'party', 'year']).sum().reset_index()
STATES_DF.sort_values(by=['state','party'], inplace=True)


COUNTY_DF['perc_votes'] = round(((COUNTY_DF['candidatevotes'] / COUNTY_DF['totalvotes']) * 100), 2)
COUNTY_DF['perc_diffs'] = COUNTY_DF['perc_votes'].diff(periods=1)

STATES_DF['perc_votes'] = round(((STATES_DF['candidatevotes'] / STATES_DF['totalvotes']) * 100), 2)
STATES_DF['perc_diffs'] = STATES_DF['perc_votes'].diff(periods=1)

COUNTY_DF = COUNTY_DF[COUNTY_DF['party'] == 'REPUBLICAN'] # keep values relative to republicans
STATES_DF = STATES_DF[STATES_DF['party'] == 'REPUBLICAN']
# Combine into a states aggregation

COUNTY_DF.drop(columns=['party', 'year', 'candidatevotes', 'totalvotes', 'perc_votes',], inplace=True)
COUNTY_DF.reset_index(drop=True)

STATES_DF.drop(columns=['party', 'year', 'candidatevotes', 'totalvotes', 'perc_votes',], inplace=True)
STATES_DF.reset_index(drop=True)

COUNTY_DF.to_csv('data/county_data.csv')
STATES_DF.to_csv('data/states_data.csv')
print('Files outputted.')