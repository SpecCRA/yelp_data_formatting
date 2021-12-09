#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Ben Xiao
# Created Date: 2021 Dec 6
# version ='1.0'
# ----------------------------------------------------------------------------

import pandas as pd
import numpy as np

class clean_yelp_data():

    def __init__(self):
        pass

    def fix_zipcode(input_zipcode):
        if len(input_zipcode) < 5:
            to_fill = 5 - len(input_zipcode)
            return (to_fill * '0') + input_zipcode
        else:
            return input_zipcode

    def fix_county_name(county_name):
        assert county_name == str

        if 'county' in county_name:
            return county_name[:county_name.find('county')].rstrip()
        else:
            return county_name

    def match_loc_to_ideology(self, zipcode, zips_df, county_df):
        zipcode_state = zips_df[zips_df['zip'] == zipcode]['state'].iloc[0]
        county_name = self.fix_county_name(zips_df[zips_df['zip'] == zipcode]['county'].iloc[0])

        state_slice = county_df[county_df['state_po'] == zipcode_state]
        ideology_metric = state_slice.loc[state_slice['county_name'] == county_name]['perc_diffs'].iloc[0]

        return ideology_metric

    def process_cpvi(cpvi):
        assert cpvi == str

        if cpvi.startswith('R'):
            return int(cpvi.split('+')[1])
        elif cpvi.startswith('D'):
            cpvi_metric = int(cpvi.split('+')[1])
            return np.negative(cpvi_metric)
        else:
            return
