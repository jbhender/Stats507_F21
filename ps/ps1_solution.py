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

# ## Problem Set 1, Solution
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *September 22, 2021*
#

# ## Contents
# + [Question 0](#Question-0)
# + [Question 1](#Question-1)
# + [Question 2](#Question-2)
# + [Question 3](#Question-3)
#
# ## Question 0
#
# Below is the rendered Markdown you were asked to reproduce. 
#    
# ---
#
# This is *question 0* for [problem set 1][1] of [Stats 507][2]. 
#
# > Question 0 is about Markdown. 
#
# The next question is about the **Fibonnaci sequence**, 
# $F_n = F_{n-2} + F_{n-1}$. In part **a** we will define a Python 
# function `fib_rec()`. 
#
# Below is a ...
#
# ### Level 3 Header
#
# Next, we can make a bulleted list:  
#
#  - Item 1  
#
#    + detail 1  
#    + detail 2  
#
# - Item 2  
#
# Finally, we can make an enumerated list:  
#
#  a. Item 1    
#  b. Item 2    
#  c. Item 3  
#
# ---
#
# [1]: https://jbhender.github.io/Stats507/F21/ps/ps1.html
# [2]: https://jbhender.github.io/Stats507/F21/
#
# Here is the Markdown I used to produce it. 
#
# ```
#    
# ---
#
# This is *question 0* for [problem set 1][1] of [Stats 507][2]. 
#
# > Question 0 is about Markdown. 
#
# The next question is about the **Fibonnaci sequence**, 
# $F_n = F_{n-2} + F_{n-1}$. In part **a** we will define a Python 
# function `fib_rec()`. 
#
# Below is a ...
#
# ### Level 3 Header
#
# Next, we can make a bulleted list:  
#
#  - Item 1  
#
#    + detail 1  
#    + detail 2  
#
# - Item 2  
#
# Finally, we can make an enumerated list:  
#
#  a. Item 1    
#  b. Item 2    
#  c. Item 3  
#
# ---
#
# [1]: https://jbhender.github.io/Stats507/F21/ps1.html
# [2]: https://jbhender.github.io/Stats507/F21/
# ```

# ## Imports
# The remaining questions will use the following imports.

# modules: --------------------------------------------------------------------
import numpy as np
import pandas as pd
from math import floor 
from timeit import Timer
from collections import defaultdict
from IPython.core.display import display, HTML
from scipy.stats import norm, binom, beta
from warnings import warn
# 79: -------------------------------------------------------------------------

# ## Question 1
#
# In this question, we write and compare the computational efficiency of
# several different functions for producing Fibonacci numbers.

# ### Test function
# The function below takes a function, `fib`, and check that it returns
# the correct $7^{th}$, $11^{th}$ and $13^{th}$ Fibonacci numbers.


def test_fib(fib):
    """
    Test if function fib returns correct Fibonacci numbers at 7, 11, and 13.

    Parameters
    ----------
    fib : function
        A function taking an integer `n` and returns the Fibonacci number F_n.

    Returns
    -------
    A bool that is True when [fib(7), fib(11), fib(13)] == [13, 89, 233].

    """
    return([fib(i) for i in (7, 11, 13)] == [13, 89, 233])


# ### a) `fib_rec()`
# Sequential computation using a recursive strategy. Note the re-use of the
# starting values to achieve a linear-time complexity.  We recongize this by
# noting that `fib_rec(n)` calls `fib_rec()` once for each recursion or a total
# of `n` times.  If you call `fib_rec()` twice on each call you end up with
# exponential complexity scaling like $2^n$. 


def fib_rec(n, a=0, b=1):
    """
    Compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.
    
    This function computes $F_n$ using a linear-complexity recursion.

    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$.
    a, b : int, optional.
        Values to initalize the sequence $F_0 = a$, $F_1 = b$.

    Returns
    -------
    The Fibonacci number $F_n$.

    """
    if n == 0:
        return(a)
    elif n == 1:
        return(b)
    else:
        a, b = b, a + b
        return(fib_rec(n - 1, a, b))


assert test_fib(fib_rec)


# ### b) `fib_for()`
# In the next function we compute Fibonacci numbers in a similar strategy as
# for `fib_rec()` but avoid the "overhead" of recursively dispatching the
# the function.


def fib_for(n, a=0, b=1):
    """
    Compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ directly by iterating using a for loop.

    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$. 
    a, b : int, optional.
        Values to initialize the sequence $F_0 = a$, $F_1 = b$. 

    Returns
    -------
    The Fibonacci number $F_n$. 

    """
    if n == 0:
        return(a)
    elif n == 1:
        return(b)
    else:
        for i in range(n - 1):
            a, b = b, a + b
        return(b)


assert test_fib(fib_for)


# ### c) `fib_whl()`
# This version is nearly identical to `fib_for()` but uses a while loop to
# iterate.


def fib_whl(n, a=0, b=1):
    """
    Compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ by direct summation, iterating using a
    while loop.

    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$.
    a, b : int, optional.
        Values to initialize the sequence $F_0 = a$, $F_1 = b$.

    Returns
    -------
    The Fibonacci number $F_n$.

    """
    if n == 0:
        return(a)
    elif n == 1:
        return(b)
    else:
        i = 1
        while i < n:
            a, b = b, a + b
            i += 1
        return(b)


assert test_fib(fib_whl)


# ### d) `fib_rnd()`
# This is our first function that avoids iteration altogether by using a 
# direct computation method, namely, we find $F_n$ by rounding 
# $\phi^n / sqrt(5)$. 
#
# Unlike Python's built-in integers, the NumPy ints used 
# here cannot be arbitrarily large. A computation resulting in an integer 
# (or float) larger than can be accommodated by the number of bits used to
# represent it typically results in an *overflow* error. In the function
# below, we extend the range of inputs by computing the approximation on 
# the log scale. This allows for larger inputs, because $\phi^n / \sqrt{5}$ is
# smaller than $\phi^n$.
#
# As you can see below in the test, the rounding method becomes inaccurate
# on account of floating point precision beginning with $n = 71$. You were
# not expected to recognize or discuss this, but kudos if you did. 


def fib_rnd(n):
    r"""
    Directly compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ by rounding $\phi^n / sqrt(5)$.
    The formula is used directly for n < 250, and is applied on the log scale
    for 250 <= n < 1478. A ValueError is raised for larger n to avoid
    overflow errors.


    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$, must be less than 1478.
    a, b : int, optional.
        Values to initialize the sequence $F_0 = a$, $F_1 = b$.

    Returns
    -------
    The Fibonacci number $F_n$ if n < 1478, else a ValueError.
    """
    if n < 250:
        return(
            round(((1 + 5 ** 0.5) / 2) ** n / (5 ** 0.5))
        )
    elif n < 1478:
        return(
            round(
                np.exp(n * np.log((1 + np.sqrt(5)) / 2) - 0.5 * np.log(5))
            )
        )
    else:
        raise ValueError('Values of n > 1477 lead to an infinite float.')


assert test_fib(fib_rnd)
i = 1
while (fib_rnd(i) == fib_for(i)):
    i += 1
fib_log = round(np.exp(i * np.log((1 + np.sqrt(5)) / 2) - 0.5 * np.log(5)))
assert fib_log == fib_rnd(i)
(i, fib_rnd(i), fib_for(i), fib_rnd(i) - fib_for(i), fib_log)


# ### e) `fib_flr()`
# This is another direction computation method, by adding 0.5 to the 
# approximation used in `fib_rnd()` we can replace rounding with integer
# truncation. Here, I use `int()` to truncate the approximations but you
# could also use `floor()`. 
#
# As with `fib_rnd()` the results becomes inaccurate from $n = 71$ due to
# finite floating point precision.  


def fib_flr(n):
    r"""
    Directly compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ by finding the smallest integer less than
    $\phi^n / sqrt(5) + 0.5$. The formula is used directly for n < 250, and is
    applied on the log scale for 250 <= n < 1477. A ValueError is raised for
    larger n to avoid integer overflow.


    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$, must be less than 1478.
    a, b : int, optional.
        Values to initialize the sequence $F_0 = a$, $F_1 = b$.

    Returns
    -------
    The Fibonacci number $F_n$ if n < 1477, else a ValueError.
    """
    if n < 250:
        return(
            int(((1 + 5 ** 0.5) / 2) ** n / (5 ** 0.5) + 0.5)
            )
    elif n < 1477:
        return(
                int(
                    np.exp(
                        n * np.log((1 + np.sqrt(5)) / 2) - 0.5 * np.log(5)
                    ) + 0.5
                )
            )
    else:
        raise ValueError('Values of n > 1476 lead to an infinite float.')


assert test_fib(fib_flr)
i = 1
while (fib_flr(i) == fib_for(i)):
    i += 1
fib_log = int(np.exp(i * np.log((1 + np.sqrt(5)) / 2) - 0.5 * np.log(5)) + 0.5)
assert fib_log == fib_flr(i)
(i, fib_flr(i), fib_for(i), fib_flr(i) - fib_for(i), fib_log)


# ### f) Comparisons
# In the code cell below, I compare the functions above using the median
# computation time on each of the following four integers: 21, 43, 233, and
# 1001. The median computation time is estimated with the sample median from
# 10,000 timing runs.

# timing comparisons: ---------------------------------------------------------
n_mc = 10000
res = defaultdict(list)
n_seq = [21, 42, 233, 1001]
res['n'] = n_seq
for f in (fib_rec, fib_for, fib_whl, fib_rnd, fib_flr):
    for n in n_seq:
        t = Timer("f(n)", globals={"f": f, "n": n})
        m = np.median([t.timeit(1) for i in range(n_mc)]) 
        res[f.__name__].append(round(m * 1e6, 1))

# construct a table, include a caption: ---------------------------------------
cap = """
<b> Table 1.</b> <em> Timing comparisons for Fibonacci functions.</em>
Median computation times, in micro seconds, from 10,000 trial runs at
each n.  While the direct computation methods are faster, they become 
inaccurate for n > 71 due to finite floating point precision. 
"""
res = pd.DataFrame(res)
t1 = res.to_html(index=False)
t1 = t1.rsplit('\n')
t1.insert(1, cap)
tab1 = ''
for i, line in enumerate(t1):
    tab1 += line
    if i < (len(t1) - 1):
        tab1 += '\n'

display(HTML(tab1))

# ### Question 2
# In this question, you write a small function to compute rows of Pascal's
# triangle.  Then, you write a second function to print Pascal's triangle
# with conventional spacing and *approximate* symmetry. 

# a) Compute a row of Pascal's triangle.
# This function computes a single row for Pascal's triangle. For large "n"
# it would be more efficient to compute only half the row and to include a
# parameter for whether to reverse and append a half row to form a whole row.


def pascal(n):
    """
    Compute an arbitrary row of Pacal's triangle.

    Row 0 is "1", row 1 is "1, 1".  

    Parameters
    ----------
    n : int
        The desired row.
 
    Returns
    -------
    A list with values for the desired row. 
    """
    den = list(range(n + 1))
    out = den.copy()
    den.pop(0)
    out[0] = 1
    for k in den:
        out[k] = int(out[k - 1] * (n + 1 - k) / k)
    return out

# ### b) Displaying Pascal's triangle
# Without fractional spacing, it isn't possible to construct a triangle
# with perfect symmetry.  In the example solution, I've chosen a compact
# representation with minimal spacing to allow for staggering. A solution
# using uniform spacing would also be suitable.  

def pascal_display(n, compact=True):
    """
    Compute an arbitrary row of Pacal's triangle.

    Row 0 is "1", row 1 is "1, 1".  

    Parameters
    ----------
    n : int
        The desired number of rows.
    compact : bool, optional.
        If True, return a compact representation with minimal spacing. 
        Otherwise, return a representation with uniform spacing. 
        The default is True. 
 
    Returns
    -------
    A string which, when printed, displays the first n rows. 
    """
    # base "cell" size of of final two rows
    
    # special case with a single row
    if n == 0:
        return('1\n')

    # determine cell sizes using the two base rows
    row0 = pascal(n)
    row1 = pascal(n - 1)
    m = n // 2 + 1
    cell_size = []
    for i, j in zip(row0[0:m], row1[0:m]):
        cell_size.extend([len(str(i)), len(str(j))])    
    if n % 2 == 0:
        cell_size.pop()
    cell_size = list(reversed(cell_size))
    if not compact == True:
        mx = max(cell_size)
        cell_size = [mx for i in cell_size]
    tot_size = 2 * sum(cell_size[0:len(cell_size)]) + cell_size[-1]
    
    # construct row-by-bow
    out = ''
    for i in range(n + 1):
        row = pascal(i)
        row = row[0:(i // 2 + 1)]
        if i % 2 == 0:
            for k, v in enumerate(reversed(row)):
                num = cell_size[2 * k]
                v = str(v)
                if k == 0:
                    row_str = v.rjust(num)
                else:
                    row_str = v.rjust(num) + row_str + v.rjust(num)
                if k < (len(row) - 1):
                    spc = cell_size[2 * k + 1]
                    row_str = ''.rjust(spc) + row_str + ''.rjust(spc)
        else:   
            for k, v in enumerate(reversed(row)):
                spc, num = cell_size[2 * k], cell_size[2 * k + 1]
                v = str(v)
                if k == 0:
                    row_str = v.rjust(num) + ''.rjust(spc) + v.rjust(num)
                else:
                    row_str = ''.rjust(spc) + row_str + ''.rjust(spc)
                    row_str = v.rjust(num) + row_str + v.rjust(num)
        # append rows
        row_str = row_str.center(tot_size)        
        out += row_str + '\n'    
    return(out)

# Here is the compact representation for the first 10 rows.

print(pascal_display(10))


# Here is the uniform representation for the first 10 rows. 

print(pascal_display(10, compact=False))

# ## Question 3
# In this question you wrote two functions: one for returning a point and 
# interval estimate for the mean as a formatted string and a second doing
# the same for a proportion using various methods. 

# ### a) Confidence interval for the mean. 


def ci_mean(
    x,
    level=0.95,
    str_fmt="{mean:.2f} [{level:.0f}%: ({lwr:.2f}, {upr:.2f})]"
):
    """
    Construct an estimate and confidence interval for the mean of `x`.

    Parameters
    ----------
    x : A 1-dimensional NumPy array or compatible sequence type (list, tuple).
        A data vector from which to form the estimates.
    level : float, optional.
        The desired confidence level, converted to a percent in the output.
        The default is 0.95.
    str_fmt: str or None, optional.
        If `None` a dictionary with entries `mean`, `level`, `lwr`, and
        `upr` whose values give the point estimate, confidence level (as a %),
        lower and upper confidence bounds, respectively. If a string, it's the
        result of calling the `.format_map()` method using this dictionary.
        The default is "{mean:.2f} [{level:.0f}%: ({lwr:.2f}, {upr:.2f})]".

    Returns
    -------
    By default, the function returns a string with a 95% confidence interval
    in the form "mean [95% CI: (lwr, upr)]". A dictionary containing the mean,
    confidence level, lower, bound, and upper bound can also be returned.

    """
    # check input
    try:
        x = np.asarray(x)  # or np.array() as instructed.
    except TypeError:
        print("Could not convert x to type ndarray.")

    # construct estimates
    xbar = np.mean(x)
    se = np.std(x, ddof=1) / np.sqrt(x.size)
    z = norm.ppf(1 - (1 - level) / 2)
    lwr, upr = xbar - z * se, xbar + z * se
    out = {"mean": xbar, "level": 100 * level, "lwr": lwr, "upr": upr}
    # format output
    if str_fmt is None:
        return(out)
    else:
        return(str_fmt.format_map(out))


# ### b) Confidence intervals for population proportions.  


def ci_prop(
    x,
    level=0.95,
    str_fmt="{mean:.2f} [{level:.0f}%: ({lwr:.2f}, {upr:.2f})]",
    method="Normal"
):
    """
    Construct point and interval estimates for a population proportion.

    The "method" argument controls the estimates returned. Available methods
    are "Normal", to use the normal approximation to the Binomial, "CP" to
    use the Clopper-Pearson method, "Jeffrey" to use Jeffery's method, and
    "AC" for the Agresti-Coull method.

    By default, the function returns a string with a 95% confidence interval
    in the form "mean [level% CI: (lwr, upr)]". Set `str_fmt=None` to return
    a dictionary containing the mean, confidence level (%-scale, level),
    lower bound (lwr), and upper bound (upr) can also be returned.

    Parameters
    ----------
    x : A 1-dimensional NumPy array or compatible sequence type (list, tuple).
        A data vector of 0/1 or False/True from which to form the estimates.
    level : float, optional.
        The desired confidence level, converted to a percent in the output.
        The default is 0.95.
    str_fmt: str or None, optional.
        If `None` a dictionary with entries `mean`, `level`, `lwr`, and
        `upr` whose values give the point estimate, confidence level (as a %),
        lower and upper confidence bounds, respectively. If a string, it's the
        result of calling the `.format_map()` method using this dictionary.
        The default is "{mean:.1f} [{level:0.f}%: ({lwr:.1f}, {upr:.1f})]".
    method: str, optional
        The type of confidence interval and point estimate desired.  Allowed
        values are "Normal" for the normal approximation to the Binomial,
        "CP" for a Clopper-Pearson interval, "Jeffrey" for Jeffrey's method,
        or "AC" for the Agresti-Coull estimates.

    Returns
    -------
    A string with a (100 * level)% confidence interval in the form
    "mean [(100 * level)% CI: (lwr, upr)]" or a dictionary containing the
    keywords shown in the string.

    """
    # check input type
    try:
        x = np.asarray(x)  # or np.array() as instructed.
    except TypeError:
        print("Could not convert x to type ndarray.")

    # check that x is bool or 0/1
    if x.dtype is np.dtype('bool'):
        pass
    elif not np.logical_or(x == 0, x == 1).all():
        raise TypeError("x should be dtype('bool') or all 0's and 1's.")

    # check method
    assert method in ["Normal", "CP", "Jeffrey", "AC"]

    # determine the length
    n = x.size

    # compute estimate
    if method == 'AC':
        z = norm.ppf(1 - (1 - level / 2))
        n = (n + z ** 2)
        est = (np.sum(x) + z ** 2 / 2) / n
    else:
        est = np.mean(x)

    # warn for small sample size with "Normal" method
    if method == 'Normal' and (n * min(est, 1 - est)) < 12:
        warn(Warning(
            "Normal approximation may be incorrect for n * min(p, 1-p) < 12."
        ))

    # compute bounds for Normal and AC methods
    if method in ['Normal', 'AC']:
        se = np.sqrt(est * (1 - est) / n)
        z = norm.ppf(1 - (1 - level) / 2)
        lwr, upr = est - z * se, est + z * se

    # compute bounds for CP method
    if method == 'CP':
        alpha = 1 - level
        s = np.sum(x)
        lwr = beta.ppf(alpha / 2, s, n - s + 1)
        upr = beta.ppf(1 - alpha / 2, s + 1, n - s)

    # compute bounds for Jeffrey method
    if method == 'Jeffrey':
        alpha = 1 - level
        s = np.sum(x)
        lwr = beta.ppf(alpha / 2, s + 0.5, n - s + 0.5)
        upr = beta.ppf(1 - alpha / 2, s + 0.5, n - s + 0.5)

    # prepare return values
    out = {"mean": est, "level": 100 * level, "lwr": lwr, "upr": upr}
    if str_fmt is None:
        return(out)
    else:
        return(str_fmt.format_map(out))


# ## c) Comparisons
# In this section you were asked to compare the 90, 95, and 99% confidence
# intervals from each of the methods above.
# The intervals produced by Jeffrey's method have the smallest width.

# construct the intervals: ----------------------------------------------------
x = np.array(48 * [0] + 42 * [1])
fmt = '({lwr:.4f}, {upr:.4f})'
tab3c = defaultdict(list)
res3c = defaultdict(list)
for lvl in [.9, .95, .99]:
    tab3c['level'].append('{0:.0f}% CI'.format(100 * lvl))
    tab3c['Mean'].append(ci_mean(x, lvl, fmt))
    res3c['Mean'].append(ci_mean(x, lvl, None))
    for m in ['Normal', 'AC', 'CP', 'Jeffrey']:
        tab3c[m].append(ci_prop(x, lvl, fmt, m))
        res3c[m].append(ci_prop(x, lvl, None, m))

tab3c = pd.melt(pd.DataFrame(tab3c), id_vars='level')
tab3c = pd.pivot(tab3c, index='variable', columns='level', values='value')
tab3c.index.name = 'Method'

# add a caption: --------------------------------------------------------------
cap = """
<b> Table 2.</b> <em> Comparing confidence intervals for proportions.</em>
Using an input vector with 42 of 90 successes, this table comapres the 90,
95, and 99% Confidence intervals constructed according to 5 different methods. 
"""
t2 = tab3c.to_html()
t2 = t2.rsplit('\n')
t2.insert(1, cap)
tab2 = ''
for i, line in enumerate(t2):
    tab2 += line
    if i < (len(t2) - 1):
        tab2 += '\n'

display(HTML(tab2))


# show the interval with the smallest width: ----------------------------------
width = defaultdict(list)
width['Level'] = ['90%', '95%', '99%']
for k, v in res3c.items():
    width[k] = [i['upr'] - i['lwr'] for i in v]
width = pd.DataFrame(width).set_index('Level')
width.where(width.isin(width.min(axis=1))).dropna(axis=1)

# ---
