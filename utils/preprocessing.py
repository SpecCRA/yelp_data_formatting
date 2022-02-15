#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2021 Dec 6
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np
import sys

sys.path.insert(0, '..')
from configs import config


# Helper functions

def load_file(filepath, index_col=False, dtypes=None, usecols=None):
    if usecols is None:
        return pd.read_csv(filepath, index_col=index_col, dtype=dtypes)
    else:
        return pd.read_csv(filepath, index_col=index_col, dtype=dtypes, usecols=usecols)


def load_from_url(url_path):
    dfs = pd.read_html(url_path)
    # apply cleaning
    return dfs[1]


def _fix_county_name(county_name: str) -> str:
    if 'county' in county_name:
        return county_name[:county_name.find('county')].rstrip()
    else:
        return county_name


def _clean_county(df):
    df['county_name'] = df['county_name'].str.lower()
    df['county_name'] = df['county_name'].apply(_fix_county_name)
    return df


def _clean_zips(zipcode_df):
    zipcode_df['county'] = zipcode_df['county'].str.lower()
    zipcode_df.loc[len(zipcode_df)] = ['02101', 'MA', 'suffolk county']
    return zipcode_df


def _process_cpvi(cpvi):
    if cpvi.startswith('R'):
        return int(cpvi.split('+')[1])
    elif cpvi.startswith('D'):
        metric = int(cpvi.split('+')[1])
        return np.negative(metric)
    else:
        return 0


def _clean_cpvi(df):
    df.drop(df.tail(1).index, inplace=True)
    df['pvi'] = df['PVI'].apply(_process_cpvi)
    df['state'] = df['State'].str.upper()
    df = df[['state', 'pvi']]
    return df


# Load and process outside data sources

# County
def load_county_data(filepath):
    df = (load_file(filepath, index_col=0).
          pipe(_clean_county)
          )

    return df


# State
def load_state_data(filepath):
    return load_file(filepath, index_col=0)


# CPI
def load_cpi_data(cpi_url):
    df = (load_from_url(cpi_url).
          pipe(_clean_cpvi)
          )

    return df


# Zipcode
def load_zipcode_data(filepath, index_col=False,
                      dtypes=config.ZIPS_DTYPES, cols=config.COLS['zipcode']):
    df = (load_file(filepath, index_col=index_col, dtypes=dtypes, usecols=cols).
          pipe(_clean_zips)
          )

    return df


# Population density
def load_pop_density(filepath, cols):
    renamed_cols = ['state', 'year', 'pop', 'pop_density']
    df = (load_file(filepath, usecols=cols)
          .query('Year >= 2000')
          .query('`Geography Type` == "State"')
          .drop(columns=['Geography Type'])
          )
    # rename columns
    df.columns = renamed_cols
    df['state'] = df['state'].str.upper()

    return df


# Income
def load_income(filepath, cols):
    df = load_file(filepath, usecols=cols)
    df['income_per_return'] = df['A02650'] / df['N1']
    col_names = ['state', 'zipcode', 'n_returns', 'n_individuals', 'n_elderly_returns',
                    'adjusted_gross_income', 'n_retruns_w_tot_income',
                    'total_income_amount', 'income_per_return']

    df.columns = col_names

    return df
