# Yelp Data Formatting for Max Yu's Research Project

This repo includes all code for processing Yelp's open reviews dataset. Dataset was downloaded in November 2021.

## Data Dictionary

1. Business zipcode ideology - % Republican votes - % Democrat votes at county level
2. Business state ideology - % Republican votes - % Democrat votes at state level
3. Business state pvi - Cook Partisan Voting Index

## Notes

* PVI does not account for Washington DC which is a district but not a state
* DC rows may need to be removed
* As of November 24, 2021, the notebook outputs a sample of data.
* Fix zip codes that are not 5 digits with leading 0s
* Some zip codes are missing -- figure out what is happening here
* one business column has a typo in the column name

## Dataset sources

* Yelp: https://www.yelp.com/dataset
* Cook Partisan Index: https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index
* Election data: https://electionlab.mit.edu/data
* Zip code to counties: https://simplemaps.com/data/us-zips


## To do

* Transfer notebook code into a script.
* Write code to process entire dataset.