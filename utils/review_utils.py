#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2022 Feb 15 
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import tqdm
import sys

sys.path.insert(0, '..')
from configs import config, state_refs

# States list
states_list = list(state_refs.us_state_to_abbrev.values())


# Helper cleaning functions
def extract_value_to_append():
    pass


def add_value_by_state():
    pass


def add_value_by_zip():
    pass


def add_zips_to_reviews(reviews: pd.DataFrame, businesses: pd.DataFrame, business_list: list):
    for business_id in business_list:
        zipcode = businesses[businesses['business_id'] == business_id]['postal_code'].iloc[0]
        state = businesses[businesses['business_id'] == business_id]['state'].iloc[0]

        reviews.loc[
            reviews['business_id'] == business_id,
            ['business_state', 'business_zipcode']
        ] = state, zipcode

    return reviews


def add_ideology_to_reviews():
    pass


def load_reviews(filepath, usecols, dtype, business_list, nrows=None):
    df = list()

    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True,
                              chunksize=100, nrows=nrows, dtype=dtype)
        
        for chunk in reader:
            chunk = (chunk.
                     filter(items=usecols).
                     query('business_id in @business_list')
                    )
            df.append(chunk)
    output = pd.concat(df, ignore_index=True)
    return output


def load_bussiness_data(filepath, dtype, usecols):
    output = list()
    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True, chunksize=1000, dtype=dtype)

        for chunk in reader:
            chunk = (chunk.
                     dropna(subset=['categories']).
                     filter(items=usecols).
                     query('state == @states_list').
                     query('categories.str.contains("Restaurants")', engine='python')
                    )
            output.append(chunk)

    output = pd.concat(output, ignore_index=True)
    return output



# Append zip code to reviews

# Add feature by zip code

# Add feature by state

# Add pop density ahead

# Add pop density before

# Add income
