#!/usr/bin/env bash

# 79: -------------------------------------------------------------------------
# Example demonstrating use of single vs double quotes with variable expansion.
#
# Run the example using: `bash ./ex_variable_expansion.sh`
#
# Author(s): James Henderson
# Updated: September 27, 2020
# 79: -------------------------------------------------------------------------

## define a variable
the_var="the variable"

## single quotes create literal strings and do not allow expansion
echo -n  "Using single quotes: "
echo 'This is $the_var.'

## double quotes allow expansion
echo -n  "Using double quotes: "
echo "This is $the_var."

## the outer quotes are what determines how these work together
echo -n "Double within single: "
echo 'This is "$the_var"'

echo -n "Single within double: "
echo "This is '$the_var'"

