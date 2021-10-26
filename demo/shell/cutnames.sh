#!/usr/bin/env bash

# 79: --------------------------------------------------------------------------     
# Stats 507, Fall 2021
# A command line utility for extracting columns from a csv file by name. 
#
# Note: To make the script executable, use
#   `chmod +x ./cutnames.sh`
#   Otherwise, call as` bash ./cutnames.sh`
#
# # Usage: `./cutnames.sh file expression`     
#   expression should be an *extended* regular expression (-E), see man grep 
#
# Author: James Henderson
# Date: Sep 17, 2020
# 79: --------------------------------------------------------------------------     

# Command line inputs: ---------------------------------------------------------

## First argument is the file we are extracting columns from.
file=$1

## The second argument is an (extended) regular
##  expression for the column names we want.
expr=$2

## Here is where we do the work
if [ ! -f "$file" ]; then
  # This line echos to stderr rather than stdout 
  echo "Could not find file $file." > /dev/stderr
else
  # get column numbers whose names match expr
  cols=$(
   <"$file" head -n1 |
    tr , \\n |   
    grep -n -E "$expr" |
    cut -f1 -d: |
    paste -s -d, -
  )

  # cut those columns out
  <"$file" cut -f"$cols" -d,
fi

# We use "$file" above in the event that the filename 
# contains spaces.

# 79: --------------------------------------------------------------------------  
