#!/usr/bin/env python3
# -*- coding: utf-8 -*
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2021 Dec 6
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
from tqdm import tqdm
from configs import config, state_refs
from utils import preprocessing as pp
from utils import review_utils as ru

print('Script starting...')

TESTING = False # Change this line to False when loading in all data
PRECPROCESS = False

# Yelp files
BUSINESS_DATA_FILEPATH = 'data/yelp_academic_dataset_business.json'
REVIEWS_DATA_FILEPATH = 'data/yelp_academic_dataset_review.json'
STATES_LIST = list(state_refs.us_state_to_abbrev.values())

# Additional data files
COUNTY_DATA_FILEPATH = 'data/county_data.csv'
STATES_DATA_FILEPATH = 'data/states_data.csv'
ZIPCODES_DATA_FILEPATH = 'data/zip_code_database.csv'
CPI_URL = 'https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index'
POP_DENSITY_FILEPATH = 'data/apportionment.csv'
INCOME_FILEPATH = 'data/zipcode2019/19zpallagi.csv'

# Begin preprocessing files:
# Remove loading these into memory
# Proprocess files if needed, then load each file in separately before deleting them from memory.
COUNTY_PVI = pp.load_county_data(COUNTY_DATA_FILEPATH, config.COLS['county'])
STATES_PVI = pp.load_state_data(STATES_DATA_FILEPATH)
CPI = pp.load_cpi_data(CPI_URL)
ZIPCODES = pp.load_zipcode_data(ZIPCODES_DATA_FILEPATH)
INCOME_DATA = pp.load_income(INCOME_FILEPATH, config.COLS['income'], config.INCOME_DTYPES)
POP_DENSITY = pp.load_pop_density(POP_DENSITY_FILEPATH, config.COLS['population'])


# read_json() requires me to designate how many rows to load reviews
if TESTING:
    NROWS = 200000
else:
    with open(REVIEWS_DATA_FILEPATH, 'r') as f:
        NROWS = len(f.readlines())
        print(f"Number of lines: {NROWS}")

# Start loading Yelp data
# Load businesses first
BUSINESS_DATA = ru.load_business_data(BUSINESS_DATA_FILEPATH, config.BUSINESS_DTYPES, config.COLS['business'])
BUSINESS_LIST = list(BUSINESS_DATA['business_id'].unique())

# Businesses

# Reviews
REVIEWS = ru.load_reviews(REVIEWS_DATA_FILEPATH, config.COLS['reviews'], config.REVIEW_DTYPES, BUSINESS_LIST, NROWS)
REVIEWS = ru.add_zips_to_reviews(REVIEWS, BUSINESS_DATA, BUSINESS_LIST)
del BUSINESS_DATA

# Add things by zipcode
ZIPCODE_LIST =  list(REVIEWS['business_zipcode'].unique())
# Income data
INCOME_COLS_TO_ADD = list(INCOME_DATA.columns)[2:]
REVIEWS = ru.add_values_by_zipcode(location_list=ZIPCODE_LIST, supplemental_df=INCOME_DATA,
                                    supplemental_colnames=INCOME_COLS_TO_ADD, reviews_df=REVIEWS, new_colnames=INCOME_COLS_TO_ADD)

# Add state CPI data
REVIEWS = ru.add_values_by_state(supplemental_df=CPI, supplemental_colnames=['pvi'], 
                                    reviews_df=REVIEWS, new_colnames=['business_state_pvi'])

# Add political ideologies by state and zip
REVIEWS = ru.add_pvi(REVIEWS, ZIPCODES, COUNTY_PVI, STATES_PVI)


# Add population densities
REVIEWS = ru.add_pop_densities(decades=[2000, 2010, 2020], reviews_df=REVIEWS, pop_density_df=POP_DENSITY)

# Calculate average rating
REVIEWS = ru.calculate_mean_rating(REVIEWS)

REVIEWS.to_csv('yelp_data.csv')
print('File exported. Script done.')