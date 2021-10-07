---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Resampling </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Resampling Methods
*Stats 507, Fall 2021*

James Henderson, PhD  
October 5 & 7, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
  - [Resampling](#/slide-3-0)
  - The [Bootstrap](#/slide-4-0)
  - Bootstrap [Example](#/slide-5-0)
  - Permutation Tests (TBD)
  - [Takeaways](#/slide-6-0)
 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Resampling
- [Resampling](https://en.wikipedia.org/wiki/Resampling_(statistics)) is an
   umbrella term for a number of statistical techniques used to estimate 
   quantities related to the sampling distribution of an estimator.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Resampling Methods
- Techniques that fall under the resampling umbrella include:  
  + the bootstrap
  + sub-sampling or the "m out of n" bootstrap
  + the jack-knife
  + permutation testing
  + cross validation.

- The utility of all of these techniques is greatly enhanced by the ability to 
  automate the resampling process and subsequent computations.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Bootstrap 
- The bootstrap is a generic statistical method for estimating the variance 
  of an estimator.
- Used to find confidence intervals when exact or 
  asymptotic analytic formulas are unavailable or unsatisfactory.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Non-parametric Bootstrap  
- The basic idea of the bootstrap is to build up the sampling distribution of
  an estimator by resampling the data many times. 
- In the _non-parametric bootstrap_  this is done by drawing $B$ copies of the
  data from the empirical distribution, $\mathbb{P}$: 

$$
  X_1, \dots, X_n \sim_{iid} P, \qquad 
 \mathbb{P}(t) = \frac{1}{n} \sum_{i=1}^n 1[X_i \le t]
$$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Parametric Bootstrap
- In the _parametric bootstrap_ the data are instead re-sampled from an
  (assumed) parametric (e.g. Gaussian) estimate of $P$. 
- For a comparison of the parametric and non-parametric bootstrap see the
  slides from [this talk][taob] by Robert Tibshirani.  

[taob]: https://statweb.stanford.edu/~tibs/ftp/guelph.ps
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Bootstrap Confidence Intervals  
- There are various methods for constructing a confidence interval for an 
  estimator $\bar{\theta}(X)$ using a bootstrap sample.
- The one I will emphasize is the _percentile method_ in which the
  confidence bounds are taken as sample quantiles from the bootstrap 
  distribution of the estimator.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Bootstrap - Percentile Method 
- For example, if $\hat P(t)$ is the empirical distribution function of 
  $\bar{\theta}(X)$, then a 95% confidence interval estimated using the 
  percentile method is: $\left(\hat{P}^{-1}(.025), \hat{P}^{-1}(.975)\right)$. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Imports
- Here are the imports we'll use in these slides. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# model imports
import numpy as np
import pandas as pd
from scipy.stats import t, bootstrap
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import statsmodels.api as sm
from os.path import exists
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Figure Settings
- Here is one way to create global settings for figure appearance.
- [Hat tip][ht]

[ht]: https://stackoverflow.com/questions/12444716/how-do-i-set-the-figure-title-and-axes-labels-font-size-in-matplotlib
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Bootstrap Example
- As an example, we'll use the "ToothGrowth" data from the R datasets package.
- We can import this data using statsmodels. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# tooth growth data
file = 'tooth_growth.feather'
if exists(file):
    tg_data = pd.read_feather(file)
else: 
    tooth_growth = sm.datasets.get_rdataset('ToothGrowth')
    #print(tooth_growth.__doc__)
    tg_data = tooth_growth.data
    tg_data.to_feather(file)
#tg_data
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## ToothGrowth Example
- We'll compare the two supplementation methods within each dose
  using a ratio of the mean tooth growth. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mean_ratio = (tg_data
 .groupby(['supp', 'dose']) # orders by supplement
 .mean()
 .groupby(['dose'])
 .agg(lambda x: x[0] / x[1])
 )
mean_ratio
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Pandas sample method
- We can draw bootstrap samples using `.sample()`.
- The re-sampling process should reflect the original design.
- In this case, we condition on the supplementation method and dose and
  re-sample with each group. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
seed = 2021 * 10 * 3

(tg_data
 .groupby(['supp', 'dose'])
 .sample(frac=1, replace=True, random_state=seed)
 )
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Ratio of Means
- Here is a function using NumPy to compute the ratio of means
  across many bootstrap replicates.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
def ratio_of_means(df, n_boot, x, invert=False):
    """
    Compute ratios of means across replicate datasets.

    The column `df[x]` is reshaped into `2 * n_boot` replicates and 
    the means of the first `n_boot` replicates are compared (pairwise) to 
    the means of the second block of `n_boot` using a ratio.  

    Parameters
    ----------
    df : pandas DataFrame
        A pandas DataFrame in which to find the column x.
    n_boot : int
        The number of bootstrap replications.
    x : str
        A numeric column in df.
    invert : bool, optional
        If True (False) use means from the second half of x as denominators
        (numerators). The default is False.

    Returns
    -------
    None.

    """
    x = np.array(df[x])
    x = x.reshape((2, n_boot, int(len(x) / (2 * n_boot))))
    rom = np.mean(x[0, :, :], axis=1) / np.mean(x[1, :, :], axis=1)
    if invert: 
        rom = 1 / rom
    return(pd.DataFrame({'rom': rom}))
```


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Point Estimates
- Here are the point estimates using the function. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
est_ratios = (tg_data
  .groupby('dose')
  .apply(lambda gdf: ratio_of_means(gdf, 1, x='len', invert=True))
  )
est_ratios.reset_index(level=1, drop=True, inplace=True)
est_ratios
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Point Estimates
- To be safe, it's better to explicitly sort here and use `invert` to 
  specify the desired order. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
est_ratios = (tg_data
  .sort_values(['dose', 'supp'])
  .groupby('dose')
  .apply(lambda gdf: ratio_of_means(gdf, 1, x='len', invert=False))
  )
est_ratios.reset_index(level=1, drop=True, inplace=True)
est_ratios
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Bootstrap replicate estimates
- Now we're ready to apply the bootstrap to form replicate estimates.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
n_boot = 1000
# ratios get inverted b/c OJ < VC alphabetically
ratios = (tg_data
  .groupby(['supp', 'dose'])
  .sample(frac=n_boot, replace=True, random_state = seed)
  .groupby('dose')
  .apply(lambda gdf: ratio_of_means(gdf, n_boot, x='len', invert=False))
  )
ratios.groupby('dose').size()
```
<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Bootstrap replicate estimates  
- As a "diagnostic" check, it's a good idea to visualize the estimates. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fig0, ax0 = plt.subplots(nrows=3, sharex=True)
_ = fig0.set_size_inches(8, 8)
fig0.tight_layout()
for i, d in enumerate([0.5, 1.0, 2.0]):
    lab = 'dose = {0:3.1f}'.format(d)
    _ = (ratios
    .query('dose == @d')['rom']
    .plot
    .hist(ax=ax0[i], legend=False, label=lab)
    )
    _ = ax0[i].legend()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Bootstrap replicate estimates  
- Here is an alternate version of the previous figure. 
<!-- #endregion -->
```python
fig1, ax1 = plt.subplots(nrows=1)
_ = fig1.set_size_inches(8, 4)
col = ['darkred', 'darkblue', 'darkgreen']
for i, d in enumerate([0.5, 1.0, 2.0]):
    lab = 'dose = {0:3.1f}'.format(d)
    _ = (ratios.
    query('dose == @d')['rom']
    .plot
    .hist(ax=ax1, color=col[i], alpha=0.5, label=lab)
    )
_ = ax1.legend()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Percentile Method
  - To use the percentile method, we directly estimate the confidence bounds
    using quantiles from the bootstrap distribution.     
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
bse = (ratios
 .groupby(['dose'])
 .quantile((.025,  .975))
 )
bse.index.names = ['dose', 'quantile']
bse = bse.reset_index().pivot(index='dose', columns='quantile', values=['rom'])
bse.columns = ('lwr', 'upr')
erb = est_ratios.join(bse)
erb['Ratio of Means (95% CI)'] = (erb
             .groupby(['dose'])
             .apply(lambda x: 
                    '{0:4.2f} ({1:4.2f}, {2:4.2f})'.format(
                        x['rom'].values[0],
                        x['lwr'].values[0],
                        x['upr'].values[0])
                   )
            )
erb[['Ratio of Means (95% CI)']]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Vertical Lines
  - We can use `plt.axvline()` to illustrate this in our plot.     
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fig0, ax0 = plt.subplots(nrows=3, sharex=True)
_ = fig0.set_size_inches(8, 8)
fig0.tight_layout()
for i, d in enumerate([0.5, 1.0, 2.0]):
    lab = 'dose = {0:3.1f}'.format(d)
    _ = (ratios
    .query('dose == @d')['rom']
    .plot
    .hist(ax=ax0[i], legend=False, label=lab)
    )
    _ = ax0[i].legend()
    ax0[i].axvline(x=erb['lwr'].values[i], color='black')
    ax0[i].axvline(x=erb['upr'].values[i], color='black')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Alternate approach
  - An alternate approach would be to compute the difference on the 
    log scale.
  - Here we compare the ratio of *geometric means* using Welch's method. 
<!-- #endregion -->

```python
# Welch's (unequal variance) t-test on log values
ert = {}
for dose in [0.5, 1, 2]:
    # extract data
    a = tg_data.query('dose == @dose and supp == "OJ"')['len'].values
    b = tg_data.query('dose == @dose and supp == "VC"')['len'].values
    # diff on a log scale
    a, b = np.log(a), np.log(b)
    a_bar, b_bar = np.mean(a), np.mean(b)
    d = a_bar - b_bar
    # std error
    v_a, v_b = np.var(a, ddof=1), np.var(b, ddof=1)
    n_a, n_b = len(a), len(b)
    se = np.sqrt(v_a / n_a + v_b / n_b)
    # degrees of freedom using Welch-Satterthwhaite approximation
    df = (v_a / n_a + v_b / n_b) ** 2 
    df = df / (v_a ** 2 / n_a ** 2 / (n_a - 1) + v_b ** 2 / n_b ** 2 / (n_b - 1))
    tt = t.ppf(.975, df=df)
    lwr, upr = d - tt * se, d + tt * se
    d, lwr, upr = np.exp(d), np.exp(lwr), np.exp(upr)
    ci = '{0:4.2f} ({1:4.2f}, {2:4.2f})'.format(d, lwr, upr)
    ert.update({dose: ci})

welch = pd.Series(ert)
erb['Ratio of Geometric Means (95% CI)'] = welch
erb.iloc[:, 3:5]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## SciPy Bootstrap
  - SciPy stats also has a [bootstrap][spb] method.
  - It takes a function to compute the *statistic* (estimator)
    and requires an axis argument. 
  - The confidence interval is reported in an attribute of that name.
[spb]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html
<!-- #endregion -->


```python slideshow={"slide_type": "code"}
rng = np.random.default_rng(10 + 7 + 2021)
erb_scipy = {}
for dose in [0.5, 1, 2]:
    # extract data
    a = tg_data.query('dose == @dose and supp == "OJ"')['len'].values
    b = tg_data.query('dose == @dose and supp == "VC"')['len'].values
    res = bootstrap(
        (a, b),
        lambda a, b, axis: np.mean(a, axis=axis) / np.mean(b, axis=axis),
        method='percentile',
        axis=0,
        random_state=rng
    )
    lwr, upr = res.confidence_interval
    ci = '{0:4.2f} ({1:4.2f}, {2:4.2f})'.format(np.mean(a) / np.mean(b), lwr, upr)
    erb_scipy.update({dose: ci})
erb['Ratio of Means (95% CI-Scipy)'] = pd.Series(erb_scipy)
erb.iloc[:, [3, 5]]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Permutation testing
  - Where the bootstrap uses resampling to build up an estimate of
    the *sampling distribution*.
  - For null hypothesis testing, we need the distribution of our statistic
    under a *null distribution*. 
  - For a null hypothesis of no association or no difference, this can often
    be accomplished using a permutation test. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Permutation testing
  - If we have $n$ total samples from 2 groups of size $k, \ell$, then there are 
    are $m_c = {n \choose k}$ possible group assignments. 
  - Note that there are actually $m_p = n!$ permutations, but they are not all 
    unique in terms of group assignment.  
  - How many possible groupings are there if we have $g$ groups of size 
    $k_1, \dots, k_g$?  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Permutation testing
  - When $m_c$ is small all possible group assignments can be considered. 
  - Let $\kappa_i$ denote the $i^{th}$ combination and $\bar \theta(X)$ be the 
    statistic of interest. 
  - Then, the permutation p-value for a two-sided test is:
  
$$
 p = \frac{1}{m_c} \sum_{i=1}^{m_c}
  1[~|\bar \theta(X)|~ \le ~|\bar\theta(\kappa_i(X))|~].
$$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Permutation testing  
  - More commonly, when $m_c$ is large we approximate the previous sum
    using a large but tractable number of random permutations.
  - If we sample $N$ permutations $\{\tilde \pi_i(X)]\}_{i=1}^N$ we can form
    a Monte Carlo approximation:

$$
\hat p = \frac{1}{N} \sum_{i=1}^N 
 1[~|\bar \theta(X)|~ \le ~|\bar\theta(\tilde\pi_i(X))|~].
$$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Permutation testing  
  - The estimate, $\hat p$, follows a Binomial distribution.
  - Use to estimate the Monte Carlo error in our estimate.
  - Particularly important if our estimate is near a decision boundary, 
    e.g. $\alpha = 0.05$. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Permutation testing p-value 
 - Because the identity permutation $\pi(X) = X$, has
   $|\bar \theta(X)| \le |\bar\theta(\pi(X))|$ it is conventional to add one 
   to  both the numerator and denominator of the p-value estimate:

$$
\hat p = \frac{1}{N+1} \left(1 + \sum_{i=1}^N 1[~|\bar \theta(X)|~
 \le ~|\bar\theta(\tilde\pi_i(X))|~]\right).
$$
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## ToothGrowth Example
- Let $\mu_S(d)$ be the population mean length for supplement $S$ at dose $d$.
- Let's test the following hypotheses for each dose at level $0.05 / 3$:

$$
H_0: \frac{\mu_{OJ}(d)}{\mu_{VC}(d)} = 1,~ 
H_1: \frac{\mu_{OJ}(d)}{\mu_{VC}(d)} \ne 1
$$

<!-- #endregion -->

```python slideshow={"slide_type": "code"}
def perm_rom(a, b, n_perm=1000, alternative='two-sided', rng=None):
    """
    Compute a permutation test p-value for the null that $\mu_a / \mu_b = 1$.

    Parameters
    ----------
    a, b - ndarray or convertible to such using np.asarray().
      Sequences of observations from two independent groups.
    n_perm - integer,
      The number of permutations to use in the approximation. 
  
    Returns
    -------
    A float between 0 and 1 estimating the p-value. 
    """
    assert alternative in ['two-sided', 'greater', 'less']
    if rng is None:
        rng = np.random.default_rng()
    elif isinstance(rng, int):
        rng = np.random.default_rng(rng)
    # convert of ndarray if needed
    a, b = np.asarray(a), np.asarray(b)
    # the observed ratio
    obs = np.mean(a) / np.mean(b)
    # length
    n_a = len(a)
    # concatenate 
    ab = np.array([a, b]).reshape((n_a + len(b), ))
    # permutations
    two = 0
    for i in range(n_perm): 
        rng.shuffle(ab)
        mean_a, mean_b = np.mean(ab[0:n_a]), np.mean(ab[n_a:])
        if max(mean_a, mean_b) / min(mean_a, mean_b) >= obs:
            two += 1
    # construct p-value
    p = (1 + two) / (n_perm + 1)
    return(p)

assert 0 < perm_rom([2] * 7 + [1.9] * 3, [1.9] * 6 + [2] * 4, rng=None) < 1
assert 0 < perm_rom([2] * 7 + [1.9] * 3, [1.9] * 6 + [2] * 4, rng=42) < 1
```
<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## ToothGrowth Example
- We can apply the function to each dose. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
erb['Permutation p-value'] = (tg_data
     .groupby(['dose'])
     .apply(lambda gdf: perm_rom(
         gdf.query('supp == "OJ"')['len'].values, 
         gdf.query('supp == "VC"')['len'].values,
         n_perm=1000,
         rng=rng),
           )
 ).transform(lambda x: np.round(x, 3))

erb.iloc[:, 3:8]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Takeaways - Bootstrap
 - The bootstrap is a widely used method for constructing confidence interval
   estimates by resampling data with replacement. 
 - The *percentile* method uses sample quantiles from the bootstrap 
   distribution to estimate confidence bounds. 
 - More generally, the bootstrap can be used to estimate quantities related to
   an estimator's sampling distribution.
 - The bootstrap estimates the *sampling distribution*.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Takeaways - Permutation tests
 - Permutation tests estimate a *null distribution*. 
 - Carry out a permutation test by (e.g.) permuting group labels to construct
   ane estimate of the null distribution for a test-statistic. 
<!-- #endregion -->
