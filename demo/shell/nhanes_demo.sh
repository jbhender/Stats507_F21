#!usr/bin/env bash

# 79: -------------------------------------------------------------------------         
# Download and combine NHANES Demographics data 
# from the 2011-2012 to 2017-2018 cycles.
#
# This is the pattern for the urls, the years and final letters are
# listed in `ps1_nhanes_files.txt`:
#  > https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT
#
# For the dentition exams, we extract a subset of relevant
# variables.
#
# Author: James Henderson
# Updated: Sep 17, 2020
# 79: -------------------------------------------------------------------------

# input parameters: -----------------------------------------------------------
new_file='nhanes_demo.csv'
wgt_regex='RIDSTATR|SDMVPSU|SDMVSTRA|WTMEC2YR|WTINT2YR'
col_regex="SEQN|RIDAGEYR|RIDRETH3|DMDEDUC2|DMDMARTL|$wgt_regex"

# download and prepare dentition data: ----------------------------------------

## loop over cohorts to download and convert to csv
while read cohort id; do
   
    ### Define variables
    url=https://wwwn.cdc.gov/Nchs/Nhanes/$cohort/DEMO_$id.XPT
    xpt_file=DEMO_$id.XPT
    csv_file=DEMO_$id.csv

    ### Don't redownload if csv file is present
    if [ ! -f $csv_file ]; then
	
	### Download data if not present
	if [ ! -f $xpt_file ]; then
	    wget $url
	fi

	### Convert files to csv using R
	read="haven::read_xpt('$xpt_file')"
	write="data.table::fwrite($read, file = '$csv_file')"
	Rscript -e "$write" # Double quotes allow expansion

    fi

done < ps1_nhanes_files.txt

# Extract columns and append files: -------------------------------------------
if [ -f $new_file ]; then
    echo File $new_file already exists, move or delete.
else
    ## get the headers 
    while read cohort id; do
	bash ./cutnames.sh DEMO_$id.csv $col_regex |
            head -n1 >> $new_file.tmp
    done < ps1_nhanes_files.txt

    ## verify the columns all match in the right order 
    if [ $(< $new_file.tmp uniq | wc -l ) != 1 ]; then
	echo Matching columns are not identical: see $new_file.tmp.
    else
	echo Columns match, appending ...
	## headers for $new_file and cleanup
	< $new_file.tmp head -n1 > $new_file
	rm $new_file.tmp
    
	## add the data
	while read cohort id; do
	    bash ./cutnames.sh DEMO_$id.csv $col_regex |
		tail -n+2 >> $new_file
	done < ps1_nhanes_files.txt
    fi
fi

# 79: -------------------------------------------------------------------------
