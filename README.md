# Yelp Data Formatting for Max Yu's Research Project

This repo includes all code for processing Yelp's open reviews dataset. Dataset was downloaded in November 2021.

## Data Dictionary

1. Business zipcode ideology - % Republican votes - % Democrat votes at county level
2. Business state ideology - % Republican votes - % Democrat votes at state level
3. Business state PVI - Cook Partisan Voting Index
4. Population density - TBD

## Notes

* PVI does not account for Washington DC which is a district but not a state
* DC rows may need to be removed.
* As of November 24, 2021, the notebook outputs a sample of data.
* Date data (year, month, day) are all based on the review date.
* Data only contains restaurants.
* Data only contains businesses from 29 of 50 states.


## Dataset sources

* Yelp: https://www.yelp.com/dataset
* Cook Partisan Index: https://en.wikipedia.org/wiki/Cook_Partisan_Voting_Index
* Election data: https://electionlab.mit.edu/data
* Zip code to counties: https://simplemaps.com/data/us-zips
* Population density: https://www.census.gov/data/tables/time-series/dec/density-data-text.html


## To do

* Transfer notebook code into a script.
* Write code to process entire dataset.
* Filter out businesses that are not restaurants. - DONE
* Fix zip codes that are not 5 digits with leading 0s - DONE
* Some zip codes are missing -- figure out what is happening here - DONE
* One business column has a typo in the column name - DONE
* Add population density of county and/or state through census data - DONE
* Split date into separate year, month, and day columns. - DONE
* Upload accompanying state, CPI, and county data files to drive. - DONE
* Rewrite average rating cell to process more efficiently.
* Add a visual map of what states are included within dataset.
* Make a bar chart to count how many reviews are in each state.