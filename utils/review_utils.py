#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2022 Feb 15 
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
from tqdm import tqdm
import sys

sys.path.insert(0, '..')
from configs import config, state_refs

# States list
states_list = list(state_refs.us_state_to_abbrev.values())


# Helper cleaning functions
def extract_value_to_append(matching_value, matching_colname,
                            source_state_or_zip_colname, source_df):
    pass

def _split_dates(reviews_df):
    reviews_df['date'] = pd.to_datetime(reviews_df['date'])
    reviews_df['year'] = reviews_df['date'].dt.year
    reviews_df['month'] = reviews_df['date'].dt.month
    reviews_df['day'] = reviews_df['date'].dt.day
    return reviews_df


def _match_zip_to_county(zipcode, zipcode_df):
    return zipcode_df[zipcode_df['zip'] == zipcode]['county_name'].iloc[0]


def _get_cpi_by_zip(county_df, zip_df, zipcode, state):
    # slice by state first
    # then slice by county - some places have the same county names
    pass


def _get_cpi_by_state():
    pass


def add_cpi():
    # grab value by county
    # grab value by state

    pass


def add_values_by_state(states_list=states_list, supplemental_df,
                        supplemental_colnames: list, reviews_df, new_colnames: list):
    for state in tqdm(states_list):
        values_to_append = list()
        for i in len(range(supplemental_dfs)):
            values_to_append.append(supplemental_df[i][supplemental_df[i]['state'] == state][supplemental_colname].iloc[0])

        reviews_df.loc[reviews_df['business_state'] == state,
                        new_colnames
        ] = values_to_append
    
    return reviews_df


def add_values_by_location(location_list:list , supplemental_df, state_or_zip,
                        supplemental_colnames: list, reviews_df, new_colnames: list):
# this is a more generalized version of 'add_values_by_state'
    for location in tqdm(location_list):
        values_to_append = list()
        for i in len(range(supplemental_dfs)):
            values_to_append.append(supplemental_df[i][supplemental_df[i][state_or_zip] == location][supplemental_colname].iloc[0])

        reviews_df.loc[reviews_df[f"business_{state_or_zip}"] == location,
                        new_colnames
        ] = values_to_append
    
    return reviews_df


def add_value_by_zip(reviews_df, supplemental_df, supplemental_colnames:list, new_colnames: list):
    zips_list = set(reviews_df['business_zipcode'])
    for zipcode in tqdm(zips_list):
        values_to_append = list()
        for i in len(range(supplemental_dfs)):
            values_to_append.append(supplemental_df[i][supplemental_df[i]['state'] == state][supplemental_colname].iloc[0])
        pass
    pass


def add_zips_to_reviews(reviews: pd.DataFrame, businesses: pd.DataFrame, business_list: list):
    for business_id in tqdm(business_list):
        zipcode = businesses[businesses['business_id'] == business_id]['zipcode'].iloc[0]
        state = businesses[businesses['business_id'] == business_id]['state'].iloc[0]

        reviews.loc[
            reviews['business_id'] == business_id,
            ['business_state', 'business_zipcode']
        ] = state, zipcode

    return reviews


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
    output = _split_dates(output)
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
    output.rename(columns={'postal_code': 'zipcode'})

    return output



# Append zip code to reviews - DONE
# Add ideology with bespoke function
# Add by state/zip function - DONE

# Add pop density ahead

# Add pop density before
