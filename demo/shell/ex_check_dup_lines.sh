#!/usr/bin/env bash

# 79: -------------------------------------------------------------------------  
# Example showing how to check for duplicate lines in a file from the shell.
#
# Run the example using, e.g.:
# `bash ./ex_check_dup_lines.sh nhanes_files.txt`
# `bash ./ex_check_dup_lines.sh dup.txt`
# 
# Author(s): James Henderson
# Updated: September 18, 2020
# 79: -------------------------------------------------------------------------

## comamnd line variables
file=$1

## version 1
uniq_lines=$(< $file sort | uniq | wc -l)
n_lines=$(< $file wc -l)

if [ $uniq_lines == $n_lines ]; then
    echo "No duplicates in $file."
else
    echo "Total lines in $file:" $n_lines, Unique lines: $uniq_lines.
fi


# 79: -------------------------------------------------------------------------
