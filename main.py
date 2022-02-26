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
from configs import config
from utils import preprocessing

TESTING = True
PRECPROCESS = False
# If testing is true, include nrows in loading reviews
NROWS = None
if TESTING == True:
    NROWS = 100000

# Append using loc:
# by state
# by county name

# File paths and URLs required for script
# Yelp files
BUSINESS_DATA_FILEPATH = 'data/yelp_academic_dataset_business.json'
REVIEWS_DATA_FILEPATH = 'data/yelp_academic_dataset_review.json'
USERS_DATA_FILEPATH = 'data/yelp_academic_dataset_user.json'

# Additional data files
COUNTY_DATA_FILEPATH = 'data/county_data.csv'
STATES_DATA_FILEPATH = 'data/states_data.csv'
ZIPCODES_DATA_FILEPATH = 'data/zip_code_database.csv'
CPI_URL = 'https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index'
POP_DENSITY_FILEPATH = 'data/apportionment.csv'
INCOME_FILEPATH = 'data/zipcode2019/19zpallagi.csv'

# Configurations
USER_CONFIG = config.USER_DTYPES

# List of things to add by zip
# list of things to add by state
# CPI by state and county

# Load and clean all additional files
# Export cleaned files and delete old dataframe from ram

# Start loading Yelp data
# Load businesses first
# Businesses

# Reviews
# Load additional file when needed

# Clean up final dataframe before export

# To do
# Write script to load main data files
# Test function to begin loading new info
# Change all states to a single format, two letter code
# Begin loading Yelp files
# Write functions to add to Yelp files
# Clean everything!
