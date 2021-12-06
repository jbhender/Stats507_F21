---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Code Tips </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tips for Better Code
*Stats 507, Fall 2021*

James Henderson, PhD  
September 23, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
- [Tip 1](#/slide-2-0)
- [Tip 2](#/slide-3-0)
- [Tip 3](#/slide-4-0)
- [Tip 4](#/slide-5-0)
- [Takeaways](#/slide-6-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tip 1
- Don't do more than you have to.
- <p class='fragment'> 
  Example: Looping over pairs of n items.
  </p>
- <p class='fragment'> 
  Don't use $n^2$ comparisons when you only need $n \choose 2$. 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 1
- Don't do more than you have to.
- Example: Looping over pairs of n items.
- Don't use $n^2$ comparisons when you only need $n \choose 2$. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# worse
phi = (1 + np.sqrt(5)) / 2
psi = (1 - np.sqrt(5)) / 2
x = np.zeros((3, 3))
for i in range(3):
    for j in range(3):
        if i < j:
            x[i, j] = phi ** i - psi ** j
        elif i > j:
            x[i, j] = phi ** j - psi ** i
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 1
- Don't do more than you have to.
- Example: Looping over pairs of n items.
- Don't use $n^{2}$ comparisons when you only need $n \choose 2$. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# better
phi = (1 + np.sqrt(5)) / 2
psi = (1 - np.sqrt(5)) / 2
x = np.zeros((3, 3))
for i in range(3):
    for j in range(i + 1, 3):
        x[i, j] = x[j, i] = phi ** i - psi ** j
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tip 2
- Iterate over indices only when necessary, else iterate over values. 
- <p class='fragment'> 
  Example: Finding the maximum. 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 2
- Iterate over indices only when necessary, else iterate over values. 
- Example: Finding the maximum. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# worse
n = 1000
x = list(np.random.uniform(size=n))
m = x[0]
for i in range(len(x)):
    if x[i] > m:
        m = x[i]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 2
- Iterate over indices only when necessary, else iterate over values. 
- Example: Finding the maximum. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# better
m = x[0]
for v in x:
    if v > m:
        m = v
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tip 3
- Limit use of intermediate variables in simple calculations.
- <p class='fragment'> 
  <em>Do</em> use intermediate variables to add clarity to complex calculations.
</p>
- <p class='fragment'> 
  Example: Computing z-scores. 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 3
- Limit use of intermediate variables in simple calculations.
- *Do* use intermediate variables to add clarity to complex calculations.
- Example: Computing z-scores. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# worse
x = np.random.uniform(size=n)
xbar = np.mean(x)
sd = np.std(x)
num = x - xbar
z = num / sd
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 3
- Limit use of intermediate variables in simple calculations.
- *Do* use intermediate variables to add clarity for complex calculations.
- Example: Computing z-scores. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# better
z = (x - np.mean(x)) / np.std(x)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tip 4
- Don't use two names when one will do. 
- <p class='fragment'> 
  <em>Do</em> pick meaningful, but concise variable names. 
  </p>
- <p class='fragment'>
  Example: Fibonacci function. 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 4
- Don't use two names when one will do. 
- *Do* pick meaningful, but concise variable names. 
- Example: Fibonacci function. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# worse
def fib_for(n, first_fib_number=0, second_fib_number=1):
    """
    Compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ directly by iterating using a for loop.

    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$. 
    first_fib_number, second_fib_number : int, optional.
        Values of $F_0$ and $F_n$ to initalize the sequence with. 

    Returns
    -------
    The Fibonacci number $F_n$ for the sequence beginning with the specified
    inputs. 

    """
    a = first_fib_number
    b = second_fib_number

    if n == 0:
        return(a)
    elif n == 1:
        return(b)
    else:
        for i in range(n - 1):
            a, b = b, a + b
        return(b)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tip 4
- Don't use two names when one will do. 
- *Do* pick meaningful, but concise variable names. 
- Example: Fibonacci function. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
# better
def fib_for(n, f0=0, f1=1):
    """
    Compute the Fibonacci number $F_n$, when $F_0 = a$ and $F_1 = b$.

    This function computes $F_n$ directly by iterating using a for loop.

    Parameters
    ----------
    n : int
        The desired Fibonacci number $F_n$. 
    f0, f1 : int, optional.
        Values to initalize the sequence $F_0$ = `f0`, $F_1$ = `f1`. 

    Returns
    -------
    The Fibonacci number $F_n$ for the sequence beginning with `f0` and `f1`. 

    """
    if n == 0:
        return(a)
    elif n == 1:
        return(b)
    else:
        for i in range(n - 1):
            a, b = b, a + b
        return(b)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- Don't do more than you have to.
- Iterate over indices only when necessary, otherwise iterate over values. 
- Limit use of intermediate variables in simple caclulations.
- Do use intermediate variables to make complex calculations clearer.
- Don't use two names when one will do.
<!-- #endregion -->
