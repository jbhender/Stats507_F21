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
    header: <a href='#/slide-0-0'> <h3> Stats 507 - NumPy Fundamentals </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# NumPy Funadmentals
*Stats 507, Fall 2021*

James Henderson, PhD  
September 14, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - <a href='#/slide-2-0'> About NumPy </a>
 - <a href='#/slide-3-0'> `ndarray`'s and `dtype`'s </a>
 - <a href='#/slide-7-0'> Vectorization </a>
 - <a href='#/slide-8-0'> Indexing/Slicing </a>
 - <a href='#/slide-10-0'> Broadcasting </a>
 - <a href='#/slide-11-0'> Random number generation </a>
 - <a href='#/slide-14-0'> Takeways </a>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## About
- NumPy is short for "Numerical Python"
- Most scientific modules use NumPy arrays for data exchange.
- NumPy provides *vectorized* mathematical functions ...
- ... and a C API useful for connecting Python to C, C++, and Fortran.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Canonical Import
 - `import numpy as np`
 - Numpy version 1.21
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
print(np.__version__)
x = range(10)
xbar = np.mean(x) # implicit conversion to ndarray 
xbar
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## NumPy's helpful scalars
- Missing values / not a number `np.nan`
- Infinity `np.Inf` or `-np.Inf`
- `np.pi`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Numpy's ndarray object
- The `ndarray` object is a flexible *N*-*d*imensional *array*.
- `ndarray`'s are *atomic* or *homogenous*, containing data of a single type.
- In addition to its primary data, an `ndarray` has attributes / meta-data:
  + `ndim` - the dimensionality,
  + `shape` - a tuple giving the size of each dimension,
  + `dtype` - the data type of the array's values. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = [0, 1, 2]; y = [3, 4, 5]
x_a = np.array(x)
y_a = np.array([x, y])
[(x_a.ndim, y_a.ndim), x_a.shape, y_a.shape, y_a]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Constructors for class ndarray
- `np.array()` converts sequence objects to arrays.
- `np.asarray()` is similar, but creates an alias when passed an `ndarray`.
- There are others: 
  + `np.ones()`, `np.zeros()`, `np.empty()`, `*_like()`,
  + `np.arange()`, `np.identity()`.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
z_x = np.asarray(x)    # x is a list
z_y = np.asarray(y_a)  # y_a is an ndarray
print((z_x is x, z_y is y_a))
z_y.shape = (3, 2)
y_a
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## More Constructors
- `np.arange()` - like built-in `range()` but returns an array; `[start, stop)`.
- `np.linspace()` - `num` evenly spaced values in `[start, stop]`. 
- Many more, skim and learn as needed. 

<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(np.linspace(0, 2 * np.pi, 5) / np.pi)
np.linspace([0, 0], [3, 6], 3)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## NumPy data types
- The `dtype` attribute tells NumPy what type to interpret the primary data
  (values) of the array as.
- Primary data is contiguous in memory, so must be *homogeneous* with a single
  `dtype`.
- Common `dtype`'s are:
  + `int8`, `int16`, `int32` and `int64`, `uint8`-`uint64`,
  + `float16`-`float128`, `complex64`-`complex256`,
  + `bool`, `object`, `string_`, `unicode_`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
(z_x.dtype, z_y.dtype)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Casting NumPy data types
- Convert an `ndarray` to another type using the `.astype()` method.
- This is known as *casting* between types.
- Binary operators (among others) operating on arrays of different but
  *compatible* types will implictly cast to the more complex type. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print((z_x.dtype, z_y.dtype))
z_f = z_x.astype(np.float64)
[(z_y[:, 1] + z_f).dtype, (z_f + z_y[:, 1]).dtype]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Casting NumPy data types
- Casting using `.astype()` always creates a copy.
- Types have shorthand strings used with `np.dtype()`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
z_f2 = z_f.astype('d') # 'd' is shorthand for np.float64
print(z_f2 is z_f)
if z_f.dtype == np.dtype('float64'):
    pass
else:
    z_f = z_f.astype(np.float64) 
if z_f.dtype != np.float64:
    z_f = z_f.astype(np.float64)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Vectorization
- A function or operator written to operate on an entire sequence (or vector)
  at once is said to be *vectorized*.  
- Generally this refers to creating functions that encapsulate associated loops.
- In interpreted languages, these loops are usually written in a lower-level,
  compiled, language (often C, C++, or Fortran) for efficiency.  
- This process and concept is referred to as *vectorization*. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Vectorization in NumPy
- *Vectorization* is integral to the appeal, popularity, and efficiency of
   NumPy. 
- For PS1, you've probably already used vectorized `np.mean()`, `np.std()`.
- Binary operators are vectorized for `ndarray` objects. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = np.arange(9).reshape(3, 3)
y = np.array([-1, 0, 1])
x[:, 0] * y, x[1, :] > y, x * y
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Indexing / Slicing
- In some respects, slicing an `ndarray` is similar to slicing a `list`.
- Higher dimensional indices can be omitted.
- A slice of an `ndarray` is a *view* of the original array referencing
  the original data.   
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
z = np.ones((4, 3))
z1 = z[:, 1].copy()
z2 = z[:, 2]
z1[:] = 0 
z2[:] = 7 # 7 is broadcast to the entire slice
z
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Boolean indexing
+ An `ndarray` can be indexed using the `bool` type, often created from
  the array itself.
+ Note that `and`  and `or` are not *vectorized*, use `np.logical_and()` or
  `np.logical_or()` instead.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(z > 1)
z[z > 1]
col_sums = np.sum(z, axis=0)
col_sums = np.sum(z, axis=0)
z[:, np.logical_and(col_sums > 4, col_sums < 30)]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Broadcasting in NumPy
- *Broadcasting* refers to rules for applying element-wise functions to
  arrays with disimilar dimensions.
- Broadcasting makes array operations more efficient by saving on memory
  allocation and indexing. 
- NumPy uses a fairly strict form of broadcasting that allows scalar
  by array operations and mismatches in the number of dimensions.   

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Broadcasting in NumPy
- Read the rules [here][nbr].
- After pre-pending with 1's to make `.ndims` agree, dimensions must match
  or be 1. 
   
[nbr]: numpy.org/doc/stable/reference/ufuncs.html#broadcasting
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
np.array([-1, 2]) * np.ones((2, 2, 2))
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Exercise
- What are the shape and sum of `z` below? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
z = np.ones((2, 3, 2))
x = np.array([i % 3 - 1 for i in range(6)])
x = x.reshape(2, 3)

try:
    z = x * z
except:
    x = x.reshape(3, 2)
    try: 
        z = x * z
    except:
        pass
    
x = x.reshape(1, 1, 3, 2)
try:
    z = x * z
except:
    z[:] = 0
    
[z.shape, np.sum(z), x.shape]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Random Numbers
 - NumPy's `random` API provides a random number generator and routines to 
   sample from a large number of [distributions][rg]. 
 - `np.random.choice()` can be used to sample a sequence object. 
 [rg]: https://numpy.org/doc/stable/reference/random/generator.html#distributions
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(np.random.uniform(0, 1, 3))
print(np.random.normal(63.5, 5.55, 2))
np.random.choice(range(3), 4)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Reproducible Results
 - To make results that rely on pseudo-random number generation 
   exactly reproducible, set a seed for the random number generator.
 - The way this is done was recently updated in NumPy v1.21.
 - Create a [Generator][gen] instance using `np.random.default_rng()`.
  
 [gen]: https://numpy.org/doc/stable/reference/random/generator.html
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
rng = np.random.default_rng(seed=42)
rng.uniform()
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Shuffle vs Permutation
- The `.shuffle()` method permutes an array in-place.
- The `.permutation()` method creates a copy.
- Both shuffle data, ignoring shape.
- The `.permuted()` method shuffles along an axis, use `out` to reassign
  in-place.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
rng = np.random.default_rng(91421)
a = np.arange(4)
rng.shuffle(a)
b = rng.permutation(a)
[a, b, b is a]
b.shape = (2, 2)
c = b
_ = rng.permuted(b, axis=0, out=b)
[c is b, c, b]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- NumPy is the backbone of scientific Python. 
- NumPy offers vectorized and optimized implementations of many mathematical
  functions, a flexible array class with expressive slicing, helfpul scalars,
  and much more. 
- NumPy uses a strict form of broadcasting.  
- NumPy's random API can be used to generate pseudo-random numbers from 
  almost any distribution. 
- NumPy is a big topic, learn a little at a time. 
<!-- #endregion -->
