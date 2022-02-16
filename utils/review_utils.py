#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2022 Feb 15 
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import sys

sys.path.insert(0, '..')
from configs import config, state_refs

# States list
states_list = list(state_refs.values())

# Helper cleaning functions

def remove_empty_cats(df):
    pass


def keep_restaurants():
    pass

def _filter_cols(df, cols_list):
    return df[cols_list]


# Load review files
def load_reviews(filepath, usecols, dtype, nrows=None, business_list):
    df = list()

    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True,
                              chunksize=100, nrows=nrows, dtype=dtype)
        
        for chunk in reader:
            chunk = (chunk.
                     filter(items=usecols).
                     query('business_id in business_list')
                    )
            df.append(chunk)
    output = pd.concat(df, ignore_index=True)
    return output

# Load business files
# Query for restaurants only
def load_bussiness_data(filepath, dtype, usecols):
    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True, chunksize=1000, dtype=dtype)

        for chunk in reader:
            chunk = (chunk.
                     dropna(subset='categories').
                     filter(items=usecols).
                     query('state == @states_list').
                     filter('categories.str.contains("Restaurants"')
                    )



# Append zip code to reviews

# Add feature by zip code

# Add feature by state

# Add pop density ahead

# Add pop density before
