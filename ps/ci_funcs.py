#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem Set 4, Question 2
Stats 507, Fall 2021

Author: James Henderson
Updated: October 18, 2021
"""
# 79: -------------------------------------------------------------------------

# imports
import numpy as np
from scipy.stats import norm, beta

# confidence interval for a mean
def ci_mean(
    x,
    axis=0,
    level=0.95,
    str_fmt="{mean:.2f} [{level:.0f}%: ({lwr:.2f}, {upr:.2f})]"
):
    """
    Construct an estimate and confidence interval for the mean of `x`.

    Parameters
    ----------
    x : A 1-dimensional NumPy array or compatible sequence type (list, tuple).
        A data vector from which to form the estimates.
    axis : int, optional.
        Axis along which to compute the means and std of x. The default is 0.
        Has only been tested for axis=1 in a 2d array. 
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
    xbar = np.mean(x, axis=axis)
    se = np.std(x, axis=axis, ddof=1) / np.sqrt(x.shape[axis])
    z = norm.ppf(1 - (1 - level) / 2)
    lwr, upr = xbar - z * se, xbar + z * se
    out = {"mean": xbar, "level": 100 * level, "lwr": lwr, "upr": upr}
    # format output
    if str_fmt is None:
        return(out)
    elif xbar.size == 1:
        return(str_fmt.format_map(out))
    else: 
        m = len(xbar)
        out2 = {i: 
                {"mean": xbar[i],
                 "level": 100 * level,
                 "lwr": lwr[i],
                 "upr": upr[i]
                } for i in range(m)}
        return([str_fmt.format_map(out2[i]) for i in range(m)])

# confidence interval for a proportion
def ci_prop(
    x,
    axis=0,
    level=0.95,
    str_fmt="{mean:.2f} [{level:.0f}%: ({lwr:.2f}, {upr:.2f})]",
    method="Normal",
    warn=True
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
    axis : int, optional.
        Axis along which to compute the means and std of x. The default is 0.
        Has only been tested for axis=0 and axis=1 in a 2d array. 
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
    warn: bool, optional
        Whether to issue a warning when using the normal approximation and 
        the assumption that there are at least 12 ones and zeros is not met.  
        The default is True. 

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
    n = x.shape[axis]

    # compute estimate
    if method == 'AC':
        z = norm.ppf(1 - (1 - level) / 2)
        n = (n + z ** 2)
        est = (np.sum(x, axis=axis) + z ** 2 / 2) / n
    else:
        est = np.mean(x, axis=axis)

    # warn for small sample size with "Normal" method
    small_n = np.logical_or((n * est) < 12, (n * (1 - est)) < 12).any()
    if warn == True and method == 'Normal' and small_n:
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
        s = np.sum(x, axis=axis)
        lwr = beta.ppf(alpha / 2, s, n - s + 1)
        upr = beta.ppf(1 - alpha / 2, s + 1, n - s)

    # compute bounds for Jeffrey method
    if method == 'Jeffrey':
        alpha = 1 - level
        s = np.sum(x, axis=axis)
        lwr = beta.ppf(alpha / 2, s + 0.5, n - s + 0.5)
        upr = beta.ppf(1 - alpha / 2, s + 0.5, n - s + 0.5)

    # prepare return values
    out = {"est": est, "level": 100 * level, "lwr": lwr, "upr": upr}
    if str_fmt is None:
        return(out)
    elif est.size == 1:
        return(str_fmt.format_map(out))
    else: 
        m = len(est)
        out2 = {i: 
                {"est": est[i],
                 "level": 100 * level,
                 "lwr": lwr[i],
                 "upr": upr[i]
                } for i in range(m)}
        return([str_fmt.format_map(out2[i]) for i in range(m)])
