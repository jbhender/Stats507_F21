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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Pandas, Part 0 </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pandas, Part 0
*Stats 507, Fall 2021*

James Henderson, PhD  
September 16, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
- [About](#/slide-2-0)
- [I/O](#/slide-5-0)
- [The `series` class](#/slide-6-0)
- [The `DataFrame` class](#/slide-7-0)
- [Selecting rows and columns](#/slide-9-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pandas
- [Pandas](https://pandas.pydata.org/) is a Python library that facilitates:
   + working with rectangular data frames, 
   + reading and writing data,
   + aggregation by group,
   + much else.
- Pandas is a core library for data analysts working in Python.   
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Canonical Import
 - `import pandas as pd`
 - In the reading, Wes McKinney suggests: 
   `from pandas import Series, DataFrame`
 - I won't (usually) do this, but you can if wanted on problem sets. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
import pandas as pd
pd.__version__
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tidy Rectangular Data
 - Rectangular datasets are a staple of data analysis.
 - A dataset is "tidy" if each row is an observation and each column is
   a variable.
 - The distinction between "observation" and "variable" can depend on 
   context - work to develop your intuition on this front.
 - Don't store "data" in column names.
 - pandas [cheat sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## I/O for Rectangular Data
 - The easiest way to read rectangular data, delimited and otherwise,
    into Python is using a pandas `pd.read_*()` function.
 - `pd.read_csv()` accepts a filename, including remote URLs.
 -  Write data to file using a pandas object's `.to_*()` methods.   
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Series
- A pandas `Series` is a fixed-length, ordered dictionary. 
- `Series` are closely related to the `DataFrame` class. 
- Series are indexed, with the index (keys) mapping to values. 
- Use the `pd.Series()` constructor with a `dict`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
import pandas as pd
nyc_air = pd.Series(
    {'LGA': 'East Elmhurst', 'JFK': 'Jamaica', 'EWR': 'Newark'})
nyc_air.index.name = 'airport'
nyc_air.name = 'city'
nyc_air 
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## DataFrames
- The pandas `DataFrame` class is the primary way of representing 
  heterogeneous, rectangular data in Python.  
- A `DataFrame` can be thought of as an ordered dictionary of `Series` 
  (columns) with a shared index (row names). 
- *Rectangular* means all the columns (Series) have the same length.  
- We will use DataFrames heavily in this class going forward. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## The DataFrame Constructor
- A common way to construct a `DataFrame` directly from data is
  to pass a `dict` of equal length lists, NumPy arrays, or `Series`,
  to `pd.DataFrame()`.
- Use the `columns` argument to order the columns.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
wiki = pd.Series({
    'LGA': 'https://en.wikipedia.org/wiki/LaGuardia_Airport',
    'EWR': 'https://en.wikipedia.org/wiki/Newark_Liberty_International_Airport',
    'JFK': 'https://en.wikipedia.org/wiki/John_F._Kennedy_International_Airport'
})
df = pd.DataFrame({'city': nyc_air, 'wiki': wiki})
df
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Select Columns ... 
- by name using `[]` with a string (caution) or list of strings,
- by position using the `.iloc[:, 0:2]` indexer,
- by name using the `.loc[:, ["col1", "col2"]` indexer.
- Columns with valid Python names an be accessed as attributes, e.g. `df.column`
  (but don't). 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
city = df['city']
city2 = df['city'].copy()
df_city = df[['city']]
[(city is df['city'], df_city is df[['city']]), (type(city), type(df_city))]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Select Columns ... 
- by name using `[]` with a string (caution) or list of strings,
- by position using the `.iloc[:, 0:2]` indexer,
- by name using the `.loc[:, ["col1", "col2"]` indexer.
- Columns with valid Python names an be accessed as attributes, e.g. `df.column`
  (but don't). 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df.loc[["JFK", "LGA"], "city"] = "NYC"  # always returns a view
df.city
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Create/Modify Columns
- Assign to a selected column to modify (or create) it. 
- To delete a column use the `del` keyword or (better) the 
  `.drop(columns='col', inplace=True)` method. 
- Style "rule" - prefer (exposed) methods when available. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
dat = pd.DataFrame({'a': range(5), 'b': np.linspace(0, 5, 5)})
dat['c'] = dat['d'] = dat['a'] + dat['b']
del dat['c']
dat.drop(columns='a', inplace=True)
dat
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Selecting rows
 - Select rows by position using `.iloc[0, :]` or by index using 
   `.loc["a", :]`. 
 - More on this topic after discussing the `Index` class in more detail. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
dat.iloc[0, :] = -1
print(dat.index)
dat.loc[0:5:2, :]  # takes a slice object b/c uses RangeIndex()
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Filtering
- Observations satisfying some condition can be selected through
  Boolean indexing or (better) using the `.query()` method. 
- The primary argument to `.query()` is a string containing a Boolean 
  expression involving column names. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
b = dat[dat['b'] > 0]
q = dat.query('b > 0 and d < 8')
[b, q]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
- Pandas `DataFrames` are used to represent tidy, rectangular data. 
- Think of `DataFrames` as a collection of `Series` of the same length and
  sharing an index. 
- Pay attention to whether you are: 
  + getting a `Series` or a (new) `DataFrame`
  + a view (alias) or a copy.
- Prefer methods when available. 
- I recommend keeping a Pandas [cheat sheet][cs] close at hand.
- More on Pandas and DataFrame methods in the next few lectures. 

[cs]: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
<!-- #endregion -->
