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
        state, county_name = _match_zip_to_county(zipcode, zip_df)
        county_ideology = county_df[(county_df['state'] == state) &
                            (county_df['county_name'] == county_name)]['perc_diffs'].iloc[0]
        reviews_df.loc[reviews_df['business_zipcode'] == zipcode, 'business_county_ideology'] = county_ideology

    return reviews_df


def _append_pvi_by_state(states_pvi_df, reviews_df, supplemental_colnames=['perc_diffs'], 
                            new_colnames=['business_state_ideology']):
    reviews_df = add_values_by_state(
        states_pvi_df, supplemental_colnames, reviews_df, new_colnames
        )
    
    return reviews_df

def _add_one_to_zipcode(zipcode):
    zipcode = int(zipcode)
    zipcode += 1
    zipcode = str(zipcode)
    zipcode = (5 - len(zipcode)) * '0' + zipcode
    return zipcode


def _check_zipcode(zipcode: np.str, zipcode_list):
    if zipcode not in zipcode_list:
        new_zipcode = _add_one_to_zipcode(zipcode)
        return _check_zipcode(new_zipcode, zipcode_list)
    else:
        return zipcode


def add_pvi(reviews_df, zipcode_df, county_pvi_df, states_pvi_df):
    print('Adding PVI by zip code...')
    reviews_df = _append_cpi_by_zip(reviews_df, county_pvi_df, zipcode_df)

    print('Adding PVI by state...')
    reviews_df = _append_pvi_by_state(states_pvi_df, reviews_df)

    return reviews_df


def add_values_by_zipcode(location_list:list , supplemental_df,
                        supplemental_colnames: list, reviews_df, new_colnames: list):

    supplemental_zipcodes = list(supplemental_df['zipcode'].unique())
    for location in tqdm(location_list):
        fixed_location = _check_zipcode(location, supplemental_zipcodes)
        values_to_append = list(supplemental_df[supplemental_df['zipcode'] == fixed_location][supplemental_colnames].iloc[0])

        reviews_df.loc[reviews_df[f"business_zipcode"] == location,
                        new_colnames
        ] = values_to_append

    return reviews_df


def add_values_by_state(supplemental_df, supplemental_colnames: list,
                            reviews_df, new_colnames:list):
    states_list = list(reviews_df['business_state'].unique())
    for state in states_list:
        values_to_append = list(supplemental_df[supplemental_df['state'] == state][supplemental_colnames].iloc[0])
        if len(new_colnames) == 1:
            reviews_df.loc[reviews_df['business_state'] == state, new_colnames] = values_to_append[0]
        else:
            reviews_df.loc[reviews_df['business_state'] == state, new_colnames] = values_to_append

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
    print('Reading in reviews data file...')
    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True,
                              chunksize=1000, nrows=nrows, dtype=dtype)
        for chunk in reader:
            chunk = (chunk.
                     filter(items=usecols).
                     query('business_id in @business_list')
                    )
            df.append(chunk)
    output = pd.concat(df, ignore_index=True)
    output = _split_dates(output)
    print('Reviews file loaded.')
    return output


def load_business_data(filepath, dtype, usecols):
    output = list()
    print('Reading in business data file...')
    with open(filepath, 'r') as f:
        reader = pd.read_json(f, orient='records', lines=True, chunksize=1000, dtype=dtype)

        for chunk in reader:
            chunk = (chunk.
                     dropna(subset=['categories']).
                     filter(items=usecols).
                     query('state == @states_list').
                     query('categories.str.contains("Restaurants")', engine='python').
                     query('postal_code.str.len() == 5')
                    )
            output.append(chunk)

    output = pd.concat(output, ignore_index=True)
    output.rename(columns={'postal_code': 'zipcode'}, inplace=True)

    return output


def _add_pop_density_forwards(decade, reviews_df, pop_density_df):
    upper_year_limit = decade + 10
    lower_year_limit = decade

    states_list = list(reviews_df['business_state'].unique())
    
    for state in states_list:
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

    return reviews_df


def _add_pop_density_backwards(decade, reviews_df, pop_density_df, states_list=states_list):
    upper_year_limit = decade
    lower_year_limit = decade-10

    states_list = list(reviews_df['business_state'].unique())

    for state in states_list:
        state_pop_density = pop_density_df[
            (pop_density_df['year'] == decade) &
            (pop_density_df['state'] == state)
        ]['pop_density'].iloc[0]

        reviews_df.loc[
            (reviews_df['year'].between(lower_year_limit, upper_year_limit, inclusive='right')) &
            (reviews_df['business_state'] == state),
            ['population_density_forwards']
            ] = state_pop_density

    return reviews_df


def add_pop_densities(decades:list, reviews_df, pop_density_df):
    for decade in decades:
        reviews_df = _add_pop_density_forwards(decade, reviews_df, pop_density_df)
        reviews_df = _add_pop_density_backwards(decade, reviews_df, pop_density_df)

    return reviews_df


def calculate_mean_rating(reviews_df):
    mean_ratings = reviews_df.groupby('business_id').mean()['stars'].reset_index()
    mean_ratings.columns = ['business_id', 'mean_stars']

    count_ratings = reviews_df['business_id'].value_counts().reset_index()
    count_ratings.columns = ['business_id', 'review_count']
    
    reviews_df = (
        reviews_df.merge(mean_ratings, how='left')
            .merge(count_ratings, how='left')
        )

    return reviews_df
