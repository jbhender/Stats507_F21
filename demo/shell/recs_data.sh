#!usr/bin/env bash

# 79: -------------------------------------------------------------------------         
# Download 2009 and 2015 RECS microdata and codebooks.
#
#
# Author: James Henderson (jbhender@umich.edu)
# Updated: Oct 3, 2020
# 79: -------------------------------------------------------------------------

# input parameters: -----------------------------------------------------------
base_url=https://www.eia.gov/consumption/residential/data

# download microdata: ---------------------------------------------------------

## 2009 RECS
if [ ! -f recs2009_public.csv ]; then
    wget $base_url/2009/csv/recs2009_public.csv
fi

## 2009 RECS replicate weights
if [ ! -f recs2009_public_repweights.csv ]; then
    wget $base_url/2009/csv/recs2009_public_repweights.csv
fi

## 2015 RECS (includes replicate weights)
if [ ! -f recs2015_public_v4.csv ]; then
    wget $base_url/2015/csv/recs2015_public_v4.csv
fi

# download codebooks: ---------------------------------------------------------

## 2009
if [ ! -f recs2009_public_codebook.xlsx ]; then
    wget $base_url/2009/xls/recs2009_public_codebook.xlsx
fi

## 2015
if [ ! -f codebook_publicv4.xlsx]; then
    wget $base_url/2015/xls/codebook_publicv4.xlsx
fi

# 79: -------------------------------------------------------------------------
