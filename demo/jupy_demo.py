# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   markdown:
#     extensions: footnotes
# ---

# ## Jupytext Demo
# **James Henderson, PhD**  
# *September 9, 2021*
#
# ## About
# This is a demonstration of using [JupyText][jt] based on the `string_df.py`
# script used in the [Tables in Notebooks][tn] slides. 
#
# Jupytext allows Markdown cells to be written as comments to be written
# as comments in a plain text Python script. There are some advantages of this:
#
# 1. Plain text mixing Markdown and Python code is easier for a human to read
# than the underlying json representation of a notebook file (.ipynb). 
#
# 2. This human readability also makes it easier to do version control using
# git.  
#
# 3. Allow you to develop in an IDE like Spyder, then quickly convert to a 
# notebook by addding additional comments intended to become Markdown cells. 
#
# [jt]: https://jupytext.readthedocs.io/en/latest/
# [tn]: https://github.com/jbhender/Stats507_F21/blob/main/nb/tables.ipynb


# ## Example
# In this example, we create a small pandas DataFrame to use as input data
# in the table examples from [Tables in Notebooks][tn]. 
#
# [tn]: https://github.com/jbhender/Stats507_F21/blob/main/nb/tables.ipynb
# The code cell below shows the header of the original file. 

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a small pandas DataFrame for examples.

@author: James Henderson
@date: August 31, 2021
"""
# 79: ------------------------------------------------------------------------

# These are the module imports, if there were more we would collect them
# all here at the top of the script.

# libraries: -----------------------------------------------------------------
import pandas as pd

# Next are two strings that will serve as the "data" forming the rows of the
# tables.

# input strings: -------------------------------------------------------------
str1 = 'To err is human.'
str2 = 'Life is like a box of chocolates.'

# Our example table will show the number and percent of vowels in each of the
# input strings. The function `n_vowels()` counts the number of vowels while
# the function `pct_vowels()` converts this number to a percentage.

# functions: -----------------------------------------------------------------
def n_vowels(s):
    """
    Count the vowels in s.

    Parameters
    ----------
    s : str
        The string in which to count vowels.

    Returns
    -------
    An integer for the count of vowels (a, e, i, o, or u) in s.

    """
    n = 0
    for v in ['a', 'e', 'i', 'o', 'u']:
        n += s.count(v)
    return(n)


def pct_vowels(s, digits=1):
    """
    Return the % of characters in s that are vowels.

    Parameters
    ----------
    s : str
        The string in which to compute the % of vowels.
    digits : int, optional
        Round the % to this many digits. The default is 1.

    Returns
    -------
    The % of vowels among all characters (not just alpha characters) in s.
    """
    n = n_vowels(s)
    pct = round(100 * n / len(s), digits)
    return(pct)

# Finally, we construct the Pandas data frame `dat` using the `DataFrame()`
# constructor with a dictionary input. 

# data frame: ----------------------------------------------------------------
dat = pd.DataFrame(
    {
     "string": [str1, str2],
     "length": [len(str1), len(str2)],
     "% vowels": [pct_vowels(str1), pct_vowels(str2)]
     }
    )
# 79: ------------------------------------------------------------------------

# ## Using Jupytext
# With JupyText installed, this script can be opened by a notebook server.
# From the open notebook, the file can be saved (using a dropdown menu) to 
# a notebook file. 
#
# ### Command Line Use
# Other options for using Jupytext are to convert this file to a notebook
# at the command line: `jupytext --to ipynb jupy_demo.py`.
#
# If you edit and develop the notebook, you can similarly convert the notebook
# file to this python script representation at the command line:
# `jupytext --to py:light jupy_demo.ipynb`. 
#
# ### Pairing
# Another way to use JupyText is to "pair" one or more representations
# (file types). Then, when you save edits to one the other(s) will be updated
# automatically by Jupytext. 

# ## Takeaways
# + Use JupyText to mantain a plain text representation of your notebooks.
# + Markdown cells are created from comments separated from code by one or
#   more blank lines. 
# + I recommend (but don't require) using the `.py` file as your primary
#   representation used for development. 
# + For this class, the *light* format is preferred.  
