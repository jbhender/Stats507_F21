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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - DataFrames </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pandas DataFrames
*Stats 507, Fall 2021*

James Henderson, PhD  
September 21 & 23, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
- [DataFrame Operations](#/slide-2-0)
- [Index Objects](#/slide-3-0)
- [Transformations](#/slide-6-0)
- [Hierarchical Indices](#/slide-7-0)
- [Merging](#/slide-9-0)
- [Pivoting](#/slide-10-0)
- [Takewaways](#/slide-11-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## DataFrame Operations
- Essential data frame operations to learn:  
  + <p class='fragment highlight-green'>
    filtering to create subsets of cases (rows),
    </p>
  + creating new variables (columns) from existing ones, 
  + merging two datasets (joins),
  + pivoting between wider and longer formats,
  + <p class='fragment highlight-red'> performing aggregations by group. </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Indices
- DataFrame indices hold axis labels and associated metadata. 
- DataFrames can have both row and column indices. 
- The `.columns` attribute is an `Index` object. 
- Indices organize a DataFrame and facilitate many methods. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
import pandas as pd
print(pd.__version__)
df = pd.DataFrame(
    {
        "a": range(5),
        "b": [("red", "black")[i % 2] for i in range(5)],
        "c": [("x", "y", "z")[i % 3] for i in range(5)]
    }
)
df.columns
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Indices
- Create a standalone `Index` using `pd.Index()`. 
- `Index` objects are immutable. 
- Move a column to an index using `.set_index()`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
idx = pd.Index(list("stats"))
df.index = idx 
df
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Indices
- Create a standalone `Index` using `pd.Index()`. 
- `Index` objects are immutable. 
- Move a column to an index using `.set_index()`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df1 = df.iloc[[3, 2, 1], ]
df_alt = df1.set_index('a')
df_alt

```
<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Indices
- Select by index value using the `loc` indexer.   
- Some methods (e.g. `.reindex()`) won't work with duplicates index values. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
try:
    df.reindex(['a', 't', 's'])
except:
    print('Duplicate label error.')

df.loc[['a', 't', 's'], 'a':'b']
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Indices
- Create a Series or DataFrame from an index using `.to_series()` or
  `.to_frame()` 
- (Better) create a column called `index` using `.reset_index()`. 
- Use to convert indices to data.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df['idx'] = df.index.to_frame()
df.reset_index(inplace=True)
df
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Transformations
- Use `.map()` to transform a Series element wise.
- Use `.applymap()` for element-wise transformation of DataFrames.
- Use`.transform()` for vectorized transformations. 
- Use `.replace()` to map existing values to new values.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df['a_sq'] = df['a'].map(lambda x: x ** 2)
df['a2'] = df['a'].transform(lambda x: np.power(x, 2))
df['a3'] = df[['a']].applymap(lambda x: x ** 3)
df['c'].replace('z', 'w', inplace=True)
df
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Strings
- Vectorized string operations (that skip missing values) can be
  accessed through a Series's `str` attribute.
- You can index this attribute or call its methods. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df['b'] = df['b'].str.title()
df['b'].str[:2]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Hierarchical Indices
- An Index can have more than one *level* allowing you to create
  hierarchical structure. 
- These use the `MultiIndex` class and associated constructor. 
- Here I add a level to the column index labeling numeric columns.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
num = [('object', 'numeric')[v != np.dtype('O')] for v in df.dtypes.values]
df.columns = [num, df.columns]
print(df.columns)
df.loc[:, 'numeric']
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Hierarchical Indices
- Use a tuple to specify multiple levels of a MultiIndex.
- Construct all tuples using `.to_flat_index()`. 
- Use a list to retain all levels. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print([df.loc[:, 'numeric'].columns, df.loc[:, ['numeric']].columns])
print(df.columns.to_flat_index())
df.loc[:, ('object', 'b')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Example
- In this example, we center all the numeric columns using `.transform()`.
- We then drop a level from the column Index. 
- <p class='fragment'> What happens if we don't index with a list? </p>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df.loc[:, ['numeric']] = (df.loc[:, ['numeric']].
                             transform(lambda x: x - np.mean(x)))
df.columns = df.columns.droplevel()
df 
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Merging
- Create a *join* by *merging* two DataFrames using `pd.merge()`.  
- Use `on` for matching rows, defaults to shared column names.
- Use `how` to determine join type: `left`, `inner`, `outer` , `right`.
- Prefer `left` joins when in doubt. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
df0 = df.loc[:, 'a':'c'].reset_index()
df1 = df.loc[:, 'a':'c'].reset_index().query('b == "Red"')
df0['old'] = 0
df1['new'] = 1
pd.merge(df0, df1, on=['index', 'b', 'c'], how='left', indicator=True)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Merging
- Shared column names not used in `on` are renamed with suffixes. 
- Indices are discarded when joining on columns. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
pd.merge(df0, df1, on=['b', 'c'], how='right', suffixes=('_0', '_1'))
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Merging
- The row Index can be used as the merge keys for left and/or right DataFrames.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
pd.merge(
    df0.set_index('index'), 
    df1.set_index('index'),
    left_index=True,
    right_index=True
)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Merging
- The row Index can be used as the merge keys for left and/or right DataFrames.
- The `.join()` method lets (left) joins be written more compactly. 
- <p class='fragment'> Can pass a list of DataFrames to join. </p>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
(df0.
 set_index(['b', 'c']).
 join(df1.set_index(['b', 'c']), rsuffix='_1')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pivoting
- Data often need to be *reshaped* to facilitate analysis or plotting. 
- Using hierarchical indices:
  + make a pandas DataFrame *longer* using `.stack()`,
  + make a pandas DataFrame *wider* using `.unstack()`. 
- Alternately use `pd.melt()` (*longer*) or `pd.pivot()` (*wider*).
- (More to come.)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeways
- DataFrame, Series, Index, or MultiIndex - know what you're working with.
- If indices confuse you, keep them as regular columns. 
- Use DataFrame methods whenever you can. 
<!-- #endregion -->
