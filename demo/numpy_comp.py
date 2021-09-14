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
    return(a.__class__([i * j for i, j in zip(a, b)]))


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
    return(a.__class__([j * b[i] for i, j in enumerate(a)]))


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
    return(a.__class__(np.asarray(a) * np.asarray(b)))


# confirm functions return the same values: ----------------------------------
n = 10000
a = list(np.linspace(0, 1, num=n))
b = list(np.linspace(0, 2 * np.pi, num=n))

c0 = mult_doc(a, b)
c1 = mult_zip(a, b)
c2 = mult_enum(a, b)
c3 = mult_np(a, b)

assert c0 == c1 == c2 == list(c3)

# timing: --------------------------------------------------------------------

# list input
time = defaultdict(list)
for f in [mult_doc, mult_zip, mult_enum, mult_np]:
    t = Timer('f(a, b)', globals={'f': f, 'a': a, 'b': b})
    tm = t.repeat(repeat=10, number=1000)
    time['Function'].append(f.__name__)
    time['min, s'].append(np.min(tm))
    time['median, s'].append(np.median(tm))
    time['mean, s'].append(np.mean(tm))

time = pd.DataFrame(time)

for c, d in zip(time.columns, time.dtypes):
    if d == np.dtype('float64'):
        time[c] = time[c].map(lambda x: '%5.3f' % x)

print(time.to_markdown(index=False))

# ndarray input
a = np.asarray(a)
b = np.asarray(b)
time_nda = defaultdict(list)
for f in [mult_doc, mult_zip, mult_enum, mult_np]:
    t = Timer('f(a, b)', globals={'f': f, 'a': a, 'b': b})
    tm = t.repeat(repeat=10, number=1000)
    time_nda['Function'].append(f.__name__)
    time_nda['min, s'].append(np.min(tm))
    time_nda['median, s'].append(np.median(tm))
    time_nda['mean, s'].append(np.mean(tm))

time_nda = pd.DataFrame(time_nda)
for c, d in zip(time_nda.columns, time_nda.dtypes):
    if d == np.dtype('float64'):
        time_nda[c] = time_nda[c].map(lambda x: '%5.3f' % x)

print(time_nda.to_markdown(index=False))
