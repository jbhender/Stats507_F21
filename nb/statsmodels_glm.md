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
    autolaunch: false
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Statsmodels (GLM)</a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## statsmodels
*Stats 507, Fall 2021*

James Henderson, PhD  
October 14, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
  - [Generalized Linear Models](#/slide-2-0)
  - [Logistic regression](#/slide-3-0)
  - [Logistic Example](#/slide-4-0)
  - [Poisson Regression](#/slide-5-0)
  - [Offsets & Exposures](#/slide-6-0)
  - [Poisson Example](#/slide-7-0)
  - [Takeaways](#/slide-8-0)

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Imports
 - Here are the import we'll use in the examples.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# imports 
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from os.path import exists
from scipy.stats import norm, t, chi2, logistic
```
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Figures
 - Let's use `pylab` to control the appearance of figures. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## GLM
 - As the name implies, [generalized linear models][glm] _generalize_ the 
   linear model through the use of a _link_ function relating the expected or 
   mean outcome to a _linear predictor_. 

[glm]: https://en.wikipedia.org/wiki/Generalized_linear_model.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## GLM  
 - A GLM relating a dependent variable $Y$ to independent variables
   $X$ and coefficients $\beta$ has the form:

$$
h(E[Y| X]) = X\beta.
$$

  - $h(\cdot)$ is called the _link function_.
  - The matrix product $X\beta$ is known as the _linear predictor_.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## GLM  
  - We often make use of the inverse of $h(\cdot)$ denoted $g(\cdot)$.
  - An equivalent specification is:

$$
E[Y | X] = g(X\beta).
$$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## OLS as GLM
- Ordinary linear regression is a GLM with the _identity link_ 
  $h(x) = g(x) = x$,

$$
E[Y | X] = X\beta.
$$

- $Y | X \sim N(X\beta, \sigma^2)$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Common GLMs
- Binary response: logistic or probit regression,
- Count-valued response: (quasi-)Poisson or Negative Binomial regression,
- Real-valued, positive response: Gamma regression.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Logistic Regression
  - Logistic regression for a binary response treats $Y | X$ 
    as Binomial($g(X\beta)$).
  - Logistic regression uses the _logit link_
    $h(x) = \log(x/(1-x))$
  - This gives the model: 

  $$
  \log \frac{ P(Y = 1 | X) }{P(Y = 0|X)} = X\beta, \quad \textrm{or} \quad
  E[Y | X] = \frac{e^{X\beta}}{1 + e^{X\beta}},
  $$
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Logistic Regression Example
  > Use the 2015 RECS data to examine 
  > features associated with homes that have finished basements.

  - We'll look at only homes *with* basements. 
  - We'll pretend the data are iid and ignore the weights for teaching
    purposes. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Download Data
  - Read the data locally or from the remote URL. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# raw data files
stem = 'https://www.eia.gov/consumption/residential/data/'
recs15_file = stem + '2015/csv/recs2015_public_v4.csv'
recs15_local = 'recs2015_public_v4.csv'

if exists(recs15_local):
    recs15 = pd.read_csv(recs15_local)
else:
    recs15 = pd.read_csv(recs15_file)
    recs15.to_csv(recs15_local)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Clean the Data
  - Limit to what we need, label categorical variables
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# columns 
cols = {
    'DOEID': 'id',
    'REGIONC': 'region',
    'TYPEHUQ': 'home_type',
    'UATYP10': 'urban',
    'BASEFIN': 'finished_basement'
}
dat0 = recs15[cols.keys()].copy()
dat0.rename(columns=cols, inplace=True)

# category labels
cat_vars = {
    'region': {1:'Northeast', 2: 'Midwest', 3: 'South', 4: 'West'},
    'home_type': {
        1: 'Mobile Home',
        2: 'Single-Family Detached',
        3: 'Single-Family Attached',
        4: 'Apartment in Building with 2 - 4 Units',
        5: 'Apartment in Building with 5+ Units'
    },
    'urban': {'U': 'urban', 'C': 'urban cluster', 'R': 'rural'}
}

for c in cat_vars.keys():
    dat0[c] = dat0[c].replace(cat_vars[c])
    dat0[c] = pd.Categorical(dat0[c])

# response variable
dep_vars =  {'finished_basement': {1: 1, 0: 0, -2: np.nan}}
for c in dep_vars.keys():
    dat0[c] = dat0[c].replace(dep_vars[c])

dat0.head()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Examine cell sizes
  - Categorical grouping includes unseen levels.
  - Only single-family homes have non-missing basement variable. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
(dat0
 #.dropna()
 .groupby(
   ['region', 'home_type', 'urban', 'finished_basement'],
   #['region', 'home_type', 'urban'],
   as_index=False
  )
 .size()
 #.query('size > 0')
)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Model 0
  - Let's start by comparing home types. 
  - Need to drop unused levels or design X (`exog`) will be less than 
    full-rank. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# cases for this analysis
dat0 = dat0.dropna()
dat0['home_type'] = dat0['home_type'].cat.remove_unused_categories()

# initial model
mod0 = smf.logit('finished_basement ~ home_type', data=dat0)
#mod0.exog
res0 = mod0.fit(disp=True)
res0.summary()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Odds Ratio
  - In logistic regression, exponential transforms of the coefficients 
    give *odds ratios* (OR). 
  - Here is the OR comparing single-family attached and detached homes. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
odds_ratio = np.exp(-1 * res0.params[1])
ci = np.exp(-1 * res0.conf_int().iloc[1, ]).values
'{0:4.2f} ({1:4.2f}, {2:4.2f})'.format(odds_ratio, ci[1], ci[0])
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Model 1
  - Adding region to the model. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod1 = smf.logit('finished_basement ~ region + home_type', data=dat0)
res1 = mod1.fit()
res1.summary()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Model 1
  - Adding an interaction between region and home type to the model. 
  - How many additional parameters will this have? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod2 = smf.logit('finished_basement ~ region*home_type', data=dat0)
res2 = mod2.fit()
res2.summary()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Model Comparison
  - First, we compare the three models using AIC.
  - Then, we carry our a likelihood ratio test comparing the models with 
    and without the interaction. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print([np.round(r.aic, 1) for r in (res0, res1, res2)])

# LRT
delta = 2 * (mod2.loglike(res2.params) - mod1.loglike(res1.params))
df = mod2.df_model - mod1.df_model
p = 1 - chi2.cdf(delta, df=df)
'$Chi^2$ = {0:4.2f}, df = {1:1g}, p = {2:4.2f}'.format(delta, df, p)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Predictions
  - Let's compute predictions for each unique region and home type.
  - Then we'll compute standard errors.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# unique values to predict
region_home = (dat0
 #.dropna()
 .groupby(
   ['region', 'home_type'],
   as_index=False
  )
 .size()
)
modx = smf.ols('size ~ region + home_type', data=region_home)
x = modx.exog

# predictions
region_home['est'] = mod1.predict(params=res1.params, exog=modx.exog)

# confidence bounds
b = res1.params.values
est = np.dot(x, b)
v = res1.cov_params()
se = np.sqrt(np.diag(np.dot(np.dot(x, v), x.T)))
z = norm.ppf(0.975)
region_home['lwr'] = logistic.cdf(est - z * se)
region_home['upr'] = logistic.cdf(est + z * se)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Visual
  - Now we can visualize the estimates. 
  - Recall that asymmetric error bars can be drawn using a tuple passed to
    `xerr`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fig0, ax0 = plt.subplots(nrows=1)
colors = ('darkblue', 'magenta')
for i in range(2):
    type = cat_vars['home_type'][(2, 3)[i]]
    df = region_home.query('home_type == @type')
#    ax0.scatter(x=df['est'], y=df['region'], color=colors[i], label=type)
    err = df['est'] - df['lwr'], df['upr'] - df['est']
    ax0.errorbar(
        x=df['est'],
        y=df['region'],
        xerr=err,
        color=colors[i],
        capsize=6,
        fmt="s",
        label=type,
        alpha=0.5
    )
ax0.legend(loc='upper left')
ax0.set_xlim((0, 1))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Poisson Regression
  - Poisson regression with a _log link_ $h(x) = \log(x)$ is often used
    for a count-valued response 
  
  $$
  \log E[Y | X] = X\beta, \qquad \textrm{or} \qquad E[Y | X] = e^{X\beta}.
  $$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Mean Variance Relationship
  - As with logistic regression, the variance in Poisson regression is 
    determined by the mean.
     + Quasi-Poisson introduces a dispersion parameter,
     + Negative-binomial regression has a dispersion parameter controlling
       how the variance changed with the mean. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Offsets and Exposures
 - An *offset* is a term in a regression model (linear predictor) with
   parameter fixed to 1.
 - The term *exposure* is often used for an offset that has been log-scaled.
 - Common to use an *exposure* to model count-valued responses as rates. 
 
 $$
  \log \frac{E[Y | X]}{N} = X\beta \iff \log E[Y | X] = X\beta + \log N.
 $$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Poisson Regression Example
  - Let's identify a count-valued variable by searching for variables 
    that start with 'N'.
  - Find an appropriate offset or exposure such as the number of rooms. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
recs15.columns[[c[0] == 'N' for c in recs15.columns]] #NUMCFAN
recs15.columns[[c[0] == 'T' for c in recs15.columns]]  #TOTROOMS
recs15[['NUMCFAN', 'TOTROOMS']].min()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Poisson Regression Example
> Is the popularity of ceiling fans similar across regions of the US?
> To answer, we estimate the rate of ceiling fans per room in residences of
> all types for each Census region. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Data Prep
- Select needed columns, give them memorable names. and create
  categorical types where needed. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fan_vars = {'NUMCFAN': 'n_ceil_fans', 'TOTROOMS': 'n_rooms'}
cols2 = cols.copy()
cols2.update(fan_vars)
_ = cols2.pop('BASEFIN')

dat1 = recs15[cols2.keys()].copy()
dat1.rename(columns=cols2, inplace=True)

for c in cat_vars.keys():
    dat1[c] = dat1[c].replace(cat_vars[c])
    dat1[c] = pd.Categorical(dat1[c])
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Model
- The log number of rooms is used as an offset.
- Using number of rooms as an exposure is equivalent. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fan_mod0 = smf.poisson(
  'n_ceil_fans ~ region',
  exposure=dat1['n_rooms'],
  data=dat1
)
fan_res0 = fan_mod0.fit()
fan_res0.summary()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Predicted Rates
- We can use contrasts to estimate predicted rates of ceiling fans per
  room.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# design matrix for predictions
x_new = np.array([[1, 0, 0, 0], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]])

# predicted rates
y_hat = fan_mod0.predict(params=fan_res0.params, exog=x_new, linear=False)
#?fan_mod0.predict

# key values
b = fan_res0.params.values
v = fan_res0.cov_params()
lp = np.dot(x_new, b)
y_hat = np.exp(lp)

# confidence bounds / margins of error 
se = np.sqrt(np.diag(np.dot(np.dot(x_new, v), x_new.T)))
z = norm.ppf(.975)
lwr, upr = np.exp(lp - z * se), np.exp(lp + z * se)
fans_per_room = pd.DataFrame({'est': y_hat, 'moe': z * se})
fans_per_room['region'] = ('MW', 'NE', 'S', 'W')
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Visualize Rates
- And then visualized predicted rates of ceiling fans per room.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
ax = (
    fans_per_room
    .sort_values('est')
    .plot
    .scatter(x='est', y='region', xerr='moe')
)
_ = ax.set_xlabel('Average Ceiling Fans per Room')
```


<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- Generalized linear models greatly the types of response variables suitable
  for regression. 
- The conditional distribution $Y | X$ can be a different member of the 
  exponential family than Gaussian.
- The *conditional mean* $E[Y|X]$ and *linear predictor* $X\beta$ are related
  through a *link* function and its inverse. 
- The formula API imported as `smf` gives us top-level functions for key 
  regression extensions, including common GLMs. 
<!-- #endregion -->
