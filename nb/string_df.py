#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a small pandas DataFrame for examples.

@author: James Henderson
@date: August 31, 2021
"""
# 79: ------------------------------------------------------------------------

# libraries: -----------------------------------------------------------------
import pandas as pd

# input strings: -------------------------------------------------------------
str1 = 'To err is human.'
str2 = 'Life is like a box of chocolates.'

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
        Roun the % to this many digits. The default is 1.

    Returns
    -------
    The % of vowels among all characters (not just alpha characters) in s.
    """
    n = n_vowels(s)
    pct = round(100 * n / len(s), digits)
    return(pct)


# data frame: ----------------------------------------------------------------
dat = pd.DataFrame(
    {
     "string": [str1, str2],
     "length": [len(str1), len(str2)],
     "% vowels": [pct_vowels(str1), pct_vowels(str2)]
     }
    )

# 79: ------------------------------------------------------------------------
