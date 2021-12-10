# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

#
# ## Provided by:
#
#  __Ahmad Shirazi__<br>
#  __Shirazi@umich.edu__
#  
#
# ## Topic:
#  
# Using <font color=red>glob module</font> to create a data frame from multiple files, row wise:

# +
import pandas as pd
from glob import glob


# - We can read each dataframe from its own CSV file, combine them together and delet the original dataframes. <br>
# - This will need a lot of code and will be memory and time consuming.<br>
# - A better solution is to use the built in glob module.<br>
# - Lets make example dataframes in the next cell.<br>

# +
# making 3 dataframes as inputs for our example
data_age1 = pd.DataFrame({'Name':['Tom', 'Nick', 'Krish', 'Jack'],
        'Age':[17, 31, 28, 42]})

data_age2 = pd.DataFrame({'Name':['Kenn', 'Adam', 'Joe', 'Alex'],
        'Age':[20, 21, 19, 18]})

data_age3 = pd.DataFrame({'Name':['Martin', 'Jenifer', 'Roy', 'Mike'],
        'Age':[51, 30, 38, 25]})

# Saving dataframes as CSV files to be used as inputs for next example
data_age1.to_csv('data_age1.csv', index=False)
data_age2.to_csv('data_age2.csv', index=False)
data_age3.to_csv('data_age3.csv', index=False)


# - We pass a patern to the glob (including wildcard characters)
# - It will return the name of all files that match that pattern in the data subdirectory.
# - We can then use a generator expression to read each file and pass the results to the concat function.
# - It will concatenate the rows for us to a single dataframe.
# -

students_age_files = glob('data_age*.csv')
students_age_files

pd.concat((pd.read_csv(file) for file in students_age_files), ignore_index=True)


# ## Concatenate 
# *Dingyu Wang*
#
# wdingyu@umich.edu

# ## Concatenate 
# + Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# + Combine two Series.

import pandas as pd

s1 = pd.Series(['a', 'b', 'c'])
s2 = pd.Series(['d', 'e', 'f'])
pd.concat([s1, s2])

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.

df1 = pd.DataFrame([['a', 1], ['b', 2], ['c', 3]],
                   columns=['letter', 'number'])
df2 = pd.DataFrame([['d', 4], ['e', 5], ['f', 6]],
                   columns=['letter', 'number'])
pd.concat([df1, df2])

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.
# * Combine DataFrame objects with overlapping columns and return only those
# that are shared by passing inner to the join keyword argument
# (default outer).

df3 = pd.DataFrame([['a', 1, 'Mary'], ['b', 2, 'John'], ['c', 3, 'James']],
                   columns=['letter', 'number', 'name'])
pd.concat([df1, df3])
pd.concat([df1, df3], join='inner')

# ## Concatenate 
# * Concatenate pandas objects along a particular axis with optional set logic
# along the other axes.
# * Combine two Series.
# * Combine two DataFrame objects with identical columns.
# * Combine DataFrame objects with overlapping columns and return only those
# that are shared by passing in `join=inner`(default outer).
# * Combine DataFrame objects horizontally along the x axis by passing in
# `axis=1`(default 0).

df4 = pd.DataFrame([['Tom', 24], ['Jerry', 18], ['James', 22]],
                   columns=['name', 'age'])
pd.concat([df1, df4])
pd.concat([df1, df4], axis=1)

# # Sparse Data Structures - falarcon@umich.edu
#
# Felipe Alarcon Pena

# `pandas` offers a way to speed up not only calculations in the typical `sparse` meaning, i.e. , `DataFrames` with 0's, but also for particular values or `NaN's`.
#
#
# Let's first start showing the effect it has on discarding `NaN's` or a particular values and compare it with other methods. 
#
# The goal of using `sparse` Data Structures is to allocate memory efficiently in large data sets and also speed-up possible operations between `sparse` Data Structures. `Sparse Data Structure` saved values and locations instead of the whole Dataframe. 
#

import pandas as pd
import numpy as np

# +
## Creating toy data.

array_nans = np.random.randn(500, 10000)

# Switching some values to NaN's to produce a sparse structure.
array_nans[10:499,1:9900] = np.nan

dense_df = pd.DataFrame(array_nans)
sparse_df = dense_df.astype(pd.SparseDtype("float", np.nan))

print(" Density of sparse DataFrame: "+str(sparse_df.sparse.density))
# -

# ## Efficiency in storing Sparse DataStructures
#
# `Sparse DataStructures` are more efficient in allocating memory for large datasets with lots of NaN's or information that it is not of interest. The toy data has some sparsity $\sim$ 50%, but real data or matrices could have densities of the orden of $\sim$0.1 % or less.

# +
## Let's compare the storing times for different methods and the same datastructure  being sparse or not.

print('Dense data structure : {:0.3f} bytes'.format(dense_df.memory_usage().sum() / 1e3))
print('Sparse data structure : {:0.3f} bytes'.format(sparse_df.memory_usage().sum() / 1e3))
# -

# Even though the sparse allocate memory better, thy take slightly longer to be created. Nevertheless, we will prove that when there are heavy operations being undertaken in large sparse data structures, the speed-up is worth it, and the allocation of memory as well.

# %timeit  df_2 = pd.DataFrame(array_nans)

# %timeit  sparse_df = pd.DataFrame(array_nans).astype(pd.SparseDtype("float", np.nan))

# ## Speed-up of calculations in Sparse DataStructures and comparison with scipy.
#
# Finally we compare the time it takes to operate on `Dense DataStructures` and `Sparse DataStructures`. Operating directly on `Sparse DataStructures` is not really efficient because `pandas` converts them to `Dense DataStructures` first. Nevertheless the `scipy` package has methods that take advantage of the psarsity of matrices to speed-up those processes.

# +
## scipy also offers methods for sparse arrays, although in the full with 0's meaning,
from scipy.sparse import csr_matrix

rnd_array = np.zeros((10000,500))
rnd_array[200:223,13:26] = np.random.randn(23,13)
sparse_rnd_array = csr_matrix(rnd_array)
sparse_matrix_df = csr_matrix(sparse_df)
# -

# %timeit sparse_matrix_df.dot(sparse_rnd_array)

# %timeit dense_df.dot(rnd_array)

# As we can see `Sparse` methods are specially useful to manage data with repeated values or just values we are not interested in. It can also be used to operate on them using `scipy` and its methods for `sparse` arrays, which could be much faster that standard multiplications. It is important to notice that it is only faster when the sparsity is significant, usually less than 1%.


# ## Topics in Pandas
# **Stats 507, Fall 2021** 

# ## Contents
# + [Pandas Table Visualization](#Pandas-Table-Visualization)
# + [Sorting in Python Pandas](#Sorting-in-Python-Pandas)
# + [Python Classes and Objects](#Python-Classes-and-Objects)

# ## Pandas Table Visualization
# **Author:** Cheng Chun, Chien  
# **Email:**　jimchien@umich.edu  
# [PS6](https://jbhender.github.io/Stats507/F21/ps/ps6.html)

# ## Introduction
# - The slide shows visualization of tabular data using the ***Styler*** class
# - The ***Styler*** creates an HTML table and leverages CSS styling language to control parameters including colors, fonts, borders, background, etc.
# - Following contents will be introduced.
#     1. Formatting Values
#     2. Table Styles
#     3. Bulitin Styles

# ## Formatting Values
# - Styler can distinguish the ***display*** and ***actual*** value
# - To control the display value, use the *.format()* method to manipulate this according to a format spec string or a callable that takes a single value and returns a string.
# - Functions of *.format()*
#     - *precision*: formatting floats
#     - *decimal / thousands*: support other locales
#     - *na_rep*: display missing data
#     - *escape*: displaying safe-HTML or safe-LaTeX

# ## Table Styles
# - Recommend to be used for broad styling, such as entire rows or columns at a time.
# - 3 primary methods of adding custom CSS styles
#     - *.set_table_styles()*: control broader areas of the table with specified internal CSS. Cannot be exported to Excel.
#     - *.set_td_classes()*: link external CSS classes to data cells. Cannot be exported to Excel.
#     - *.apply() and .applymap()*: add direct internal CSS to specific data cells. Can export to Excel.
# - Also used to control features applying to the whole table by generic hover functionality, *:hover*.
# - List of dicts is the format to pass styles to .set_table_styles().

# ## Builtin Styles
# - *.highlight_null*: identifying missing data.
# - *.highlight_min / .highlight_max*: identifying extremeties in data.
# - *.background_gradient*: highlighting cells based or their, or other, values on a numeric scale.
# - *.text_gradient*: highlighting text based on their, or other, values on a numeric scale.
# - *.bar*: displaying mini-charts within cell backgrounds.

import numpy as np
import pandas as pd
# Example of table bar chart
np.random.seed(0)
df = pd.DataFrame(np.random.randn(5,4), columns=['A','B','C','D'])
df.style.bar(subset=['A', 'B'], color='#d65f5f')

# ---
# ---
#

# ## Sorting in Python Pandas
# **Author:** Nuona Chen  
# **Email:** nuona@umich.edu 

#  <h3>DataFrame.sort_values()</h3>
#
#
#
#  <h2>DataFrame.sort_values()</h2>
#  <h3>General Form</h3>
#  <li>DataFrame.sort_values(by, axis=0, ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=False, key=None)</li>
#  
#  <h3>What it does</h3>
#  <li>sorts the input DataFrame by values</hi>
#  
#  <h3>Input Parameters</h3>
#   <li>by: name or list of names to sort by</li>
#    <li>axis: 0 -> sort indices, 1 -> sort columns </li>
#    <li>ascending: true -> sort ascending, false -> sort descending</li>
#    <li>inplace: true -> sort in-place </li>
#    <li>kind: sorting algorithm </li>
#    <li>na_position: first -> put NaNs at the beginning, last -> put NaNs at the end</li>
#    <li>ignore_index: true -> label axis as 0, 1,..., n-1</li>
#  
#  <h3>Function Output</h3>
#  <li>The sorted Pandas DataFrame</li>
#  <h4>Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html</h4>

# +
from IPython.core.display import HTML, display
display(HTML('<h2>Example1 - Sort by Columns</h2>'))

data = {"id": [1, 2, 3, 4, 5, 6],
        "gpa": [3.2, 3.7, 3.1, 3.0, 3.7, 3.7],
        "total credit hours": [55, 68, 100, 94, 46, 110],
        "major": ["Statistics", "Anthropology", "Business", "Computer Science", "Business", "Statistics"]}
print("Input DataFrame - ie_data: ")
ie_data = pd.DataFrame(data)
print(ie_data)

display(HTML('<h3>Sort by gpa in an ascending order</h3>'))
display(HTML("<code>ie_data.sort_values(by='gpa', ascending=True)</code>"))

print(ie_data.sort_values(by="gpa", ascending=True))

display(HTML('<h3>Sort by gpa and major in an descending order</h3>'))
display(HTML("<code>ie_data.sort_values(by=['gpa', 'major'], ascending=[False, True])</code>"))

print(ie_data.sort_values(by=["gpa", "major"], ascending=[False, True]))
display(HTML('<p>The order of variables in the by statement is the order of sorting. Major is sorted after gpa is sorted.</p>'))

display(HTML('<h2>Example2 - Sort by Rows</h2>'))

del ie_data["major"]
print("Input DataFrame - ie_data: ")
print(ie_data)
display(HTML('<h3>Sort by the row with index = 4 in an descending order</h3>'))
display(HTML("<code>ie_data.sort_values(by=4, axis=1, ascending=False)</code>"))

ie_data.sort_values(by=4, axis=1, ascending=False)


# -

# ---
# ---
#

# ## Python Classes and Objects
#
# **Name:** Benjamin Osafo Agyare  
# **UM email:** bagyare@umich.edu  
#

# ## Overview
#   - [Python classes](#Python-classes)
#   - [Creating a Class data](#Creating-a-Class)
#   - [The __init__() Function](#The-__init__()-Function)
#   - [Object Methods and the self operator](#Object-Methods-and-the-self-operator)
#   - [Modifying and Deleting objects](#Modifying-and-Deleting-objects)

# ## Python classes
# - Python is an object oriented programming language.
# - Almost everything in Python is an object, with its properties and methods.
# - A Class is like an object constructor, or a "blueprint" for creating objects.

# ## Python classes
# - Some points on Python class:
#   + Classes are created by keyword class.
#   + Attributes are the variables that belong to a class.
#   + Attributes are always public and can be accessed using the dot (.) operator. Eg.: Myclass.Myattribute

# ## Creating a Class
# - To create a class in python, use the reserved keyword `class`
#
# ### Example
# - Here is an example of creating a class named Student, with properties name, school and year:

class Student:
    school = "U of Michigan"
    year = "freshman"


# ## The __init__() Function
#
# - To make better meaning of classes we need the built-in `__init__()` function.
# - The `__init__()` is used function to assign values to object properties, or other operations that are necessary to do when the object is being created.
# - All classes have this, which is always executed when the class is being initiated.

# +
class Student:
    def __init__(self, name, school, year):
        self.name = name
        self.school = school
        self.year = year

person1 = Student("Ben", "University of Michigan", "freshman")
print(person1.name)
print(person1.school)
print(person1.year)


# -

# ## Object Methods and the self operator
# - Objects in python can also have methods which are functions that belong to the object

# ## Object Methods and the self operator
# - The self parameter
#   + The self parameter `self` in the example above references the current state of the class.
#   + It can be used to access the variables that belong to the class.
#   + You can call it whatever you like but has to be the first parameter of any function in a class

# ## Example

# +
class Student:
    def __init__(myself, name, school, year):
        myself.name = name
        myself.school = school
        myself.year = year

    def getAttr(person):
        print("Hi, I'm " + person.name + " and a "
              + person.year + " at " + person.school)


person2 = Student("Ben", "University of Michigan", "freshman")
person2.getAttr()
# -

# ## Modifying and Deleting objects
# - You can modify object properties
# - It is also possible to delete properties objects using the `del` keyword and same can be used to delete the object itself

# ## Example

# +
## Modify object properties
person2.year = "senior"

## Delete properties of objects
del person2.name

## Delete object
del person2
# -

# ## References:
# - [https://www.w3schools.com/python](https://www.w3schools.com/python)
# - [https://www.geeksforgeeks.org/python-classes-and-objects/](https://www.geeksforgeeks.org/python-classes-and-objects/)
# - [https://www.tutorialspoint.com/python3](https://www.tutorialspoint.com/python3)

# ---
# ---


import pandas as pd
import numpy as np
import random

# **Stan Brouwers** *brouwers@umich.edu*

# # Pandas, write to LaTeX
#
# - Pandas function.
# - Can write dataframe to LaTeX table.
# - Helpful when writing reports.
# - Easy to call.
#

# # A first example
#
# - Multiple ways to call the function.
# - Selecting certain parts of a dataframe also possible.
# - Column names and indices are used to label rows and columns.

# Generate some data.
data = pd.DataFrame([[random.randint(1,10) for columns in range(5)] for rows in range(5)])
print(data.to_latex())

# # Another example
#
# - Table can be written to a file. (buf input)
# - Subset of columns can be chosen.
#     - Using list of column names.

data.to_latex(buf='./test.doc')
# Only printing certain columns
print(data.to_latex(columns=[0, 4]))


# ## Topics in Pandas
# **Stats 507, Fall 2021** 
# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
# + [Duplicate labels](#Duplicate-labels) 
# + [Topic 2 Title](#Topic-2-Title)
#
# # Duplicate labels
#
# **Xinyi Liu**
# **xyiliu@umich.edu**

import numpy as np
import pandas as pd

# * Some methods cannot be applied on the data series which have duplicate labels (such as `.reindex()`, it will cause error!),
# * Error message of using the function above: "cannot reindex from a duplicate axis".

series1 = pd.Series([0, 0, 0], index=["A", "B", "B"])
#series1.reindex(["A", "B", "C"]) 

# * When we slice the unique label, it returns a series,
# * when we slice the duplicate label, it will return a dataframe.

df1 = pd.DataFrame([[1,1,2,3],[1,1,2,3]], columns=["A","A","B","C"])
df1["B"]
df1["A"]

# * Check if the label of the row is unique by apply `index.is_unique ` to the dataframe, will return a boolean, either True or False.
# * Check if the column label is unique by `columns.is_unique`, will return a boolean, either True or False.

df1.index.is_unique
df1.columns.is_unique


# * When we moving forward of the data which have duplicated lables, to keep the data clean, we do not want to keep duplicate labels. 
# * In pandas version 1.2.0 (cannot work in older version), we can make it disallowing duplicate labels as we continue to construct dataframe by `.set_flags(allows_duplicate_labels=False)`
# * This function applies to both row and column labels for a DataFrame.

# +
#df1.set_flags(allows_duplicate_labels=False) 
## the method above cannot work on my end since my panda version is 1.0.5
# -

# Reference: https://pandas.pydata.org/docs/user_guide/duplicates.html

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
# ## Contents
#
# + [Function](Function) 
# + [Topic 2 Title](#Topic-2-Title)
#
# ## Function
# Defining parts of a Function
#
# **Sachie Kakehi**
#
# sachkak@umich.edu

# ## What is a Function
#
#   - A *function* is a block of code which only runs when it is called.
#   - You can pass data, known as *parameters* or *arguments*, into a function.
#   - A function can return data as a result.

# ## Parts of a Function
#
#   - A function is defined using the $def$ keyword
#   - Parameters or arguments are specified after the function name, inside the parentheses.
#   - Within the function, the block of code is defined, often $print$ or $return$ values.

# ## Example
#
#   - The following function multiplies the parameter, x, by 5:
#   - Note : it is good practice to add a docstring explaining what the function does, and what the parameters and returns are. 

def my_function(x):
    """
    The function multiplies the parameter by 5.
    
    Parameters
    ----------
    x : A float or integer.
    
    Returns
    -------
    A float or integer multiplied by 5. 
    """
    return 5 * x
print(my_function(3))

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
# + [Duplicate labels](#Duplicate-labels) 
# + [Topic 2 Title](#Topic-2-Title)
# # Duplicate labels
#
# **Shuyan Li**
# **lishuyan@umich.edu**
#
# Real-world data is always messy. Since index objects are not required to be unique, sometimes we can have duplicate rows or column labels. 
# In this section, we first show how duplicate labels change the behavior of certain operations. Then we will use pandas to detect them if there are any duplicate labels, or to deal with duplicate labels.
#
# - Consequences of duplicate labels
# - Duplicate label detection
# - Deal with duplicate labels

import pandas as pd
import numpy as np

# Generate series with duplicate labels
s1 = pd.Series([0,4,6], index=["A", "B", "B"])

# ## Consequences of duplicate labels
# Some pandas methods (`Series.reindex()` for example) don’t work with duplicate indexes. The output can’t be determined, and so pandas raises.

s1.reindex(["A", "B", "C"])

# Other methods, like indexing, can cause unusual results. Normally indexing with a scalar will reduce dimensionality. Slicing a DataFrame with a scalar will return a Series. Slicing a Series with a scalar will return a scalar. However, with duplicate labels, this isn’t the case.

df1 = pd.DataFrame([[0, 1, 2], [3, 4, 5]], columns=["A", "A", "B"])
df1

# If we slice 'B', we get back a Series.

df1["B"] # This is a series

# But slicing 'A' returns a DataFrame. Since there are two "A" columns.

df1["A"] # This is a dataframe

# This applies to row labels as well.

df2 = pd.DataFrame({"A": [0, 1, 2]}, index=["a", "a", "b"])
df2

df2.loc["b", "A"]  # This is a scalar.

df2.loc["a", "A"]  # This is a Series.

# ## Duplicate Label Detection
# We can check whether an Index (storing the row or column labels) is unique with `Index.is_unique`:

df2.index.is_unique # There are duplicate indexes in df2.

df2.columns.is_unique # Column names of df2 are unique.

# `Index.duplicated()` will return a boolean ndarray indicating whether a label is repeated.

df2.index.duplicated()

# ## Deal with duplicate labels
# - `Index.duplicated()` can be used as a boolean filter to drop duplicate rows.

df2.loc[~df2.index.duplicated(), :]

# - We can use `groupby()` to handle duplicate labels, rather than just dropping the repeats. 
#
# For example, we’ll resolve duplicates by taking the average of all rows with the same label.

df2.groupby(level=0).mean()

# Reference: https://pandas.pydata.org/docs/user_guide/duplicates.html

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   
#
# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Empty cells](#Empty-cells)
# + [Windows Rolling](#Windows-Rolling) 
# + [Data Transformation](#Data-Transformation)


# ## Empty cells
# ---
# **Name: Yan Xu**
#
# Email:yanyanxu@umich.edu

import pandas as pd
import numpy as np
from datetime import datetime
from ps1_solution import ci_prop
import numpy.random as npra
from warnings import warn
import matplotlib.pyplot as plt
from os.path import exists


from scipy import stats
from scipy.stats import chi2_contingency 
from IPython.display import HTML

# Remove rows: remove rows that contain empty cells. Since data sets can be very big, and removing a few rows will not have a big impact on the result.
# Replace Empty Values:insert a new value using fillna() to replace NA.
# Replace Only For a Specified Columns: To only replace empty values for one column, specify the column name for the DataFrame.

#If you want to consider inf and -inf to be “NA” in computations
pd.options.mode.use_inf_as_na = True

df = pd.read_csv('https://www.w3schools.com/python/pandas/dirtydata.csv.txt')
df #The dataframe containing bad data we want to clean

# To make detecting missing values easier (and across different array dtypes), pandas provides the isna() and notna() functions, which are also methods on Series and DataFrame objects

df["Date"][20:25].notna()

new_df = df.dropna()
print(new_df.to_string())#dropna() method returns a new DataFrame, and will not change the original.
#If you want to change the original DataFrame, use the `inplace = True` argument

#insert a new value to replace the empty values
df.fillna(130)
df["Calories"].fillna(130, inplace = True)#only replace empty values for one column


# ### Data in wrong format
#
# In our Data Frame, we have two cells with the wrong format.
# Check out row 22 and 26, the 'Date' column should be a string that represents a date,try to convert all cells in the 'Date' column into dates.

# Method to validate a date string format in Python


date_string = '12-25-2018'
format = "%Y/%m/d"

try:
  datetime.strptime(date_string, format)
  print("This is the correct date string format.")
except ValueError:
  print("This is the incorrect date string format. It should be YYYY/MM/DD")


# This is the incorrect date string format. It should be YYYY/MM/DD

# for row 26,the "date" column is in wrong format
df['Date'] = pd.to_datetime(df['Date'])


# ### Removing Duplicates
#
# Duplicate rows are rows that have been registered more than one time.
# To discover duplicates, we can use the duplicated() method.
# The duplicated() method returns a Boolean values for each row.

print(df[10:15].duplicated())


# To remove duplicates, use the drop_duplicates() method.

df.drop_duplicates(inplace = True)  


# ## Windows Rolling
# ---
# **Name: Junyuan Yang**
#
# **UM email: junyyang@umich.edu**
#
# Return a rolling object allowing summary functions to be applied to windows of length n.
# By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting center=True.
# Each points' weights could be determined by win_type shown in windows function, or evenly weighted as default.

import numpy as np
import pandas as pd
from os.path import exists
import re

rng = np.random.default_rng(9 * 2021 * 28)
n=100
a = rng.binomial(n=1, p=0.5, size=n)
b = 1 - 0.5 * a + rng.normal(size=n)
c = 0.8 * a + rng.normal(size=n) 
df = pd.DataFrame({'a': a, 'b': b, 'c': c})
df['c'].plot()

# - Calculating the mean in centered windows with a window length of 10 and windows type of 'triangular'

df['c'].rolling(10, center=True, win_type='triang').mean().plot()

# - Except existing functions like `sum`, `mean` and `std`, you could also use the self defined funciton by `agg.()`

df['c'].rolling(10).agg(lambda x: max(x)).plot()


# ## Data Transformation 
# ---
# **Name: Tong Wu**
#
# **UM email: wutongg@umich.edu**  
#
# Data transforming technique is important and useful when we prepare the data
# for analysis.  
# - Removing duplicates
# - Replacing values
# - Discretization and binning
# - Detecting and filtering outliers
# - Computing indicator/dummy variables
# ### Removing duplicates
# - Use `duplicated()` method returning a boolean Series to indicate which row
# is duplicated or not.
# - Duplicated rows will be dropped using `drop_duplicates()` when the
# duplicated arrary is `False`.

import pandas as pd
import numpy as np
import scipy.stats as st

data = pd.DataFrame({
    'a': [('red', 'black')[i % 2] for i in range(7)],
    'b': [('x', 'y', 'z')[i % 3] for i in range(7)]
    })
data.duplicated()
data.drop_duplicates()

# - We can specify a subset of data to detect duplicates.

data.drop_duplicates(['a'])

# - Above methods by default keep the first observed duplicated, but we can 
# keep the last occurance and drop the first occurance.

data.drop_duplicates(['a', 'b'], keep='last')

# ### Replacing values
# - General replacing approach
#  + When we find flag values for missing value, we can replace them with NAs.

pd.Series([1., -999., 2., -999., 5., 3.]).replace(-999, np.nan)

# - In a special case, we need to detect missing values and fill in them. 
#  +  Built-in Python `None` value is also treated as `NA`.

data1 = pd.DataFrame(np.random.randn(6,3))
data1.iloc[:3, 1] = np.nan
data1.iloc[:2, 2] = np.nan
data1.iloc[1, 0] = None

# Detect missing values by rows and drop rows with all NAs.
data1.dropna(axis=0, how='all')
# For time seris data, we want to keep rows with obervations.
data1.dropna(thresh=2)

# Fill in missing values.
# - Note that `fillna()` method return a new object by default.
#  + Using `inplace=True` to modify the existing object.
# - `ffill` method propagate last valid observation forward.

data1.fillna(0)
_ = data1.fillna(method='ffill', inplace=True)

# ### Discretization and binning
# This technique is used when we want to analyze continuous data seperated
# into different bins.  
# For example, we have a group of people and the **age** isgrouped into bins.

ages = [20, 17, 25, 27, 21, 23, 37, 31, 61, 45, 41, 88]
# Default it is cut into intervals with left side opened and right side closed
bins = [15, 25, 35, 60, 90]
cats = pd.cut(ages, bins)
# Categorical object
cats
cats.codes
cats.categories
# Bins count
pd.value_counts(cats)

# - Cut without emplicit bin edges.
#  + It will compute equal-length bins using the range of data.

pd.cut(ages, 4, precision=2)

# - Cut data based on sample quantiles
cat2 = pd.qcut(np.random.randn(1000), 4, precision=2)
pd.value_counts(cat2)


# ### Detecting and filtering outliers
# Here is an example with normal distributed data.
data2 = pd.DataFrame(np.random.randn(1000, 4))
data2.describe()

# Find rows which contains absolute value is larger than 3.
data2[(np.abs(data2) > 3).any(1)]
# Cap values outside the interval -3 to 3
data2[(np.abs(data2) > 3)] = np.sign(data2) * 3
data2.describe()

# ### Computing indicator/dummy variables
# We can convert a categorical variable into an indicator matrix. That is if
# a column contains $k$ distinct values, the indicator matrix is derived with
# $k$ colunms with 1s and 0s.

pd.get_dummies(cats)

# ## Problem Set 6: pd_topic_nkernik.py
# **Stats 507, Fall 2021**  
# *Nathaniel Kernik*
# nkernik@umich.edu
# *November, 2021*

# modules: --------------------------------------------------------------------
import numpy as np
import pandas as pd

# 79: -------------------------------------------------------------------------

# ## Question 0 - Topics in Pandas
# Data in/out - Reading multiple files to create a single DataFrame


for i in range(3):
    data = pd.DataFrame(np.random.randn(10, 4))
    data.to_csv("file_{}.csv".format(i))

files = ["file_0.csv", "file_1.csv", "file_2.csv"]
result = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print(result)


# Basic grouping with apply

df = pd.DataFrame(
    {
        "animal": "cat dog cat fish dog cat cat".split(),
        "size": list("SSMMMLL"),
        "weight": [8, 10, 11, 1, 20, 12, 12],
        "adult": [False] * 5 + [True] * 2,
    }
)
print(df)

# List the size of the animals with the highest weight.

df.groupby("animal").apply(lambda subf: subf["size"][subf["weight"].idxmax()])

df = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
)
print(df)

# Using both row labels and value conditionals

df[(df.AAA <= 6) & (df.index.isin([0, 2, 4]))]

df = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]},
    index=["foo", "bar", "boo", "kar"],
)


# Slicing methods
#     positional-oriented
#     label-oriented

print(df.loc["bar":"kar"])
print(df[0:3])
print(df["bar":"kar"])


# Creating new columns using applymap
df = pd.DataFrame({"AAA": [1, 2, 1, 3], "BBB": [1, 1, 2, 2], "CCC": [2, 1, 3, 1]})
print(df)

source_cols = df.columns
new_cols = [str(x) + "_cat" for x in source_cols]
categories = {1: "Alpha", 2: "Beta", 3: "Charlie"}
df[new_cols] = df[source_cols].applymap(categories.get)
print(df)


# ## Problem Set 6: pd_topic_gxchen.py
# **Stats 507, Fall 2021**  
# *Guixian Chen*
# gxchen@umich.edu
# *November, 2021*

# ## Table Styles
# * `pandas.io.formats.style.Styler` helps style a DataFrame or Series (table) according to the data with HTML and CSS.
# * Using `.set_table_styles()` from `pandas.io.formats.style.Styler` to control areas of the table with specified internal CSS.
# * Funtion `.set_table_styles()` can be used to style the entire table, columns, rows or specific HTML selectors.
# * The primary argument to `.set_table_styles()` can be a list of dictionaries with **"selector"** and **"props"** keys, where **"selector"** should be a CSS selector that the style will be applied to, and **props** should be a list of tuples with **(attribute, value)**.

import pandas as pd
import numpy as np

# example 1
df1 = pd.DataFrame(np.random.randn(10, 4),
                  columns=['A', 'B', 'C', 'D'])
df1.style.set_table_styles(
    [{'selector': 'tr:hover',
      'props': [('background-color', 'yellow')]}]
)

# example 2
df = pd.DataFrame([[38.0, 2.0, 18.0, 22.0, 21, np.nan],[19, 439, 6, 452, 226,232]],
                  index=pd.Index(['Tumour (Positive)', 'Non-Tumour (Negative)'], name='Actual Label:'),
                  columns=pd.MultiIndex.from_product([['Decision Tree', 'Regression', 'Random'],
                                                      ['Tumour', 'Non-Tumour']], names=['Model:', 'Predicted:']))
s = df.style.format('{:.0f}').hide_columns([('Random', 'Tumour'), ('Random', 'Non-Tumour')])
cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', '#ffffb3')]
}
index_names = {
    'selector': '.index_name',
    'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
}
headers = {
    'selector': 'th:not(.index_name)',
    'props': 'background-color: #000066; color: white;'
}
s.set_table_styles([cell_hover, index_names, headers])



# -*- coding: utf-8 -*-
# %%

# Wenxiu Liao
# wenxiul@umich.edu

# ### sort_values()
# * The Series.sort_values() method is used to sort a Series by its values.
# * The DataFrame.sort_values() method is used to sort a DataFrame by its column or row values.
#     - The optional by parameter to DataFrame.sort_values() may used to specify one or more columns to use to determine the sorted order.

import numpy as np
import pandas as pd
from os.path import exists
from scipy import stats
from scipy import stats as st
from warnings import warn
from scipy.stats import norm, binom, beta
import matplotlib.pyplot as plt

df1 = pd.DataFrame(
    {"A": [2, 1, 1, 1], "B": [1, 3, 2, 4], "C": [5, 4, 3, 2]}
)
df1.sort_values(by="C")

# The by parameter can take a list of column names, e.g.:

df1.sort_values(by=["A", "B"])

# You can specify the treatment of NA values using the na_position argument:

s = pd.Series(
    ["A", "B", "C", "Aaba", "Baca", np.nan, "CABA", "dog", "cat"],
    dtype="string"
)
s.sort_values(na_position="first")


# !/usr/bin/env python
# coding: utf-8

# ## Topics in Pandas<br>
# **Stats 507, Fall 2021**

# ## Contents<br>
# + [pandas.cut function](#pandas.cut-function)
# + [Sampling in Dataframes](#Sampling-in-Dataframes)
# + [Idioms-if/then](#Idioms-if/then)

# ___<br>
# ## pandas.cut function<br>
# **Name: Krishna Rao**<br>
# <br>
# UM-mail: krishrao@umich.edu

# ## pandas.cut function<br>
# * Use the cut function to segment and sort data values into bins. <br>
# * Useful for going from a continuous variable to a categorical variable. <br>
# * Supports binning into an equal number of bins, or a pre-specified array of bins.<br>
# <br>
# #### NaNs?<br>
# * Any NA values will be NA in the result. <br>
# * Out of bounds values will be NA in the resulting Series or Categorical object.

# ## Examples<br>
# * Notice how the binning start from 0.994 (to accommodate the minimum value) as an open set and closes sharply at 10<br>
# * The default parameter 'right=True' can be changed to not include the rightmost element in the set<br>
# * 'right=False' changes the bins to open on right and closed on left



import pandas as pd
import numpy as np
input_array = np.array([1, 4, 9, 6, 10, 8])
pd.cut(input_array, bins=3)
#pd.cut(input_array, bins=3, right=False)


# + <br>
# Observe how 0 is converted to a NaN as it lies on the open set of the bins<br>
# 1.5 is also converted to NaN as it lies between the sets (0, 1) and (2, 3)

# %%


bins = pd.IntervalIndex.from_tuples([(0, 1), (2, 3), (4, 5)])
#bins = [0, 1, 2, 3, 4, 5]
pd.cut([0, 0.5, 1.5, 2.5, 4.5], bins)
# -


# ## Operations on dataframes<br>
# * pd.cut is a very useful function of creating categorical variables from continous variables<br>
# * 'bins' can be passed as an IntervalIndex for bins results in those categories exactly, or as a list with continous binning.<br>
# * Values not covered by the IntervalIndex or list are set to NaN.<br>
# * 'labels' can be specified to convert the bins to categorical type variables. Default is `None`, returns the bins.

# ## Example 2 - Use in DataFrames<br>
# * While using IntervalIndex on dataframes, 'labels' can be updated with pd.cat.rename_categories() function<br>
# * 'labels' can be assigned as string, numerics or any other caregorical supported types

# +

# %%


df = pd.DataFrame({"series_a": [0, 2, 1, 3, 6, 4, 2, 8, 10],
                   "series_b": [-1, 0.5, 2, 3, 6, 8, 14, 19, 22]})


# %%


bin_a = pd.IntervalIndex.from_tuples([(0, 2), (4, 6), (6, 9)])
label_a = ['0 to 2', '4 to 6', '6 to 9']
df['bins_a'] = pd.cut(df['series_a'], bin_a)
df['label_a'] = df['bins_a'].cat.rename_categories(label_a)


# %%


bin_b = [0, 1, 2, 4, 8, 12, 15, 19]
label_b = [0, 1, 2, 4, 8, 12, 15]
df['bins_b'] = pd.cut(df['series_b'], bin_b)
df['labels_b'] = pd.cut(df['series_b'], bin_b, labels=label_b)


# %%


df
# -


# #### References:<br>
# * https://pandas.pydata.org/docs/reference/api/pandas.cut.html<br>
# * https://stackoverflow.com/questions/55204418/how-to-rename-categories-after-using-pandas-cut-with-intervalindex<br>
# ___

# ___<br>
# ## Sampling in Dataframes<br>
# **Name: Brendan Matthys** <br>
# <br>
# UM-mail: bmatthys@umich.edu

# ## Intro -- df.sample<br>
#

# Given that this class is for an applied statistics major, this is a really applicable topic to be writing about. This takes a dataframe and returns a random sample from that dataframe. Let's start here by just importing a dataframe that we can use for



import pandas as pd
import os
import pickle
import numpy as np


# + <br>
# -----------------------------------------------------------------------------

# %%


filepath =os.path.abspath('')
if not os.path.exists(filepath + "/maygames"):
    nba_url ='https://www.basketball-reference.com/leagues/NBA_2021_games-may.html'
    maygames = pd.read_html(nba_url)[0]
    maygames = maygames.drop(['Unnamed: 6','Unnamed: 7','Notes'], axis = 1)
    maygames = maygames.rename(columns =
                               {
        'PTS':'Away Points',
        'PTS.1':'Home Points'
    })

    #dump the data to reference for later
    pickle.dump(maygames,open(os.path.join(filepath,'maygames'),'wb'))
else:
    maygames = pd.read_pickle('maygames')
    
maygames
# -


# The dataframe we will be working with is all NBA games from the 2020-2021 season played in May. We have 173 games to work with -- a relatively strong sample size.

# Let's start here with taking a sample with the default parameters just to see what the raw function itself actually does:



maygames.sample()


# The default is for this function to return a single value from the dataframe as the sample. Using the right parameters can give you exactly the sample you're looking for, but all parameters of this function are optional.

# ## How many samples?

# The first step to taking a sample from a population of data is to figure out exactly how much data you want to sample. This function has two different ways to specify this -- you can either use the parameters n or frac, but not both.<br>
# <br>
# ### n <br>
#  * This is a parameter that takes in an integer. It represents the numebr of items from the specified axis to return. If neither n or frac aren't specified, we are defaulted with n = 1.<br>
#  <br>
# ### frac<br>
#  * This is a parameter that takes in a float value. That float returns the fraction of data that the sample should be, representative of the whole population. Generally speaking, the frac parameter is usually between 0 and 1, but can be higher if you want a sample larger than the population<br>
#  <br>
# ### Clarification <br>
# It's important to note that if just any number is typed in, the sample function will think that it is taking an input for n.



maygames.sample(n = 5)




maygames.sample(frac = 0.5)




print(len(maygames))
print(len(maygames.sample(frac = 0.5)))


# ## Weights and random_state

# The weights and random_state paramteres really define the way that we are going to sample from our original dataframe. Now that we have the parameter that tells us how many datapoints we want for our sample, it is imperative that we sample the right way. <br>
# <br>
# ### Weights<br>
# <br>
# Weights helps define the probabilities of each item being picked. If the parameter is left untouched, then the default for this is that all datapoints have an equal probability of being chosen. You can choose to specify the weights in a variety of ways. <br>
# <br>
# If a series is used as the parameter, the weights will align itself with the target object via the index.<br>
# <br>
# If a column name is used, the probabilities for being selected will be based on the value of that specific column. If the sum of the values in that column is not equal to 1, the weights of those values will be normalized so that they sum to 1. If values are missing, they will be treated as if they are weighted as 0.



maygames.sample(n = 10, weights = 'Attend.')


# The sample above took in 10 datapoints, and was weighted based on the game attendance, so that the games with more people at them had a higher chance of being picked.

# ### Random_state<br>
# <br>
# Random state is essentially the parameter for the seed we want. This creates a sample that is reproducible if you want it to be. Generally, an integer is inputted for the parameter, but an np.random.RandomState object can be inserted if wanted. The default value for this is None.



sample_1 = maygames.sample(n = 10, weights = 'Attend.', random_state = 1)
sample_1




sample_2 = maygames.sample(n = 10, weights = 'Attend.', random_state = 1)
sample_2




sample_1 == sample_2


# As you can see, the random_state parameter creates a sample that can be reproduced for future uses, which can prove to be incredibly helpful.

# ## Replace and ignore index

# The last few optional parameters we have are replace and ignore index. Both can be advantageous in their own right. <br>
# <br>
# ### Replace<br>
# <br>
# The parameter replace specifies whether we want to be able to sample with or without replacement. It takes in a Boolean as input. If True, then the datapoint has the ability to be chosen again into the sample. If False, the datapoint is removed from the pool of possible points to be chosen.



maygames.sample(
    n = 10,
    weights = 'Attend.',
    random_state = 1,
    replace = True)


# ### Ignore_index<br>
# <br>
# The ignore_index parameter is useful if you want your index to be relabeled instead of having the original index labels in the sample. This takes in a Boolean input. If True, the resulting index is relabeled, but if False (default), then the resulting index stays how it was.

# maygames.sample(<br>
#     n = 10,<br>
#     weights = 'Attend.',<br>
#     random_state = 1,<br>
#     replace = True,<br>
#     ignore_index = True)<br>
# --

# ___<br>
# ## Idioms-if/then<br>
# **Name: Junqian Liu**<br>
# <br>
# UM-mail: junqianl@umich.edu



import numpy as np
import pandas as pd


# ## Dataframe method
# - The dataframes allows us to change the values of one or more columns directly by the conditions
# - df.loc allows us to choose which columns to work as the condition, and which columns to be changed based on the conditions
# - More specifically, it works as df.loc[conditions, target columns] = values



df = pd.DataFrame(
    {"apple": [4, 5, 6, 7], "boy": [10, 20, 30, 40], "cat": [100, 50, -30, -50],
    "dog": [3, 5, 0, 6]}
)
df.loc[df.apple >= 5, "boy"] = -1
df.loc[df.apple >= 5, ["cat", "dog"]] = 555
df


# ## Pandas method
# - pandas also can achieve the same aim by setting up a mask
# - pandas.DataFrame.where allows to decide if the conditions are satisfied and then change the values
# - overall, the goal is achieved by setting up the mask to the dataframe and using pandas.DataFrame.where to replace the values.
# - needs to assign to the dataframe after replacing values



df2 = pd.DataFrame(
    {"apple": [4, 5, 6, 7], "boy": [10, 20, 30, 40], "cat": [100, 50, -30, -50],
    "dog": [3, 5, 0, 6]}
)
df_mask = pd.DataFrame(
    {"apple": [True] * 4, "boy": [False] * 4, "cat": [True, False] * 2,
    "dog": [False] * 4}
)
df2 = df2.where(df_mask, 818)
df2


# ## Numpy method
# - Similar to pandas method, np.where can also replace the value through if/then statement
# - It is more convenience as it doesn't need to set up the masks
# - It works by np.where(condistions, if true, else), to be more specific, the example is given below



df3 = pd.DataFrame(
    {"apple": [4, 5, 6, 7], "boy": [10, 20, 30, 40], "cat": [100, 50, -30, -50],
    "dog": [3, 5, 0, 6]}
)
df3["elephant"] = np.where(df["apple"] > 5, "water", "banana")
df3

# -*- coding: utf-8 -*-
# ## Topics in Pandas
# **Stats 507, Fall 2021**
#

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using
# the exact title with spaces replaced by a dash.
#
# + [Filling missing values](#Filling-missing-values)
# + [Missing values in pandas](#Missing-values-in-pandas)

# + [markdown] slideshow={"slide_type": "slide"}
# ## Filling missing values
# ## Zane Zhang  zzenghao@umich.edu

# + [markdown] slideshow={"slide_type": "fragment"}
# > Creat a dataframe with nan value

# + slideshow={"slide_type": "fragment"}
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(5, 3),
    index=["a", "c", "d", "e", "f"],
    columns=["one", "two", "three"],
)

df=df.reindex(["a", "b", "c", "d", "e", "f"])
df

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Replace NA with a scalar value
#
#
# **fill the nan value with -1**

# + slideshow={"slide_type": "fragment"}
df.fillna(-1)

# + [markdown] slideshow={"slide_type": "subslide"}
# **fill nan with string**

# + slideshow={"slide_type": "fragment"}
df.fillna("missing")

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Fill gaps forward(method="Pad") or backward(method="bfill")

# + slideshow={"slide_type": "fragment"}
print("fill the data based on the forward data")
print(df.fillna(method="pad"))
print("fill the data based on the backward data")
print(df.fillna(method="bfill"))
# -

# ## Missing values in pandas
# ## Mohammad Zhalechian  mzhale@umich.edu

# * Panda is flexible with regard to handling missing data
# * $NaN$ is the default missing value marker in Pandas
# * Pandas provides two function $insa()$ and $notna()$ to detect missing values

# +
df = pd.DataFrame({'one': [1,2,3], 'two':['a','b','c']})
df2 = df.reindex([0,1,2,3,4])

pd.isna(df2)
pd.notna(df2)
pd.isna(df2['two'])
# -

# ## Inserting Missing Values
#
# * We can insert missin values using $None$ or $numpy.nan$.
# * Pandas objects provide compatibility between $None$ and $numpy.nan$.

# +
df2.loc[0,'one'] = np.nan
df2.loc[1,'two'] = None

pd.isna(df2)
# -

# ## Calculations with Missing Values
#
# * Most of descriptive statistics and computational methods are written to account for missing data
# * For example:
#     * When summing data (e.g., $np.sum()$), missing values will be treated as zero.
#     * Cumulative methods like $cumsum()$, $np.mean()$, $cumprod()$ ingnore the missing values be default. We can use $skipna=False$ to override this behavior.

np.sum(df2['one'])
np.mean(df2['one'])

# ## Filling missing values
#
# * We can fill missing values using several methods
#     * Replace missing values with a scalar value using $df.fillna('name')$.
#     * Filling the missing values with non-missing values forward or backward using $df.fillna(method = 'pad')$.

# +
df3= df2.copy()
df3.fillna('missing')

df4= df2.copy()
df4.fillna(method = 'pad')
# -
# !/usr/bin/env python3

# importing packages
from IPython.display import HTML
import pandas as pd 
import numpy as np
import os 
from scipy import stats
from scipy.stats import chi2_contingency
from collections import defaultdict
from scipy.stats import norm, inom, beta
import re 

# Andrew Heldrich
# aheldric@umich.edu

# ## `rank()` Method
# - A common need is to rank rows of data by position in a group
# - SQL has nice partitioning functions to accomplish this, e.g. `ROW_NUMBER()`
# - Pandas `rank()` can be used to achieve similar results

# ## Example
# - If we have sales data for individual people, we may want to find their sales
# rank within each state

rng = np.random.default_rng(10 * 8)
df = pd.DataFrame({"id":[x for x in range(10)],
                    "state":["MI", "WI", "OH", "OH", "MI", "MI", "WI", "WI",
                                "OH", "MI"],
                    "sales":rng.integers(low=10, high=100, size=10)})
df

# ## groupby -> rank
# - Need to chain `groupby()` and `rank()`
# - Assign results to new ranking column
# - Now we can easily see the best sales person in each state and can do
# additional filtering on this column
# - Especially useful for time-based ranking
#     - E.g. Find last 5 appointments for each patient

df["sales_rank"] = (df.groupby("state")["sales"]
                        .rank(method="first", ascending=False))
df

top_2 = (df.query('sales_rank < 3')
            .sort_values(by=["state", "sales_rank"]))
top_2


# # name: Siwei Tang Email: tangsw@umich.edu
# # Q0
# ## Time series/ data functionality
#
# The Python world has a number of available representation of dates, times, deltas, and timespans. Whiles the times series tools provided by Pandas tend to be the most useful for data science applications, it's helpful to see their relationsip to other packages used in Python.
#
# ## Native Python dates and times: `datetime` and `dateutil`
#
# Pythonn's baseic objects for working with dates and times reside in the built-in `dateime` module. Along with the third-party `dateutil` module, you can use it to quickly perform a host of useful functionalities on dates and time. 

# - build a date using the `datetime` type

from datetime import datetime
datetime(year = 2021, month=10, day=20)

# - using dateutil module to parse dates from a variety of strng formats

from dateutil import parser
date = parser.parse("20th of October, 2021")
date 

# - Once you have a `datetime` object, you can do things like printing the day of the week:

date.strftime('%A')

# In the final line, `%A` is part of the [strfyime section](https://docs.python.org/3/library/datetime.html) od Python's [datetime documentation]()

# ## Typed arrays of times: Numpy's `datatime64`
# - The `datatime64` dtype encoded dates as 64-bit inegers, and thus allows arrays of dates to be represented very compactly. The `datatime64` requires a very specific input format:

date =np.array('2021-10-20', dtype=np.datetime64)
date

# - Once we have this date formated, however, we can quickly do vectorized operations on it

date + np.arange(12)

# - One detail of the `datetime64` and `timedelta64` object is that they are build on a fundamental time unit. Because the `datetime64` object is limited to 64-bit precision, the range of encodable times is $2^{64}$ times this fundamental unit. In other words, `datetime64` imposes a trade-off between **time resolution** and **maximum time span**.

# ## Dates and times in pandas: best of both worlds
# Pandas builds upon all the tools just discussed to provide a `Timestamp` object, which combines the ease-of-use of `datetime` and `dateutil` with the efficient storage and vectorized interface of `numpy.datetime64`. From a group of these `Timestamp` objects, Pandas can construct a `DatetimeIndex` that can be used to index data in a `Series` or `DataFrame`.

date = pd.to_datetime('20th of October, 2021')
date

date.strftime('%A')

# - we can do Numpy-style vectorized operations directly on this same object:

date + pd.to_timedelta(np.arange(12),'D')

# ## Pandas Time Series Data Structures
# - for time stamps, Pandas provides the `Timestamp` type. As mentioned before, it is essentially a replacement for Python's native `datetime`, but is based on the more efficient `numpy.datetime64` date type. The associated Index structure is `DatetimeIndex`. 
# - for time Periods, Pandas provides the `Period` type. This encodes a fixed-frequency interval based on `numpy.datetime64`. The associated index structure is `PeriodIndex`.
# - For time deltas or durations, Pandas provides the `Timedelta` type. `Timedelta` is a more efficient replacement for Python's native `datetime.timedelta` type, and is based on `numpy.timedelta64`. The assocaited index structure is `TimedeltaIndex`.
#
# Passing a single date to `pd.to_datetime()` yields a `Timestamp`; passing a series of dates by default yields a `DatetimeIndex`:

dates = pd.to_datetime([datetime(2021,10,20),
                        '21st of October, 2021',
                        '2021-Oct-22',
                       '10-23-2021',
                       '20211024'])
dates

# - Any `DatetimeIndex` can be converted to a `PeriodIndex` with the `to_period()` function with the addition of a frequency code; here we use `'D'` to indicate daily frequency.

dates.to_period('D')

# - A `TimedeltaIndex` is created, for example, when a date is subtracted from another:

dates - dates[0]

# ## Regular Sequences: `pd.date_range()`

# - `pd.date_range()` for timestamsps, `pd.period_range()` for periods, and `pd.timedelta_range()` for time deltas. This is similar to Python's `range()` or `np.arange()`.

pd.date_range('2021-09-11','2021-10-21')

# - Alternatively, the date range can be specified not with a start and end point, but with a startpoint and a number of periods
# - The spacing can be modified by altering the `freq` argument, which defaults to `D`.

print(pd.date_range('2021-09-11',periods=10))
print(pd.date_range('2021-09-11', periods = 10, freq = 'H'))

# - To create regular sequencs of `Period` or `Timedelta` values, the very similar `pd.period_range()` and `pd.timedelta_range()` functions are useful. Here are some monthly periods:

pd.period_range('2021-09',periods = 10, freq='M')

# - A sequence of durations increasing by an hour:

pd.timedelta_range(0,periods=30, freq='H')


# Zehua Wang wangzeh@umich.edu

# ## Imports

import pandas as pd

# ## Question 0 - Topics in Pandas [25 points]

# ## Data Cleaning

# Create sample data
df = pd.DataFrame(
    {
        'col1': range(5),
        'col2': [6, 7, 8, 9, np.nan],
        'col3': [("red", "black")[i % 2] for i in range(5)],
        'col4': [("x", "y", "z")[i % 3] for i in range(5)],
        'col5': ["x", "y", "y", "x", "y"]
    }
)
df

# ### Duplicated Data
# - Find all values without duplication
# - Check if there is duplication using length comparison
# - return true if duplication exists

df['col3'].unique()
len(df['col3'].unique()) < len(df['col3'])

# ### Duplicated Data
# - Record duplication
# - subset: columns that need to remove duplication. Using all columns
#   if subset is None.
# - keep: Determine which duplicates to keep (if any), 'first' is default
#     - 'first': drop duplications except the first one
#     - 'last': drop duplications except the last one
#     - False: drop all duplications
# - inplace: return a copy (False, default) or drop duplicate (True)
# - ignore_index: return series label 0, 1, ..., n-1 if True, default is False

df.drop_duplicates()
df.drop_duplicates(subset=['col3'], keep='first', inplace=False)
df.drop_duplicates(subset=['col4', 'col5'], keep='last')

# ### Missing Data
# - Check if there is missing value
# - Delete missing value: pd.dropna
#     - axis: 0, delete by row; 1, drop by column
#     - how: any, delete if missing value exist; all, delete if 
#         all are missing values
#     - inplace: return a copy (False, default) or drop duplicate (True)    

df.isnull().any() # pd.notnull for selecting non-missing value
df.dropna(axis=0, how='any')

# ### Missing Data
# - Replcae missing value: pd.fillna
#     - value: the value filled up for missing value
#     - method: how to fill up the missing value
#         - 'backfill'/'bfill': using next valid observation
#         - 'pad'/'ffill': using previous valid observation
#         - None is by default
# - Generally, we could fill up the missing value with mean or median
#     for numeric data, and mode in categorical data.

df.fillna(method='ffill')
df.fillna(value=np.median(df[df['col2'].notnull()]['col2']))

# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Filling in Missing Data](#Filling-in-Missing-Data) 
# + [Topic 2 Title](#Topic-2-Title)

# ## Topic Title
# Include a title slide with a short title for your content.
# Write your name in *bold* on your title slide. 

# ## Filling in Missing Data
#
#
# *Xinhe Wang*
#
# xinhew@umich.edu

# ## Fill in Missing Data
#
# - I will introduce some ways of using ```fillna()``` to fill in missing 
# data (```NaN``` values) in a DataFrame.
# - One of the most easiest ways is to drop the rows with missing values.
# - However, data is generally expensive and we do not want to lose all 
# the other columns of the row with missing data.
# - There are many ways to fill in the missing values:
#     - Treat the ```NaN``` value as a feature -> fill in with 0;
#     - Use statistics -> fill in with column mean/median/percentile/a
#     random value;
#     - Use the "neighbors" -> fill in with the last or next values;
#     - Prediction methods -> use regression/machine learning models to 
#     predict the missing value.

# ## Example Data
# - Here we generate a small example dataset with missing values.
#
# - Notice that if we want to indicate if the value in column "b" is larger
# than 0 in column "f", but for the missiing value in column "b", 
# ```df['b'] > 0``` returns ```False``` instead of a ```NaN``` value.
# Therefore, ```NaN``` values need to be delt with before further steps.

import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randn(5, 4),
                  columns=['a', 'b', 'c', 'd'])
df.iloc[2, 1] = np.nan
df.iloc[3:5, 0] = np.nan
df['e'] = [0, np.nan, 0, 0, 0]
df['f'] = df['b']  > 0
df

# ## Fill in with a scalar value
# - We can fill in ```NaN``` values with a designated value using 
# ```fillna()```.

df['e'].fillna(0)

df['e'].fillna("missing")

# ## Fill in with statistics (median, mean, ...)
# - One of the most commonly used techniques is to fill in missing values
# with column median or mean.
# - We show an instance of filling in missing values in column "b" with 
# column mean.

df['b'].fillna(df.mean()['b'])

# ## Fill in with forward or backward values
# - We can fill in with the missing values using its "neighber" using 
# ```fillna()```.
# - Can be used if the data is a time series.
# - When the ```method``` argument of ```fillna()``` is set as ```pad``` 
# or ```ffill```, values are filled forward; when ```method``` is set as
# ```bfill```or ```backfill```, values are filled backward.
# - The ```limit``` argument of ```fillna()``` sets the limit of number 
# of rows it is allowed to fill.

df['a'].fillna(method='pad', limit=1)

df['a'].fillna(method='bfill', limit=1)

# <p>This is a short tutorial about neat pandas idioms. <a href="https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html#idioms">idioms</a> .
# From Xiatian Chen email:simoncxt@umich.edu</p>
# <h1>Idioms</h1>
# <h2>If-then and splitting:</h2>
# <pre><code>    -Clear idioms allow the code to be more readable and efficient  
#     -Always need to construct data under specific conditions, here are some examples.
# </code></pre>
# <p><code>df = pd.DataFrame(
#     {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
# )
# df.loc[df.AAA &gt;= 5, "BBB"] = -1</code>  </p>
# <pre><code>    -Can also apply if-then to multiple columns
# </code></pre>
# <p><code>df.loc[df.AAA &gt;= 5, ["BBB", "CCC"]] = 555</code>  </p>
# <pre><code>    -Can use numpy where() to apply if-then-else
# </code></pre>
# <p><code>df["logic"] = np.where(df["AAA"] &gt; 5, "high", "low")</code>  </p>
# <pre><code>    -Split the frame under condition
# </code></pre>
# <p><code>df[df.AAA &lt;= 5]
# df[df.AAA &gt; 5]</code> </p>
# <h2>Building criteria:</h2>
# <pre><code>    -When there is only 1-2 criterias, can be directly contained in df.loc  
#     -Can return a series or just modify the dataframe
# </code></pre>
# <p><code>df.loc[(df["BBB"] &lt; 25) &amp; (df["CCC"] &gt;= -40), "AAA"]
# df.loc[(df["BBB"] &gt; 25) | (df["CCC"] &gt;= 75), "AAA"] = 0.1</code>   </p>
# <pre><code>    -When there is a list of criteria, it can be done with a list of dynamically built criteria
# </code></pre>
# <p><code>Crit1 = df.AAA &lt;= 5.5
# Crit2 = df.BBB == 10.0
# Crit3 = df.CCC &gt; -40.0
# CritList = [Crit1, Crit2, Crit3]
# AllCrit = functools.reduce(lambda x, y: x &amp; y, CritList)
# df[AllCrit]</code> </p>



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
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ### Author: Houyu Jiang
# ### Email: houyuj@umich.edu

# + [Topic: pd.diff()](#Topic:-pd.diff())



# + [Direction of the difference](#Direction-of-the-difference)



# + [Distance of difference](#Distance-of-difference)

# ## Topic: pd.diff()
#
# - ```pd.diff()``` is a pandas method that we could use to
# compute the difference between rows or columns in DataFrame.
# - We could import it through ```import pandas as pd```.
# - Suppose ```df``` is a pandas DataFrame, we could use 
# ```diff``` method to compute.

df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6],
                   'b': [1, 1, 2, 3, 5, 8],
                   'c': [1, 4, 9, 16, 25, 36]})
df.diff(axis=0)

# ## Direction of the difference
# - ```pd.diff()``` by default would calculate the 
# difference between different rows.
# - We could let it compute the difference between 
# previous columns by setting ```axis=1```

df.diff(axis=1)

# ## Distance of difference
# - ```pd.diff()``` by default would calculate the difference
# between this row/column and previous row/column
# - We could let it compute the difference between this row/column
# and the previous n row/column by setting ```periods=n```

df.diff(periods=3)


# %%


# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Missing Data](#Missing-Data)

# ## Missing Data
# I will be looking at how pandas dataframes handle missing values.
# **Stefan Greenberg**
#
# sfgreen@umich.edu


# ## Imports
import numpy as np
import pandas as pd
# ## Detecting missing data
# - missing data includes `NaN`, `None`, and `NaT`
#     - can change settings so that `inf` and -`inf` count as missing
# - `.isna()` returns True wherever there is a missing value
# - `.notna()` returns True wherever there is not a missing value

# +
df = pd.DataFrame([[0.0, np.NaN, np.NaN, 3.0, 4.0, 5.0],
                   [0.0, 1.0, 4.0, np.NaN, 16.0, 25.0]], 
                 index=['n', 'n^2'])

df.append(df.isna())
# -

# ## Filling missing data
#
# - pandas makes it easy to replace missing values intelligently
# - the `.fillna()` method replaces all missing values with a given value
# - the `.interpolate()` method will use neighboring values to fill in gaps
# in data

# +
df_zeros = df.fillna(0)
df_interp = df.copy()

df_interp.loc['n'] = df_interp.loc['n']                     .interpolate(method='linear')
df_interp.interpolate(method='quadratic', axis=1, inplace=True)

df_zeros
#df_interp
# -

# ## Remove missing data with `.dropna()`
#
# - `.dropna()` will remove rows or columns that have missing values
# - set `axis` to determine whether to drop rows or columns
# - drop a row or column if it has any missing values or only if it has 
# entirely missing values by setting `how` to either *'any'* or *'all'*
# - set a minimum number of non-missing values required to drop row/column
# by setting `thresh`
# - specify what labels along other aixs to look at using `subset` i.e. 
# only drop a row if there is a missing value in a subset of the columns 
# or vise versa

# +
drop_cols   = df.dropna(axis=1)
drop_all    = df.dropna(how='all')
drop_thresh = df.dropna(thresh=5)
drop_subset = df.dropna(subset=[0, 1, 5])

print(df, '\n\n', 
      drop_cols.shape, drop_all.shape, drop_thresh.shape, drop_subset.shape)
# -
# ## Math operations with missing data
# - cumulative methods - `.cumsum()` and `.cumprod()` - by default will skip 
# over missing values
# - `.sum()` and `.prod()` treat missing values as identities
#     - `.sum()` treats missing values as zero
#     - `.prod()` treats missing values as one
#


# +
sumprod = df.append(
          df.sum()
            .to_frame()
            .transpose()
            .rename(index={0:'sum'}))

sumprod.append(
        df.prod()
          .to_frame()
          .transpose()
          .rename(index={0:'prod'}))
# -


# Question 0
#
# Name: Feng yuteng
#
# Email:ytfeng@umich.edu

import pandas as pd
import numpy as np


# ## Sparse data structures
# - overview
# - Sparse array 
# - SparseDtype
# - Sparse accessor

# ### Overview

# "So a matrix will be a sparse matrix if most of the elements of it is 0. Another definition is, a matrix with a maximum of 1/3 non-zero elements (roughly 30% of m x n) is known as sparse matrix. We use matrices in computers memory to do some operations in an efficient way."
#
# References:" https://www.mvorganizing.org/what-is-sparse-matrix-in-data-structure-with-example/#What_is_sparse_matrix_in_data_structure_with_example"
#

# ### Difference between a normal array and a sparse array

# - Sparse array(matrix) allocates spaces only for the non-default values.
# - Normal array(matrix) allocates spaces for all values. 
# - Therefore, sparse matrices are much cheaper to store since we only need to store certain entries of the matrix. 

# ## Sparse array

arr = np.random.randn(10)
arr[2:5] = np.nan
arr[7:8] = np.nan
sparr = pd.arrays.SparseArray(arr)
sparr


np.asarray(sparr)


# ## SparseDtype

# - The dtype of the non-sparse values
#
# - The scalar fill value

sparr.dtype


pd.SparseDtype(np.dtype('datetime64[ns]'))
## default value will be used for filling missing value for that dtype


# ### Sparse accessor

# - ".sparse" provides attributes and methods that are specific to sparse data 

s = pd.Series([0, 0, 1, 2], dtype="Sparse[int]")
s.sparse.density
## basically the mean of the series


s.sparse.fill_value

# # Dealing Missing Values
# *Stats 507, Fall 2021*
#
# Han Qiu
# November 11
# itskeira@umich.edu

# ## Filling missing values: Pandas.fillna() method
#   - Within pandas, a missing value is denoted by NaN/NA .
#   - It is very common to find several entries labelled NaN/NA by Python, when dealing with large dataset. 
#   - The `.fillna()`method helps to replace NaN/Na value in a Dataframe or Series with non-null data in a couple of ways.
#     

# ## Pandas.fillna() method
#   - Replace NA/NaN with a scalar value(e.g. 0).
#   - For example, you can set the value equals to 0 to fill holes using `value = 0`

import pandas as pd
import numpy as np

df = pd.DataFrame([[np.nan, 2, np.nan, 0],
                   [3, 4, np.nan, 1],
                   [np.nan, np.nan, np.nan, 5],
                   [np.nan, 3, np.nan, 4]],
                  columns=list("ABCD"))
df

df.fillna(0)

# ## Pandas.fillna() method
#   - We can propagate non-NA/ non-NaN values forward or backward by using the `method` keyword.
#   - There are total four methods avaliable `backfill`, `bfill`, `pad`, `ffill`, where the first two fill values forward and last two fill values backward.
#   
#

df.fillna(method="ffill")

# ## Pandas.fillna() method
#   - If we only want consecutive gaps filled up to a certain number of data points, we can use the `limit` keyword.
#   - For example, we can only replace the first NaN element.

values = {"A": 0, "B": 1, "C": 2, "D": 3}
df.fillna(value=values)

df.fillna(value=values, limit=1)
