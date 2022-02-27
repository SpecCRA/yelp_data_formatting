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

def _split_dates(reviews_df):
    reviews_df['date'] = pd.to_datetime(reviews_df['date'])
    reviews_df['year'] = reviews_df['date'].dt.year
    reviews_df['month'] = reviews_df['date'].dt.month
    reviews_df['day'] = reviews_df['date'].dt.day
    return reviews_df


def _match_zip_to_county(zipcode, zipcode_df):
     data = zipcode_df[zipcode_df['zipcode'] == zipcode][['state', 'county_name']]
     state, county_name = data['state'].iloc[0], data['county_name'].iloc[0]
     return state, county_name



def _append_cpi_by_zip(reviews_df, county_df, zip_df):
    zips_list = set(reviews_df['business_zipcode'])

    for zipcode in tqdm(zips_list):
        state = reviews_df.loc[reviews_df['business_zipcode'] == zipcode]['state'].iloc[0]
        county_name = _match_zip_to_county(zipcode, zip_df)

        county_ideology = county_df[(county_df['state'] == state) & 
                            (county_df['county_name'] == county_name)]['perc_diffs'].iloc[0]

        reviews_df.loc[reviews_df['business_zipcode'] == zipcode, 'business_county_ideology'] = county_ideology

    return reviews_df


def _append_pvi_by_state(states_pvi_df, reviews_df, states_list=states_list, supplemental_colnames=['perc_diffs'], 
                            new_colnames=['business_state_ideology']):
    # can add with other state
    reviews_df = add_values_by_location(
        states_list, states_pvi_df, 'state', supplemental_colnames, reviews_df, new_colnames
        )
    
    return reviews_df


def add_pvi(reviews_df, zipcode_df, county_pvi_df, states_pvi_df, states_list=states_list):
    # grab value by count
    # loop through zips
    print('Adding PVI by zip code...')
    reviews_df = _append_cpi_by_zip(reviews_df, county_pvi_df, zipcode_df)


    # grab value by state
    print('Adding PVI by state...')
    reviews_df = _append_pvi_by_state(states_list, states_pvi_df, reviews_df)

    return reviews_df


def add_values_by_location(location_list:list , supplemental_dfs, state_or_zip,
                        supplemental_colnames: list, reviews_df, new_colnames: list):
# this is a more generalized version of 'add_values_by_state'
# This doesn't work
# Create a key:value pair for dataframe and colnames
    for location in tqdm(location_list):
        values_to_append = list()
        for i in len(range(supplemental_dfs)):
            values_to_append.append(supplemental_dfs[i][supplemental_dfs[i][state_or_zip] == location][supplemental_colname].iloc[0])

        reviews_df.loc[reviews_df[f"business_{state_or_zip}"] == location,
                        new_colnames
        ] = values_to_append
    
    return reviews_df


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


def load_business_data(filepath, dtype, usecols):
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
    output.rename(columns={'postal_code': 'zipcode'}, inplace=True)

    return output


def _add_pop_density_forwards(decade, reviews_df, pop_density_df, states_list=states_list):
    upper_year_limit = decade + 10
    lower_year_limit = decade
    
    for state in STATES_LIST:
        state_pop_density = pop_density_df[
            (pop_density_df['year'] == decade) &
            (pop_density_df['state'] == state)
        ]['pop_density'].iloc[0]

        reviews_df.loc[
            (reviews_df['year'].between(lower_year_limit, upper_year_limit, inclusive='right')) &
            (reviews_df['business_state'] == state),
            ['population_density_backwards']
        ] = state_pop_density

        reviews_df.loc[
            (reviews_df['year'] > 2020), ['population_density_backwards']
        ] = state_pop_density


def _add_pop_density_backwards(decade, reviews_df, pop_density_df, states_list=states_list):
    upper_year_limit = decade
    lower_year_limit = decade-10

    for state in STATES_LIST:
        state_pop_density = pop_density_df[
            (pop_density_df['year'] == decade) &
            (pop_density_df['state'] == state)
        ]['pop_density'].iloc[0]

        reviews_df.loc[
            (reviews_df['year'].between(lower_year_limit, upper_year_limit, inclusive='right')) &
            (REVIEreviews_dfWS['business_state'] == state),
            ['population_density_forwards']
            ] = state_pop_density

    return reviews_df


def add_pop_densities(decades:list, reviews_df, pop_density_df):
    for decade in decades:
        reviews_df = _add_pop_density_forwards(decade, reviews_df, pop_density_df)
        reviews_df = _add_pop_density_backwards(decade, reviews_df, pop_density_df)

    return reviews_df

