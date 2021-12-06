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
    header: <a href="#/slide-0-0"> <h3> Statsmodels </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## statsmodels
*Stats 507, Fall 2021*

James Henderson, PhD  
October 12, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
  - [statsmodels](#/slide-2-0)
  - [regression](#/slide-3-0)
  - [OLS](#/slide-4-0)
  - [Example](#/slide-6-0)
  - [Formulas](#/slide-7-0)
  - [Interactions](#/slide-9-0)
  - [Contrasts](#/slide-13-0)
  - [Takeaways](#/slide-14-0)


<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## statsmodels

> statsmodels is a Python module that provides classes and functions for the
> estimation of many different statistical models, as well as for conducting
> statistical tests, and statistical data exploration.
>
>   <cite>--[statsmodels][sm]</cite>

[sm]: https://www.statsmodels.org/stable/index.html

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## statsmodels
  - For general use, the canonical way to import statsmodels 
    is to import the `api` submodule with the handle `sm`.
  - You will usually want to import the formula API as well. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# imports 
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from os.path import exists
from scipy.stats import t
sm.__version__
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Regression
  - We will focus on using statsmodels for regression problems:
     + linear models using ordinary least squares,
     + generalized linear models.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Regression
  - A regression problem is one in which our focus is on the conditional
    mean of a *dependent* or *endogenous* variable ($Y$) ...
  -  ... given some set of *independent* or *exogenous* variables (X).
  - [endog, exog][enex]
  - This has the form:
  $$
    \mathbb{E}[Y|X = x] = f(x; \beta). 
  $$

[enex]: https://www.statsmodels.org/stable/endog_exog.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Linear Regression
  - In linear regression of *ordinary least squares (OLS)* $f(x; \beta)$ is
    linear in $\beta$ and $Y|X$ is (usually) assumed to be Gaussian with
    covariance $\Sigma = \sigma^2I_{p \times p}$. 

$$
\mathbb{E}[Y|X = x] = x\beta = \sum_{j=1}^{p} x_j \times \beta_j,
\qquad Y | X \sim N(X\beta, \sigma^2). 
$$

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Design Matrix
  - The design matrix $X$ forms a *basis* for the conditional mean and is
    determined by are IVs. 
  - We assume $X \in \mathbb{R}^{n \times p}$ where $n$ is the number of 
    samples (rows) and $p$ the dimension of the basis (columns). 
  - A formula interface as provided by statsmodels (using [patsy][patsy]) 
    allows for a concise, flexible way to construct $X$ from a data frame. 

  [patsy]: https://patsy.readthedocs.io/en/latest/

<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Example - ToothGrowth
  - Let's revisit the ToothGrowth data from the 
   [Resampling Methods][rm] notes. 
  
  [rm]: https://jbhender.github.io/Stats507/F21/slides/resampling.slides.html#/
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

(tg_data
 .groupby(['dose', 'supp'])
 .apply(lambda gdf: gdf.iloc[0:2, :])
)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - endog, exog
  - To begin, let's compare supplementation methods within each dose 
    separately. 
  - To be concrete, we'll start with the dose of 0.5 mg/day of 
    Vitamin C. 
  - Here, we create the outcome and design matrices directly. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tg_05 = tg_data.query('dose == 0.5')
Y = tg_05['len']
X = pd.get_dummies(tg_05['supp'])['OJ']
X = sm.add_constant(X) 
(Y, X)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - OLS
  - Now we can set up the model object using `sm.OLS()` ...
  - and then call its fit model to estimate the parameters. 
  - The `summary()` method prints key information.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod0_05 = sm.OLS(Y, X)
res0_05 = mod0_05.fit()
res0_05.summary()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - OLS Attributes
  - The results object `res0_05` contains much of the summary information 
    in attributes (properties).
  - Here we explore those properties while reviewing the relationships in 
    the coefficient table. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(type(res0_05))
print((res0_05.rsquared_adj, res0_05.aic))
(res0_05.params, res0_05.tvalues)
#res0_05.  # use tab complete to see methods
?res0_05.conf_int
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - Coefficient table
- Let's review the coefficient table from the summary results
  and construct it using attributes and methods from the results
  object. 
<!-- #endregion -->

```python
b = res0_05.params                     # estimated parameters
v = res0_05.cov_params()               # variance-covariance
se = np.sqrt(np.diag(v))               # std errors
t_stats = res0_05.params / se          # t statistics
assert all(t_stats == res0_05.tvalues) # same as stored in object     

df = res0_05.df_resid                  # degrees of freedom
p = 2 * (1 - t.cdf(t_stats, df=df))    # p-values
assert all(np.round(p, 6) == np.round(res0_05.pvalues, 6))

tt = t.ppf(.975, df=df)                # multiplier
lwr, upr = b - tt * se, b + tt * se    # CI bounds
ci = res0_05.conf_int()
ci['lwr'], ci['upr'] = lwr, upr
ci

```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - OLS Methods
  - The results object `res0_05` also has a number of useful [methods][olsrm].
  - On the previous slides, we used the methods `.summary()`, 
    `.cov_params()` and `.conf_int()` methods.
  - You can use the `.save()` and `sm.load()` function to store results on
    disk (as pickle).

  [olsrm]: https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html#statsmodels.regression.linear_model.RegressionResults
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
file_name = 'res0_05.pickle'
# notebook needs to be trusted
res0_05.save(file_name)
del res0_05
res0_05 = sm.load(file_name)
res0_05.summary2()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example - Diagnostics
  - Let's use the `.predict()` method and then create some plots. 
  - We'll also use the `.add_gridspec()` [method][gs] of our figure object.

  [gs]: https://matplotlib.org/stable/tutorials/intermediate/gridspec.html
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
y_hat, r = res0_05.predict(), res0_05.resid
b0, b1 = res0_05.params
col = [('darkgreen', 'orange')[x] for x in X['OJ'].values]

fig0 = plt.figure(tight_layout=True)
gs = fig0.add_gridspec(2, 2)

f0_ax0 = fig0.add_subplot(gs[0, 0])
_ = f0_ax0.set_title('Observed ~ Predicted')
_ = f0_ax0.scatter(x=y_hat, y=Y, color=col)

f0_ax1 = fig0.add_subplot(gs[0, 1])
_ = f0_ax1.set_title('Residual ~ Predicted')
_ = f0_ax1.scatter(x=y_hat, y=r, color=col)

f0_ax2 = fig0.add_subplot(gs[1, :])
f0_ax2.set_title('QQ Plot')
_ = sm.qqplot(ax=f0_ax2, data=r, line='s')

```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example 
- We can compare the ratio of geometric means by regressing
  the log outcome on supplement type.
- This is almost identical to our t-test analysis from the re-sampling notes
  except we use a pooled estimate of the (residual) variance. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tg_data['log_len'] = tg_data[['len']].transform(np.log)
tg_data['OJ'] = pd.get_dummies(tg_data['supp'])['OJ']
doses = [0.5, 1.0, 2.0]
cis = []
for dose in doses:
    # subset dose
    dat = tg_data.query('dose == @dose')
    
    # fit OLS model
    Y, X = dat['log_len'], sm.add_constant(dat['OJ'])
    m = sm.OLS(Y, X)
    res = m.fit()
    ci = res.conf_int()
    
    # format confidence interval
    ci.columns = ('lwr', 'upr')
    ci['est'] = res.params
    ci.index.name = 'term'
    ci = ci.transform(np.exp)
    ci['CI'] = (
        ci.groupby('term').apply(lambda gdf: 
                         '{0:4.2f} ({1:4.2f}, {2:4.2f})'.format(
                             gdf['est'].values[0],
                             gdf['lwr'].values[0], 
                             gdf['upr'].values[0]
                         )
                        )
    )
    cis.append(ci.loc['OJ', 'CI'])
pd.DataFrame({'dose': doses, 'Ratio of Means (95% CI)': cis})
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Formula Method
- Formulas are a convenient way to construct the design matrix $X$
  from a dataset. 
- Formulas are not only convenient, but also concise and expressive, allowing
  us to focus on the modeling and iterate quickly w/o being distracted by 
  set up. 
- In a formula string, a tilde `~` separates DV(s) from the IVs. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod1 = sm.OLS.from_formula('log_len ~ OJ + dose', data=tg_data)
res1 = mod1.fit()
res1.summary2()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Design Inspection
- If you're ever unsure about how a formula is interpreted by statsmodels,
  take a look at (select) rows of the design matrix.
- The model object has attributes `endog` and `exog` and `*_names`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
X = mod1.exog
print(mod1.exog_names)
X
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Formula API
- The formula API was imported as `smf`. 
- This allows us to call the previous model and others more concisely. 
- Use `smf.ols()` with a formula when fitting linear regression models. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# smf.
mod1 = smf.ols('log_len ~ OJ + dose', data=tg_data)
res1 = mod1.fit()
res1.summary2()
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Interactions
- *Interaction* terms in the design matrix are formed by multiplying values
   from two (or more) variables together. 
- Here we specify an interaction between the indicator `OJ` and `dose` 
  treated as a continuous variable. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod2 = sm.OLS.from_formula('log_len ~ OJ:dose', data=tg_data)
res2 = mod2.fit()
res2.summary2()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Interaction Inspection
- What to you expect `X` to look like below. How many zeros will it
  have? 
- Note also how the interaction is named.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
X = mod2.exog
print(mod2.exog_names)
X
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Main Effects & Interactions
- We rarely use interactions without also including the associated *main*
  effects for the variables that make up the interaction. 
- `a + b + a:b` can be concisely written as `a*b`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
mod3 = smf.ols('log_len ~ OJ*dose', data=tg_data)
res3 = mod3.fit()
res3.summary2()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Interaction Inspection
- How many columns do you expect `X` to have? 
- What are their names? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
#mod3 = smf.ols('log_len ~ OJ*dose', data=tg_data)
X = mod3.exog
print(mod3.exog_names)
X
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Categorical Interactions
- Let's run an analysis with the same *mean structure* as our dose-by-dose
  analysis. 
- *Mean-structure* means the models have the same predictions or fitted values,
  but not the same variance structure. 
- We can let each supplement and dose combination have its own mean by making
  *dose* categorical and interacting this with `supp` (or `OJ`).
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tg_data['dose_cat'] = pd.Categorical(tg_data['dose'])
mod4 = smf.ols('log_len ~ OJ*dose_cat', data=tg_data)
res4 = mod4.fit()
res4.summary2()
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Interaction Inspection
- How many columns do you expect `X` to have? 
- What are their names? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
#mod4 = smf.ols('log_len ~ OJ*dose_cat', data=tg_data)
X = mod4.exog
print(mod4.exog_names)
X
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## AIC
- The Akaike Information Criterion (AIC) is one way ato compare competing
  models fit to the same data.
- There is a trade-off between model fit and model complexity -2 times 
  the log-likelihood (aka the *deviance*) plus 2 times the number
  of parameters (columns in X). 
- The log-likelihood is a method of the model object.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(np.round(-2 * mod4.loglike(res4.params) + 2 * len(res4.params), 2))
[np.round(r.aic, 1) for r in [res1, res2, res3, res4]]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Contrasts
- Linear combinations of regression coefficients are known as *contrasts*.
- We often express contrasts using matrix notation -- each row of `L` below
  specifies a contrast. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
b = res4.params
v = res4.cov_params()
L = np.zeros((3, len(b)))
L[0, 3] = 1      # OJ
L[1, (3, 4)] = 1 # OJ + OJ:dose_cat[T.1.0]
L[2, (3, 5)] = 1 # OJ + OJ:dose_cat[T.2.0]
est = np.exp(np.dot(L, b))
se = np.sqrt(np.diag(np.dot(np.dot(L, v), L.T)))
tt = t.ppf(.975, df=res4.df_resid)
lwr, upr = est - tt * se, est + tt * se
np.round(np.array([est, lwr, upr]).T, 2)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Contrasts
- Contrasts can also be estimated using the `.t_test()` method of the
  results object. 
- In models with interactions, we need contrasts to estimate the means for
  non-reference groups.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
contrasts = res4.t_test(L)
print(np.round(np.exp(contrasts.effect), 2))
contrasts
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Contrasts
- Setting up the contrasts matrix `L` takes care.
- The `.t_test()` method also accepts a string with contrasts specified using
  the parameter (variable) names. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
contrasts = res4.t_test(
    'OJ = 0, OJ + OJ:dose_cat[T.1.0] = 0, OJ + OJ:dose_cat[T.2.0] = 0'
)
#contrasts
#contrasts.summary()
est_ci4 = np.zeros((3, 3))
est_ci4[:, 0] = np.exp(contrasts.effect)
est_ci4[:, 1:3] = np.exp(contrasts.conf_int())
np.round(est_ci4, 2)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- Regression is among the most important techniques in the data science 
  toolkit.
- OLS and many related (statistical) regression models can be fit using
  statsmodels.
- The formula API allows us for flexible and concise specification of the 
  design matrix. 
- In a formula, `:` indicates an interaction and `a*b = a + b + a:b`.
- Estimate contrasts using the `.t_test()` method. 
<!-- #endregion -->
