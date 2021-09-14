#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
"""
Compare timings of different multiplication strategies to NumPy.

Author: James Henderson
Updated: September 14, 2021
"""

# modules: -------------------------------------------------------------------
import numpy as np
import pandas as pd
from collections import defaultdict
from timeit import Timer


# example from numpy documentation: ------------------------------------------
def mult_doc(a, b):
    """
    Multiply two sequences a and b using a for loop.

    Parameters
    ----------
    a, b : sequence types (e.g. list or tuple) or compatible 1d ndarrays.
        The sequences to be multiplied.

    Returns
    -------
    The element-wise product, `a * b`, with class the same as `a`.

    """
    c = []
    for i in range(len(a)):
        c.append(a[i] * b[i])
    return(c)


# two more "pythonic" implementations: ---------------------------------------
def mult_zip(a, b):
    """
    Multiply two sequences a and b using zip and a list comprehension.

    Parameters
    ----------
    a, b : sequence types (e.g. list or tuple) or compatible 1d ndarrays.
        The sequences to be multiplied.

    Returns
    -------
    The element-wise product, `a * b`, with class the same as `a`.

    """
    out = [i * j for i, j in zip(a, b)]
    if isinstance(a, np.ndarray):
        return(out)
    else:
        return(a.__class__(out))


def mult_enum(a, b):
    """
    Multiply two sequences a and b using enumerate and a list comprehension.

    Parameters
    ----------
    a, b : a sequence type (e.g. list or tuple) or compatible 1d ndarray.
        The sequences to be multiplied.

    Returns
    -------
    The element-wise product, `a * b`, with class the same as `a`.

    """
    out = [j * b[i] for i, j in enumerate(a)]
    if isinstance(a, np.ndarray):
        return(out)
    else:
        return(a.__class__(out))
    return(a.__class__())


# a numpy implementation: ----------------------------------------------------
def mult_np(a, b):
    """
    Multiply two sequences a and b using NumPy.

    Parameters
    ----------
    a, b : a 1d ndarray or a compatible sequence type (e.g. list or tuple)
        The sequences to be multiplied.

    Returns
    -------
    The element-wise product, `a * b`, with class the same as `a`.

    """
    out = np.asarray(a) * np.asarray(b)
    if isinstance(a, np.ndarray):
        return(out)
    else:
        return(a.__class__(out))


# confirm functions return the same values: ----------------------------------
# test with ndarray input
n = 10000
a = np.linspace(0, 1, num=n)
b = np.linspace(0, 2 * np.pi, num=n)

c0 = mult_doc(a, b)
c1 = mult_zip(a, b)
c2 = mult_enum(a, b)
c3 = mult_np(a, b)

assert np.all(c0 == c1 == c2 == c3)

# test with list input
a = list(a)
b = list(b)

c0 = mult_doc(a, b)
c1 = mult_zip(a, b)
c2 = mult_enum(a, b)
c3 = mult_np(a, b)

assert c0 == c1 == c2 == c3

# timing with ndarray input: -------------------------------------------------
a = np.asarray(a)
b = np.asarray(b)
time_nda = defaultdict(list)
for f in [mult_doc, mult_zip, mult_enum, mult_np]:
    t = Timer('f(a, b)', globals={'f': f, 'a': a, 'b': b})
    tm = t.repeat(repeat=10, number=100)
    time_nda['Function'].append(f.__name__)
    time_nda['min, s'].append(np.min(tm))
    time_nda['median, s'].append(np.median(tm))
    time_nda['mean, s'].append(np.mean(tm))

time_nda = pd.DataFrame(time_nda)
for c, d in zip(time_nda.columns, time_nda.dtypes):
    if d == np.dtype('float64'):
        time_nda[c] = time_nda[c].map(lambda x: '%5.3f' % x)
time_nda

# timing with list input: ----------------------------------------------------
a = list(a)
b = list(b)
time_lst = defaultdict(list)
for f in [mult_doc, mult_zip, mult_enum, mult_np]:
    t = Timer('f(a, b)', globals={'f': f, 'a': a, 'b': b})
    tm = t.repeat(repeat=10, number=100)
    time_lst['Function'].append(f.__name__)
    time_lst['min, s'].append(np.min(tm))
    time_lst['median, s'].append(np.median(tm))
    time_lst['mean, s'].append(np.mean(tm))

time_lst = pd.DataFrame(time_lst)
for c, d in zip(time_lst.columns, time_lst.dtypes):
    if d == np.dtype('float64'):
        time_lst[c] = time_lst[c].map(lambda x: '%5.3f' % x)
time_lst
