#!/usr/bin/env python3
# -*- coding: utf-8 -*
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2021 Dec 6
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import tqdm
from utils.utility_functions import clean_yelp_data
import config

# File paths and URLs required for script
BUSINESS_DATA_FILEPATH = 'data/yelp_academic_dataset_business.json'
REVIEWS_DATA_FILEPATH = 'data/yelp_academic_dataset_review.json'
USERS_DATA_FILEPATH = 'data/yelp_academic_dataset_user.json'
COUNTY_DATA_FILEPATH = 'data/county_data.csv'
STATES_DATA_FILEPATH = 'data/states_data.csv'
ZIPCODES_DATA_FILEPATH = 'data/zip_code_database.csv'
CPI_URL = 'https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index'
POP_DENSITY_FILEPATH = 'data/apportionment.csv'

COUNTY_DF = pd.read_csv(COUNTY_DATA_FILEPATH, index_col=0)
STATES_DF = pd.read_csv(STATES_DATA_FILEPATH, index_col=0)
ZIPS_DF = pd.read_csv(ZIPCODES_DATA_FILEPATH)
POP_DENSITY = pd.read_csv(POP_DENSITY_FILEPATH)

# Configuration
USER_CONFIG = config.USER_DTYPES

# Load and fix zipcode data
ZIPS_DF = ZIPS_DF[['zip', 'state', 'county']]
ZIPS_DF['zip'] = ZIPS_DF['zip'].astype(str).apply(clean_yelp_data.fix_zipcode)
ZIPS_DF['county'] = ZIPS_DF['county'].str.lower()
ZIPS_DF.loc[len(ZIPS_DF)] = ['02101', 'MA', 'suffolk county']

# Load and fix county data
COUNTY_DF['county_name'] = COUNTY_DF['county_name'].str.lower()
COUNTY_DF['county_name'] = COUNTY_DF['county_name'].apply(clean_yelp_data.fix_county_name)

# Population density data
CPVI = pd.read_html(CPI_URL)[1]
CPVI.drop(CPVI.tail(1).index, inplace=True)
CPVI['pvi'] = CPVI['PVI'].apply(clean_yelp_data.process_cpvi)
CPVI['state'] = CPVI['State'].str.upper()
CPVI = CPVI[['state', 'pvi']]

# Create a unique states list
STATES_LIST = list(COUNTY_DF['state_po'].unique())
print(f"Number of states: {len(STATES_LIST)}")

# Load business data
BUSINESSES = list()
with open(BUSINESS_DATA_FILEPATH, 'r') as f:
    reader = pd.read_json(f, orient='records', lines=True, chunksize=1000, dtype=config.BUSINESS_DTYPES)

    for chunk in tqdm(reader):
        reduced_chunk = chunk[config.COLS['business']]
        reduced_chunk = reduced_chunk[reduced_chunk['state'].isin(STATES_LIST)]
        reduced_chunk['postal_code'] = reduced_chunk['postal_code'].apply(clean_yelp_data.fix_zipcode)
        reduced_chunk = reduced_chunk[reduced_chunk['categories'].notnull()]
        reduced_chunk = reduced_chunk[reduced_chunk['categories'].str.contains('Restaurants')]
        BUSINESSES.append(reduced_chunk)

    BUSINESSES = pd.concat(BUSINESSES, ignore_index=True)
print('Businesses loaded.')
BUSINESS_LIST = list(BUSINESSES['business_id'].unique())

# Load reviews
REVIEWS = list()
print('Loading reviews...')
with open(REVIEWS_DATA_FILEPATH, 'r') as f:
    reader = pd.read_json(f, orient='records', nrows=300000, lines=True, chunksize=1000, dtype=config.REVIEW_DTYPES)

    for chunk in tqdm(reader):
        reduced_chunk = chunk[config.COLS['reviews']]
        reduced_chunk = reduced_chunk[reduced_chunk['business_id'].isin(BUSINESS_LIST)]
        # Only keep US
        REVIEWS.append(reduced_chunk)
    REVIEWS = pd.concat(REVIEWS, ignore_index=True)
print('Reviews loaded')

BUSINESS_LIST = list(REVIEWS['business_id'].unique()) # rename to get effective list
print(f"Number of businssess: {len(BUSINESS_LIST)}")
USERS_LIST = list(REVIEWS['user_id'].unique())

print('Adding business state and zip codes...')
for business_id in tqdm(BUSINESS_LIST):
    business_zipcode = BUSINESSES[BUSINESSES['business_id'] == business_id]['postal_code'].iloc[0]
    business_state = BUSINESSES[BUSINESSES['business_id'] == business_id]['state'].iloc[0]

    REVIEWS.loc[REVIEWS['business_id'] == business_id, ['business_state', 'business_zipcode']] = business_state, business_zipcode

REVIEWS = REVIEWS[REVIEWS['business_state'].isin(STATES_LIST)]

STATES_LIST = list(REVIEWS['business_state'].unique())
STATES_ABBR = dict()

for state in list(STATES_DF['state']):
    STATES_ABBR[state] = COUNTY_DF[COUNTY_DF['state'] == state]['state_po'].unique()[0]

print('Processing business state ideology and state pvi')
for state in tqdm(list(STATES_ABBR.keys())):
    try:
        state_ideology = STATES_DF[STATES_DF['state'] == state]['perc_diffs'].iloc[0]

        if state == 'DISTRICT OF COLUMBIA':
            state_pvi = 0
        else:
            state_pvi = CPVI[CPVI['state'] == state]['pvi'].iloc[0]

        REVIEWS.loc[REVIEWS['business_state'] == STATES_ABBR[state],
                    ['business_state_ideology', 'business_state_pvi']] = state_ideology, state_pvi
    except:
        print(state)
        print('bad output')

print('Adding total reviews and average stars per business')
REVIEWS['count'] = 1
BUSINESS_COUNTS = REVIEWS.groupby('business_id').sum().reset_index()[['business_id', 'count']]
BUSINESS_STARS = REVIEWS[['business_id', 'stars']].groupby('business_id').sum().reset_index()
BUSINESSES_LIST = list(BUSINESS_COUNTS['business_id'].unique())

for business in tqdm(BUSINESSES_LIST):
    tot_reviews = BUSINESS_COUNTS[BUSINESS_COUNTS['business_id'] == business]['count'].iloc[0]
    avg_stars = round((BUSINESS_STARS[BUSINESS_STARS['business_id'] == business]['stars'].iloc[0] / tot_reviews), 3)
    REVIEWS.loc[REVIEWS['business_id'] == business, ['business_review_total', 'avg_star_rating']] = tot_reviews, avg_stars

# add state pop density
POP_DENSITY = POP_DENSITY[POP_DENSITY['Year'] >= 2000]
POP_DENSITY_COLS = ['Name', 'Year', 'Resident Population', 'Geography Type', 'Resident Population Density']
POP_DENSITY = POP_DENSITY[POP_DENSITY_COLS]
POP_DENSITY = POP_DENSITY[POP_DENSITY['Geography Type'] == 'State']
POP_DENSITY.drop(columns=['Geography Type'], inplace=True)
POP_DENSITY_RENAMED_COLS = ['state', 'year', 'pop', 'pop_density']
POP_DENSITY.columns = POP_DENSITY_RENAMED_COLS
POP_DENSITY['state'] = POP_DENSITY['state'].str.upper()
POP_DENSITY = POP_DENSITY[POP_DENSITY['state'].isin(list(STATES_ABBR.keys()))]

# split date into separate columns
REVIEWS['date'] = pd.to_datetime(REVIEWS['date'])
REVIEWS['year'] = REVIEWS['date'].dt.year
REVIEWS['month'] = REVIEWS['date'].dt.month
REVIEWS['day'] = REVIEWS['date'].dt.day
