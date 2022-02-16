#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

USER_DTYPES = {
    'user_id': np.str,
    'review_count': np.int
}

BUSINESS_DTYPES = {
    'business_id': np.str,
    'state': np.str,
    'city': np.str,
    'postal_code': np.str,
    'categories': np.str,
    'review_count': np.int,
    'stars': np.float,
}

REVIEW_DTYPES = {
    'review_id': np.str,
    'user_id': np.str,
    'business_id': np.str,
    'stars': np.int,
    'useful': np.int
}

ZIPS_DTYPES = {
    'zip': np.str,
    'state': np.str,
    'county': np.str
}

INCOME_DTYPES = {
    'STATE': np.str,
    'zipcode': np.str,
    'ELDERLY': np.int,
    'N1': np.int,
    'N2': np.int,
    'A00100': np.float,
    'N02550': np.float,
    'N02650': np.float,
    'A02650': np.float
}

COLS = {
    'users': ['user_id', 'review_count'],
    'county': ['state_po', 'county_name', 'perc_diffs'],
    'business': ['business_id', 'state', 'city', 'postal_code', 'categories', 'stars', 'review_count'],
    'reviews': ['review_id', 'user_id', 'business_id', 'date', 'stars', 'useful'],
    'zipcode': ['zip', 'state', 'county'],
    'population': ['Name', 'Year', 'Resident Population', 'Geography Type', 'Resident Population Density'],
    'income': ['STATE', 'zipcode', 'N1', 'N2', 'ELDERLY', 'A00100', 'N02650', 'A02650']
}

FILENAMES = {
    
}