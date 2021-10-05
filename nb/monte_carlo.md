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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Monte Carlo Studies </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Monte Carlo Studies
*Stats 507, Fall 2021*

James Henderson, PhD  
October 5, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Monte Carlo](#/slide-2-0)
 - [Example - Estimating pi](#/slide-3-0)
 - [LLN & CLT](#/slide-4-0)
 - [Precision](#/slide-7-0)
 - [Takeaways](#/slide-8-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Monte Carlo - *Why* 
 - In statistics and data science we are often interested in computing 
   expectations (means) of various types of random outcomes.
 - When analytic expectations are unavailable or cumbersome to compute, 
   it can be useful to obtain *Monte Carlo* approximations.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Monte Carlo - *What* 
 - We form Monte Carlo estimates by simulating (from) a random process and
   then directly averaging the values of interest. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Example
 - In this example, we'll from a Monte Carlo estimate of $\pi.$ 
 - Our estimate is based on the fact that the unit circle has area $\pi.$
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
from scipy.stats import norm
n_mc = 1000
rng = np.random.default_rng(10 * 5 / 2021)
xy = rng.random.uniform(2 * n_mc)
xy = xy.reshape((2, n_mc))
d = np.power(xy[0, :], 2) + np.power(xy[1, :], 2)
p_hat = np.mean(d < 1)
pi_hat = 4 * p_hat
pi_hat
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Law of Large Numbers
 - Monte Carlo estimation works because the sample average is generally a
   good estimate of the corresponding expectation 
   $\bar{\theta}_n \to_p \theta $.
$$
{\bar{\theta}}_{n} := \sum_{i=1}^n X_i / n  \to_p \theta := E[X].
$$
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Central Limit Theorem
 - Assume our data are:
   + *independent and identically distributed* (iid),
   + from a distribution with finite variance.
 - Then, the rate of convergence of a sample average to its population 
   counterpart is characterized by the *central limit theorem* (CLT):
$$
 \sqrt{n}(\bar{\theta}_n - \theta) \to_{d} N(0,\sigma^2)
$$
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Central Limit Theorem
 - On the previous slide, $\sigma^2$ is the variance of
   the underlying distribution from which X is drawn.

 - Estimate the variance of a Monte Carlo estimate to construct confidence
   intervals around your estimates.

 - Choose the number of Monte Carlo replicates to attain the desired precision.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
se = 4 * np.sqrt(p_hat * (1 - p_hat) / n_mc)

se2 = 4 * np.sqrt( np.var(d) / n_mc )
z = norm.ppf(.975)
lwr, upr = pi_hat - z * se, pi_hat + z * se
'{0:5.3f} ({1:4.2f}, {2:4.2f})'.format(pi_hat, lwr, upr)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Confidence Level
- We chose $z = \Phi^{-1}(0.975)$ on the previous slide to attain a 95% 
  *confidence level*. 
- This means that we expect the population parameter ($\pi$) to be in our
  (random) interval 95% of the time.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
lwr < np.pi < upr # Expect this to be True ~95% of the time with z = 1.96
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Desired Precision
- Suppose we need to estimate $\pi$ to within $\pm 0.001$ with 99% confidence.
- To determine the number of Monte Carlo replicates we should use to attain
  the desired margin of error, solve the inequality, 
  
$$
\Phi^{-1}(0.995) 4 \sqrt{ \frac{\pi}{4} \left(1 - \frac{\pi}{4}\right) / n }  
 < 0.001.
$$
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
z = norm.ppf(.995)
n_min =  (1000 * z * 4 * np.sqrt(np.pi / 4 * (1 - np.pi / 4))) ** 2
n_min
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example
- Here is our earlier example with 18 million Monte Carlo replicates.
- This is feasible because we are using vectorized operations.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
n_mc = int(1.8e7)
xy = rng.uniform(size=2 * n_mc).reshape((2, n_mc))
d = np.power(xy[0, :], 2) + np.power(xy[1, :], 2)
eps = 4 * np.mean(d < 1) - np.pi
(eps, np.abs(eps) < 0.001)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- *Monte Carlo* estimates are statistical estimates of population parameters
  using "data" simulated from a (pseudo-)random process.
- Use vectorized operations for efficient *Monte Carlo* estimation. 
- Use the CLT or the Normal approximation to the Binomial to estimate the 
  variance of a Monte Carlo estimate.
- Choose the number of Monte Carlo replicates based on the required/desired
  precision.  

<!-- #endregion -->
