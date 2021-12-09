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
    'county': np.str
}

COLS = {
    'users': ['user_id', 'review_count'],
    'business': ['business_id', 'state', 'city', 'postal_code', 'categories', 'stars', 'review_count'],
    'reviews': ['review_id', 'user_id', 'business_id', 'date', 'stars', 'useful'],
    'zipcode': ['zip', 'county']
}