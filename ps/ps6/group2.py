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

# ## sort_values
# ** Mengtong Ai**
# **mengtona@umich.edu**

#sort_values is mainly to sort the DataFrame in ascending and descending order
import numpy as np
import pandas as pd

#Let's create a DataFrame as df
data = np.random.randn(10, 4)
df = pd.DataFrame(data,columns=['a','b','c','d'])
#view df 
print(df)
#Sort column a of df in ascending order
df.sort_values(by='a')
print(df)
#Sort column a of df in descending order
df.sort_values(by='a',ascending=False)
print(df)
#### 1.2use sort_values to Sort in ascending order
#first,you should determine which column to sort by,second,call sort_values
# method
#chose a column ,here
df.sort_values(by='a')
print(df)
#or chose b column 
df.sort_values(by='b')
print(df)

#### 1.3use sort_values to Sort in descending order
#Descending order is to add a parameter as 'ascending=False' on the basis of 
# ascending order
#for example,chose a column
df.sort_values(by='a',ascending=False)
print(df)
#or chose b
df.sort_values(by='b',ascending=False)
print(df)
#In fact,'ascending=True'  means ascending,and 'ascending=False' 
# means descending
#'ascending=True'
df.sort_values(by='a',ascending=True)
print(df)
#'ascending=False'
df.sort_values(by='a',ascending=False)
print(df)

#### 1.4multi-column sorting
#If you want to sort by multiple columns, put all the columns to be arranged
# into a list, 
#and then assign values to the 'by=' parameter
#for example,wo chose a,b,c columns to sort
df.sort_values(by=['a','b','c'])
print(df)
#Explain，the principle of multi-column sorting is to sort the first column
# first, 
#then continue to sort the second column on this basis, and so on


#### 1.5ascending and descending order of multi-column sorting
#Sorting overall designation

# df sort by first column as a in ascending order
df.sort_values(by=['a','b','c'])
print(df)
## df sort by first column as a in descending order
df.sort_values(by=['a','b','c'],ascending=False)
print(df)

#Sorting freely specified
#The values in 'by=' parameter and 'ascending=' parameter correspond one-to-one


# df  is arranged in descending order in column a first, second in ascending order in column b,and in ascending order in column c last
df.sort_values(by=['a','b','c'],ascending=[False,True,True])
print(df)
# df  is arranged in ascending order in column b first, second in descending order in column c
df.sort_values(by=['b','c'],ascending=[True,False])
print(df)

# ## Data Cleaning
# **Jiaxi Chen**

# References: 
# * https://www.w3schools.com/python/pandas/pandas_cleaning.asp
# * https://pandas.pydata.org/docs/reference/index.html
#
#
# ### Finding Duplicates
# - Duplicate rows are rows that have been registered more than one time.
#
# - `pandas.DataFrame.duplicated` returns boolean series denoting duplicate rows.
# - `keep` determines which duplicates (if any) to mark.
#     - `keep = False` : Mark all duplicates as True.
#     - `keep = first` : Mark duplicates as True except for the first occurrence.
#     - `keep = last` : Mark duplicates as True except for the last occurrence.

import pandas as pd
import numpy as np
from pydataset import data

df = data('iris')
df.head()
print(df[df.duplicated(keep=False)])
print(df[df.duplicated(keep='first')])

# ### Removing Duplicates
# - We can use the `drop_duplicates()` method to remove duplicates
# - The `inplace = True` will make sure that the method does NOT return
# a new DataFrame, but it will remove all duplicates from the original
# DataFrame.

print(df.shape)
df.drop_duplicates(inplace = True)
print(df.shape)

# ### Finding NaN
# - Check for NaN under a single DataFrame column:
# `df['your column name'].isnull().values.any()`
# - Count the NaN under a single DataFrame column:
# `df['your column name'].isnull().sum()`
# - Check for NaN under an entire DataFrame: `df.isnull().values.any()`
# - Count the NaN under an entire DataFrame: `df.isnull().sum().sum()`

data = {'set_of_numbers': [1,2,3,4,5,np.nan,6,7,np.nan,8,9,10,np.nan]}
df = pd.DataFrame(data)
check_for_nan = df['set_of_numbers'].isnull()
print (check_for_nan)
nan_count = df['set_of_numbers'].isnull().sum()
print (nan_count)
nan_exist = df['set_of_numbers'].isnull().values.any()
print(nan_exist)

# ### Replacing NaN with mean, median or mode
# - A common way to replace empty cells, is to calculate the mean, median or mode value of the column.
# - Pandas uses the `mean()` `median()` and `mode()` methods to calculate the respective values for a specified column

x = df["set_of_numbers"].mean()
df["set_of_numbers"].fillna(x, inplace = True)
print(df)
nan_count = df['set_of_numbers'].isnull().sum()
print (nan_count)

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Topic Title](#Topic-Title) 
# + [Topic 2 Title](#Topic-2-Title)
# + [DataFrame Method: `select_dtypes()`](#DataFrame-Method:-`select_dtypes()`) 

# ## Topic Title
# Include a title slide with a short title for your content.
# Write your name in *bold* on your title slide. 

# ## DataFrame Method: `select_dtypes()`
# *Brody Erlandson*
# berlands@umich.edu
#
# We can select the columns with a specific type(s), and/or exclude columns
# with a specific type(s).
#   
# - Parameters:
#   - include: scalar or list-like. Default None.
#   - exclude: scalar or list-like. Default None.
# - Returns: DataFrame

# ## `select_dtypes()` Example

df = pd.DataFrame({"strings1" : ["a", "b", "c"], "ints" : [1, 2, 3],
                   "floats" : [.1, .2, .3], 
                   "category" : ["cat1", "cat1", "cat2"],
                   "string2" : ["x", "y", "z"]})
df = df.convert_dtypes()
df["category"] = df["category"].astype("category")
df.select_dtypes(include=["string", "category"])

# Similarly:

df.select_dtypes(exclude=[float, int])

# ## When to use `select_dtypes()`
#
# Say you have a lot of columns of different types. You'd like to apply some
# function to only one type. Instead of finding all the indices or names
# of the columns, we can use `select_dtypes()` to get these columns.  
# 
# For example:   

df.select_dtypes(include="string").apply(lambda x : x + "_added")


# In[ ]:


############################ pd_topic_group2_3e_yangyli ##############################


########################### pd_topic_group2_4j_aayushi #############################
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

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using
# the exact title with spaces replaced by a dash.
#
# + [Topic Title](#Topic-Title)
# + [Topic 2 Title](#Topic-2-Title)

# ## Topic Title
# Include a title slide with a short title for your content.
# Write your name in *bold* on your title slide.


# Aayushi Sinha
#
# aayushi@umich.edu
#
#
# ##  Timedeltas in Pandas

# ### Class pd.Timedelta
#
# * It represents a duration of time or date. Easy to use for date or time manipulations.
# * It is a similar to the python class of datetime.timedelta.
# * It is expressed in difference units, e.g. days, hours, minutes, seconds.

# In[1]:


import pandas as pd
from datetime import datetime, timedelta

#Calculating the number of days between two dates.
present_date = datetime.now()
print ("Present Date", str(present_date))
future_date = present_date + timedelta(days = 6)
print("Future Date", str(future_date) )

print("Days left", str(present_date - future_date))


# ### Parsing
# * Prasing through a string or an integer with units in the argument can create a timedelta object.
# * pd.to_timedelta can convert a scalar, array, list, or series from a recognized timedelta
#   format/ value into a Timedelta type.

# In[3]:


#Parsing and to_timedelta
print (pd.Timedelta('2 days 2 hours 15 minutes 30 seconds'))
#Converting to timedelta object
pd.to_timedelta("1 days 06:05:01.00003")


# ### Operations
#
# * You can construct timedelta64[ns] Series/Dataframes through subtraction operations and operate on the series/dataframes.
# * NaT values are supported in timedelta series.
# * min, max and the corresponding idxmin, idxmax operations are supported. Even negate can be used.

# In[5]:


# Operation Examples
s = pd.Series(pd.date_range('2012-1-1', periods=3, freq='D'))
td = pd.Series([ pd.Timedelta(days=i) for i in range(3) ])
df = pd.DataFrame(dict(A = s, B = td))
df['C']=df['A']+df['B']
df['D']=df['C']-df['B']
print(df)


############################ pd_topic_group2_4i_lydiajr ##############################

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

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using
# the exact title with spaces replaced by a dash.
#
# + [Topic Title](#Topic-Title)
# + [Topic 2 Title](#Topic-2-Title)

# ## Topic Title
# Include a title slide with a short title for your content.
# Write your name in *bold* on your title slide.

#!/usr/bin/env python
# coding: utf-8

# + [Timedeltas: Representing changes in time](#Topic-Title)
# *Lydia Rogers*, lydiajr@umich.edu
#
# Reference for timedeltas can be found [here](https://pandas.pydata.org/pandas-docs/stable/user_guide/timedeltas.html)

# ## Intro to Timedeltas
# * In addition to the datetime functionality that works well with pandas, there are occasions where we will want to analyze changes in time rather than dates.
# * We can represent these changes in time as timedeltas using the `datetime` module in addition to pandas.

# In[1]:


# Load required modules
import pandas as pd
import datetime

# Initializing timedeltas
# Can initialize using pd.Timedelta...
t1 = pd.Timedelta("2 days")
t2 = pd.Timedelta(2, unit = "d")
print(t1 == t2)

# null = NaT
t3 = pd.Timedelta("nan")
t4 = pd.Timedelta("nat")
print(t3, t4)

# negative times also supported
t5 = pd.Timedelta("-1us")
t6 = pd.Timedelta("-3hr")
print(t5, t6)


# ... or from a time string using to_timedelta
t7 = pd.to_timedelta("1 days 06:05:01.00003")
t8 = pd.to_timedelta("247ms")
print(t7, t8)


# ## Operations using timedeltas
# * Timedeltas can be used in arithmetic operations such as addition and subtraction with other timedeltas or datetimes, as well as in scalar multiplication.
# * Other operations supported include minimum and maximum calculations, and absolute values.
# * We can convert timedeltas to different scales (hours, minutes, seconds) by dividing one timedelta object by another.

# In[2]:


# Create example dataframe
sundays = pd.Series(pd.date_range("2021-10-24", periods=6, freq="W"))
td = pd.Series([pd.Timedelta(days=i*7) for i in range(6)])
df = pd.DataFrame({"dates": sundays, "days": td})

# Timedelta arithmetic
df["new_date"] = df["dates"] + 2 * df["days"]
df["new_timedelta"] = df["dates"] - df["new_date"]
df["scaled_timedelta"] = df["new_timedelta"] * 0.4
df["seconds_timedelta"] = df["scaled_timedelta"] / pd.Timedelta(1, "s")
print(df)

# Additional operations
print("min:", df["new_date"].min())
print("max:", df["new_date"].max())
print(abs(df["new_timedelta"]))


# ## Summarizing Timedeltas
# * Timedeltas and datetimes are also supported by most reduction operations such as mean, median, quantile, and sum.
# * These reduction operations, implemented in pandas, offer easy ways to summarize changes in time.

# In[3]:


print("mean timedelta:", df["seconds_timedelta"].mean())
print("mean date:", df["new_date"].mean())

print("median timedelta:", df["seconds_timedelta"].median())
print("median date:", df["new_date"].median())

print("timedelta 75th quantile:", df["seconds_timedelta"].quantile(0.75))
print("date 75th quantile:", df["new_date"].quantile(0.75))

print("timedelta sum:", df["seconds_timedelta"].sum())


############################ pd_topic_yangyli ##############################

#!/usr/bin/env python
# coding: utf-8

# ## STAT 507 Problem Set 4
# ## Name: Yang Li (46933158)
# ## Email: yangyli@umich.edu
# > ## Question 0 - Topics in Pandas [25 points]
#

# In[1]:


import pandas as pd
import numpy as np
import datetime
from scipy.stats import norm
import matplotlib.pyplot as plt
import math
from scipy import stats


# ## Time series
# - Pandas contains extensive capabilities and features for working with time series data for all domains.
# - Parsing time series information from various sources and formats.

# In[2]:


dti = pd.to_datetime(["1/1/2021",
                      np.datetime64("2021-01-01"),
                      datetime.datetime(2021, 1, 1)])
dti


# ## Time series
# - Generate sequences of fixed-frequency dates and time spans.
# - Manipulating and converting date times with timezone information.
#

# In[3]:


dti = pd.date_range("2021-01-01", periods=2, freq="H")
print(dti)
dti1 = dti.tz_localize("UTC")
print(dti1)
dti1.tz_convert("US/Pacific")


# ## Time series
#
# - Resampling or converting a time series to a particular frequency.

# In[4]:


idx = pd.date_range("2021-01-01", periods=4, freq="H")
ts = pd.Series(range(len(idx)), index=idx)
ts


# ## Time series
#
# - Performing date and time arithmetic with absolute or relative time increments.

# In[5]:


friday = pd.Timestamp("2021-10-22")
print(friday.day_name())
# Add 1 day
saturday = friday + pd.Timedelta("1 day")
print(saturday.day_name())


# In[ ]:


############################ pd_topic_group2_2a_pxchen ##############################


# In[ ]:


"""
@author: Panxi Chen (pxchen)
@email: pxchen@umich.edu 
"""

### PS4 - Question 0 - Topics in Pandas


# In[1]:


# Module imports
import pandas as pd
import numpy as np
from datetime import *
from IPython.core.display import display, HTML


# ## Timedeltas
# ### Overview
# - Using Timedeltas
# - Filter data with Timedelta
#     - Example - number of homework
# - Example - age
# - Arithmetic operation
# - Example - Arithmetic Operation

# ## Timedeltas
# - Timedeltas is a type that shows the difference between values of date times. For instance, the difference between years, months, days, hours, minutes, seconds, even milliseconds, and so on. Also, the result will give in the Timedelta type.
# - the form of the datetime is not restricted. It can be either mm-dd-yyyy or yyyy-mm-dd, "-" or "/".  
# - if we do not assign month or year, then it will have default value 1, which is first day and January.

# In[2]:


# Construct Timedelta by string
td0 = pd.Timedelta('1 days 7 hours 45 minutes 30 seconds')
print(td0)


# In[3]:


td2 = pd.date_range('2020-01-24', periods=7, freq='15min')
print("The frequence is ", pd.to_timedelta(td2.freq))


# In[4]:


# Construct Timedelta
to_td = pd.to_timedelta('30min')

# transform from minutes to seconds
td_second = to_td.total_seconds()

# transform from seconds to time
td_period = str(pd.Timedelta(seconds=700000))

# print results
print("seconds:", int(td_second), "s")
print("period:", td_period)


# In[5]:


td_mdy = pd.to_datetime('8-18-2021') - pd.to_datetime('12-21-2020')

td_n = pd.to_datetime('2020-12-24') - pd.to_datetime('2019')
td_ny = pd.to_datetime('2020-12-24') - pd.to_datetime('2019-1')
td_nyr = pd.to_datetime('2020/12/24') - pd.to_datetime('2019-1-1')

print("datetime in mm-dd-yyyy with assigned date:", td_mdy)
print("datetime in yyyy-mm-dd with assigned year and month:", td_ny)
print("datetime in yyyy-mm-dd with assigned year:", td_n)
print("datetime in yyyy-mm-dd with assigned date on Jan. 1st:", td_n)


# ## Filter data with Timedelta
# - We can use Timedelta to filter the date data to obtain the results we need.

# ## Example - number of homework
# - In following example, we are going to figure out the number of homework that will due in a week.
# - From the dataframe df_dues, we could see from index 1 to 3, the homework is closed.

# In[6]:


dues = {'due_date': ['2021/10/07', '2021/10/11', 
                     '2021/10/22', '2021/10/24', 
                     '2021/10/27', '2021/10/31',], 
        'hw_number': [3, 1, 2, 5, 4, 2]}
df = pd.DataFrame(dues, index=[1, 2, 3, 4, 5, 6])
display(HTML(df.to_html()))


# In[7]:


df['due_date'] = pd.to_datetime(df['due_date'])
df = df[(df['due_date'] - datetime.now()) > pd.Timedelta(days=0)]
df = df[(df['due_date'] - datetime.now()) < pd.Timedelta(days=7)]
display(HTML(df.to_html(index=False)))
print(df['hw_number'].sum(), "homework needs to be finished in one week.")


# ## Example - age
# - We could apply Timedelta to calculate the age of a person given his birth date.
# - In this example, we use Timedelta to find the age for someone born on 06/27/1998.

# In[8]:


age = int((datetime.now() 
           - pd.to_datetime('6-27-1998')) 
          / pd.Timedelta(days=365))
print("age:", age)


# ## Arithmetic Operation
# - This example shows the arithmetic operation of Timedelta. Also, a time series is constructed further on the basis of Timedelta.

# ## Example - Arithmetic Operation

# In[9]:


time = pd.date_range(start='2021-9-7', periods=7, freq='7D')
print("Time period from {} to {}".format(time.min(), time.max()))


# In[10]:


# add 5 minutes
time_plus = time + pd.Timedelta(minutes=5)

# subtract datetime(year, month, day, hour, minute)
time_minus = time - datetime(2020, 1, 21, 3, 5)

#print results
print("Addition: ", time_plus)
print("Subtraction: ", time_minus)


# In[11]:


td1 = pd.Series([pd.Timedelta(days=3*(i+1)) for i in range(7)])
df1 = pd.DataFrame(dict(date=time, period=td1))

# operations
df1['addition']=df1['date'] - df1['period']
df1['subtraction']=df1['date'] - df1['period']
display(HTML(pd.DataFrame(df1).to_html()))


# In[12]:


# Construct Time Series
ts1 = pd.Series(np.random.randn(7), index=time)
print('Time seris (Oct. 5th):', ts1['2021-10-05'])
display(HTML(pd.DataFrame(ts1).to_html()))


# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
#
# + [Dropping](#Dropping) 
# + [Pandas Aggregation](#Pandas-Aggregation)
# + [Pandas with Time](#Pandas-with-Time)
# + [Window Functions](#Window-Functions) 
# + [Rolling Functions](#Rolling-Functions) 
# + [Expanding Functions](#Expanding-Functions) 
# + [Time series](#Time-series)
# + [Timestamps vs time spans](#Timestamps-vs-time-spans)

# ## Dropping
#
# __Pengfei Liu__    
# 2021/11/16

# ## Dropping In Pandas
# - Delete (some parts of) data samples under certain conditions using `pd.drop()`.
# - Use `axis` to choose to drop from the index(`0` or `index`) or columns(`1` or `columns`).
# - General usage: `df.drop(df[<some boolean condition>].index)`

import numpy as np
import pandas as pd
df1 = pd.DataFrame(np.arange(24).reshape(6, 4), columns=['A', 'B', 'C', 'D'])
print(df1)
#drop columns
print(df1.drop(['B','C'], axis = 1))
#drop the items that is less than 6 in column A.
print(df1.drop(df1[df1['A'] < 6].index))

# - In the previous test, we showed the importance of `labels`, which was `df1[df1['A'] < 6].index` there.
# - we can also use the parameter `level` to make multiple indexing.
#

midx = pd.MultiIndex(levels=[['lama', 'cow', 'falcon'],
                             ['speed', 'weight', 'length']],
                     codes=[[0, 0, 0, 1, 1, 1, 2, 2, 2],
                            [0, 1, 2, 0, 1, 2, 0, 1, 2]])
df = pd.DataFrame(index=midx, columns=['big', 'small'],
                  data=[[45, 30], [200, 100], [1.5, 1], [30, 20],
                        [250, 150], [1.5, 0.8], [320, 250],
                        [1, 0.8], [0.3, 0.2]])
print(df)
print(df.drop(index = 'cow', columns = 'small'))

# - We also have other relative functions such as `pd.dropna()` and `pd.drop_duplicates()`.

# ## Pandas Aggregation
#
# __LiHsuan Lin__    
# 2021/11/16

# ####  An essential piece of analysis in large dataset is efficient summarization
# #### There are a few aggregation operations in Pandas that are useful
# #### Aggregate using one or more operations over the specified axis

# +


# create df
df = pd.DataFrame([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [np.nan, np.nan, np.nan]],
                  columns=['A', 'B', 'C'])
df

# +


# sum and min aggregation operation
df.agg(['sum', 'min'])


# ### Normally, it is used hand in hand with group_by to find the aggregation on groups
# 
# - first specify the column (group) and then apply agg

# +


# create example df
data1 = {'Name':['Max', 'Bill', 'Max', 'Princi', 
                 'Gaurav', 'Bill', 'Princi', 'Tom'], 
        'salary(K)':[80, 78, 56, 110, 
               78, 87, 150, 32], 
        'Address':['Nagpur', 'Kanpur', 'Allahabad', 'Kannuaj',
                   'Jaunpur', 'Kanpur', 'Allahabad', 'Aligarh'], 
        'Qualification':['MS', 'MA', 'MCA', 'Phd',
                         'B.Tech', 'Phd', 'MA', 'MS']}
df = pd.DataFrame(data1)
df

# +


# group by Name
df.groupby(['Name']).mean()

# +


df.groupby(['Name','Qualification']).sum()


# - multiple aggregrations
# - use {Column:Operation} to specify the group and which operations to use

# +


df.groupby('Name').agg({'salary(K)':['min', 'max']})
# -

# ## Pandas with Time
# *Stats 507, Fall 2021*  
#    
# __Jinhuan Ke__  
# jhgoblue@umich.edu  
# 10/19/2021
#   
# - Timestamp
# - Period
# - DatetimeIndex and PeriodIndex
# - Generating ranges of timestamps

import pandas as pd
import numpy as np
import datetime

# ## Timestamp
# - Timestamped data is the most basic type of time series data that associates values with points in time. 
# - For pandas objects it means using the points in time.
# - use `pd.Timestamp()` to generate time series data save in seconds.
# - time variable can be `year, month, day` or `"year-month=day"`.

print(pd.Timestamp("2021-10-21"))
print(pd.Timestamp(2021, 10, 21))

# ## Period
# - Time spans can be represented by `Period`.
# - use `pd.Period()` to generate time span variables.
# - the `freq` parameter in the function specify the frequency of the time series.

print(pd.Period("2021-10-21", freq='Y'))
print(pd.Period("2021-10-21", freq='M'))
print(pd.Period("2021-10-21", freq='D'))

# ## DatetimeIndex and PeriodIndex
# - Timestamp and Period can serve as an index. 
# - Lists of Timestamp and Period are automatically coerced to DatetimeIndex and PeriodIndex respectively.

dates = [
    pd.Timestamp("2021-10-21"),
    pd.Timestamp("2021-10-22")
]
t1 = pd.Series(np.random.randn(2), dates)
print(t1.index)
print(type(t1))
t1

periods = [pd.Period("2021-10-21"), pd.Period("2021-10-22")]
t2 = pd.Series(np.random.randn(2), periods)
print(t2.index)
print(type(t2))
t2

periods_m = [pd.Period("2021-10-21", 'M'), pd.Period("2021-10-22", 'M')]
t3 = pd.Series(np.random.randn(2), periods_m)
print(t3.index)
print(type(t3))
t3

# ## Generating ranges of timestamps
# - we can use the `date_range()` and `bdate_range()` functions to create a DatetimeIndex. 
# - The default frequency for `date_range` is a calendar day,
# - while the default for `bdate_range` is a business day.
# - `freq` parameter in function can refer to the [Date Offset][do]
#
# [do]: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

# +
start = datetime.datetime(2021, 10, 21)
end = datetime.datetime(2021, 12, 21)
dtindex_1 = pd.date_range(start, end)
print(dtindex_1)

dtindex_2 = pd.bdate_range(start, end)
print(dtindex_2)

dtindex_3 = pd.bdate_range(start, periods=10, freq='BM') #business month end
print(dtindex_3)
# -

# # Question 0 - Topics in Pandas

# ##  Window Functions
# * Provide the calculation of statistics 
# * Primarily used in signal processing and time series data
# * Perform desired mathematical operations on consecutive values at a time

# ## Rolling Functions
# * Can apply on Series and Dataframe type
# * For DataFrame, each function is computed column-wise
# * Here is an example for calculation of rolling sum
# * Similar way to calculate the mean, var, std ...

series = pd.Series(range(5))
df = pd.DataFrame({"A": series, "B": series ** 3})
df.rolling(3).sum()

# ## Parameters
# * **win_type** changes the window function (equally weighted by default)
# * You can set the minimum number of observations in window required to have a
# value by using **min_periods=k**
# * Set the labels at the center of the window by using **center==True** 
# (set to the right edge by default)

print(df.rolling(3, win_type='gaussian').sum(std=3))
print(df.rolling(3, win_type='gaussian', center=True).sum(std=3))
print(df.rolling(3, win_type='gaussian', min_periods=2, 
                 center=True).sum(std=3))

# ## Expanding Functions
# * Calculate the expanding sum of given DataFrame or Series
# * Perform desired mathematical operations on current all previous values
# * Similar way to calculate the mean, var, std...
df.expanding(min_periods=2).sum()

# + [General Time Series Functions](#General-Time-Series-Functions)
# modules: -------------------------------------------------------------------
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import ttest_ind_from_stats
from scipy.stats import norm
from Stats507_hw4_helper import ci_prop
from Stats507_hw4_helper import ci_mean
from numpy import arange
import itertools
from scipy.stats import binom
from collections import defaultdict
import math
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import datetime
# + [Convert to Timestamps](#Convert-to-Timestamps) [markdown]
# ## Time Series 
# **Ran Yan**
# -
# # Question 0 - Topics in Pandas
#
# ##  General Time Series Functions
# * pandas contains extensive capabilities and features for working with time series data for all domains.
# * can parse time series information in different formats and sources
# * can manipulating and converting date times with timezone information

# +
# example 1
dti = pd.to_datetime(
    ["5/20/2000", np.datetime64("2000-05-20"), datetime.datetime(2000, 5, 20)]
)
dti

# example 2
dti = pd.date_range("2000-01", periods=5, freq="D")
dti

# example 3
dti = dti.tz_localize("UTC")
dti
# -

# ## Convert to Timestamps
# * when convert to timestamps, convert series to series and convert list-like data to DatetimeIndex
# * return a single timestamp if pass a string
# * can use format argument to ensure specific parsing, here is an example below

pd.to_datetime("2021/10/23", format="%Y/%m/%d")

# ## Other Useful Time Series Functions
# - `between_time` 
#     - to select rows in data frame that are only between certain time range
#     - here is an example below to select time from 9:00 to 10:00
# - `date_range`
#     - convert timestamp to a 'unix' epoch
# - `bdate_range`
#     - create DatetimeIndex for in a range of business days

# +
rng = pd.date_range('2/3/2000', periods=24, freq='H')
ts = pd.Series(np.random.randn(len(rng)), index=rng)
ts.iloc[ts.index.indexer_between_time(datetime.time(9), datetime.time(10))]

stamps = pd.date_range("2021-10-23 20:15:05", periods=2, freq="H")
stamps

start = datetime.datetime(2021, 10, 20)
end = datetime.datetime(2021, 10, 23)
index = pd.bdate_range(start, end)
index
# -

# Eduardo Ochoa Rivera \
# eochoa@umich.edu \
# November 20, 2021

# ## Module imports

import numpy as np
import pandas as pd
import datetime

# ## Time series

# pandas contains extensive capabilities and features for working with time series data for all domains.
# For example: 
# * Parsing time series information from various sources and formats

dti = pd.to_datetime(["1/1/2018", 
                      np.datetime64("2018-01-01"), 
                      datetime.datetime(2018, 1, 1)])
dti

# * Generate sequences of fixed-frequency dates and time spans

dti = pd.date_range("2018-01-01", periods=3, freq="H")
dti

# * Performing date and time arithmetic with absolute or relative time increments. It can be specially usefull for financial data analysis.
#

friday = pd.Timestamp("2018-01-05")
print(friday.day_name())
saturday = friday + pd.Timedelta("1 day")
print(saturday.day_name())
monday = friday + pd.offsets.BDay()
print(monday.day_name())

# ## Timestamps vs time spans

# Timestamped data is the most basic type of time series data that associates values with points in time.

pd.Timestamp(datetime.datetime(2012, 5, 1))

# However, in many cases it is more natural to associate things like change variables with a time span instead.
#

pd.Period("2011-01"), pd.Period("2012-05", freq="D")

# **Timestamp** and **Period** can serve as an index.

# +
dates = [
    pd.Timestamp("2012-05-01"),
    pd.Timestamp("2012-05-02"),
    pd.Timestamp("2012-05-03"),
]
ts = pd.Series(np.random.randn(3), dates)
print(ts.index) 
ts

periods = [pd.Period("2012-01"), 
           pd.Period("2012-02"), 
           pd.Period("2012-03")]
ts = pd.Series(np.random.randn(3), periods)
print(ts.index) 
ts

# ## Working with Python APIs
# 
# _Tianyu Jiang (prajnaty@umich.edu)_
# 
# ### Background knowledge: What is an application programming interface (API)
# 
# - An API is a set of defined rules that
# explain how computers or applications communicate with one another.
# 
# - APIs sit between an application and the web server, acting as an intermediary layer that processes data transfer between systems.
#     1. __A client application initiates an API call__ to retrieve information — also known as a request.
#     This request is processed from an application to the web server
#     via the API’s Uniform Resource Identifier (URI) 
#     and includes a request verb, headers, and sometimes, a request body.
#     1. After __receiving a valid request__,
#     the API __makes a call__ to the external program or web server.
#     1. The server sends __a response__
#     to the API with the requested information.
#     1. __The API transfers the data__ 
#     to the initial requesting application.
# 
# Ref: https://www.ibm.com/cloud/learn/api
# 
# ### Import libraries
# 1. __requests__ library helps us get the content 
# from the API by using the ```get()``` method.
# The ```json()``` method converts the API response to JSON format for easy handling.
# 1. __json__ library is needed so that we can work with the JSON content we get from the API.
# In this case, we get a dictionary for each Channel’s information such as name, id, views and other information.
# 1. __pandas__ library helps to create a dataframe
# which we can export to a .CSV file in correct format with proper headings and indexing.

# In[1]:


# import libraries
import numpy as np
import pandas as pd
import requests
import json


# - Here I created a json dict,
# if you want to get json from web url, you need to use an API key.
#     - If you don't use an API key, you may get
#     [this](https://stackoverflow.com/questions/54783076/you-must-use-an-api-key-to-authenticate-each-request-to-google-maps-platform-api) error message.
#     - You may use ```requests.get(url).json()```
#     to get the response from the API for the url (in json format).
# 
# 
# - Reference: https://stackoverflow.com/questions/46578128/pandas-read-jsonjson-url

# In[2]:


json_dict = {
"message": "hello world",
"result": [{"id":12312312, "TimeStamp":"2017-10-04T17:39:53.92","Quantity":3.03046306,},
           {"id": 2342344, "TimeStamp":"2017-10-04T17:39:53.92","Quantity":3.03046306,}]
}

df = pd.json_normalize(json_dict['result'])

# Sanity check
print(df)


# In[3]:


# Process the timestamp and move it to front
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
df = df.set_index('TimeStamp')

# Sanity check
print(df)


# ### Alternative approach
# 
# - Use ```pd.DataFrame(df['result'].values.tolist())```

# In[4]:


df = pd.read_json('https://bittrex.com/api/v1.1/public/getmarkethistory?market=BTC-ETC')
df = pd.DataFrame(df['result'].values.tolist())

# Process the timestamp and move it to front
df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
df = df.set_index('TimeStamp')

# Sanity check
print(df.head())

# ## If Then
# **Kailin Wang**
# **wkailin@umich.edu**
# -

# %%
# modules: --------------------------------------------------------------------
import numpy as np
import pandas as pd
from os.path import exists

# + [markdown] magic_args="[markdown]"
# ## Pandas `if-then`  idioms
# - The `if-then/if-then-else` idiom is a compact form of if-else that can be implemented to columns in `pd.DataFrame`
# - Expressed on one column, and assignment to another one or more columns
# - Use pandas where after you’ve set up a mask
# -


df = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
)
df

# + [markdown] magic_args="[markdown]"
# ## Pandas `if-then`  idioms
# - An `if-then` on one column
# -


df.loc[df.AAA >= 5, "BBB"] = -1
df

# + [markdown] magic_args="[markdown]"
# - An `if-then` with assignment to 2 columns:
# -


df.loc[df.AAA >= 5, ["BBB", "CCC"]] = 1022
df

# + [markdown] magic_args="[markdown]"
# ## Pandas `if-then`  idioms
# - Use pandas where after you’ve set up a mask
# -


df_mask = pd.DataFrame(
    {"AAA": [True] * 4, "BBB": [False] * 4, "CCC": [True, False] * 2}
)
df.where(df_mask,1022)

# + [markdown] magic_args="[markdown]"
# ## Pandas `if-then-else`  idioms
# - if-then-else using NumPy’s where()
# -


df = pd.DataFrame(
    {"AAA": [4, 5, 6, 7], "BBB": [10, 20, 30, 40], "CCC": [100, 50, -30, -50]}
)
df
df["logic"] = np.where(df["AAA"] > 5, "high", "low")
df

# + [markdown] magic_args="[markdown]"
# ## Time Delta
# **Liuyu Tao**
# **liuyutao@umich.edu**

# + [markdown] magic_args="[markdown]"
# ## Overview
# - Parsing
# - to_timedelta

# + [markdown] magic_args="[markdown]"
# ## Parsing
# - There are several different methods to construct the Timeselta, below are the examples
# -


import pandas as pd
import datetime

# read as "string"
print(pd.Timedelta("2 days 3 minutes 36 seconds"))
# similar to "datetime.timedelta"
print(pd.Timedelta(days=2, minutes=3, seconds=36))
# specify the integer and the unit of the integer
print(pd.Timedelta(2.0025, unit="d"))

# + [markdown] magic_args="[markdown]"
# ## Sorting
# **Julia Weber- juliaweb@umich.edu**

# + [markdown] magic_args="[markdown]"
# ## Sorting- About
# - Pandas has built in functions that allow the user to sort values in a column or index of a dataframe.
# - Sorting is important, as a user can look for patterns in the data and easily determine which observations have the highest/lowest values for a certain variable.

# + [markdown] magic_args="[markdown]"
# ## sort_values() Function
# - The sort_values() function can be used to order rows of a dataframe by the values of a column.
# - Default sorts low to high. If we set ascending=False, sorts high to low.
# -


import pandas as pd

names = ["Julia", "James", "Andrew", "Sandy", "Joe"]
ages = [15, 18, 16, 30, 26]
test_df = pd.DataFrame({"name" : names, "age" : ages})
test_df.sort_values("age", ascending=False)

# + [markdown] magic_args="[markdown]"
# ## sort_index() Function
# - The sort_index() function can be used to sort the index of a dataframe.
# - This function is similar to the sort_values() function, but is applied to the index.
# -


sorted_df = test_df.sort_values("age", ascending=False)
sorted_df.sort_index()

# + [markdown] magic_args="[markdown]"
# ## Timestamp class
# **Yuelin He- yuelinhe@umich.edu**

# + [markdown] magic_args="[markdown]"
# Timestamp is Pandas' equivalent (and usually interchangeable) class of 
# python’s Datetime. To construct a Timestamp, there are three calling 
# conventions:
#
# 1. Converting a datetime-like string.
#
# 1. Converting a float representing a Unix epoch in units of seconds.
#
# 1. Converting an int representing a Unix-epoch in units of seconds in a 
# specified timezone.
#
# The form accepts four parameters that can be passed by position or keyword.
#
# There are also forms that mimic the API for datetime.datetime (with year, 
# month, day, etc. passed separately through parameters).
#
# See the following code for corresponding examples:
# -


import pandas as pd

## datetime-like string
print(pd.Timestamp('2021-01-01T12'))

## float, in units of seconds
print(pd.Timestamp(889088900.5, unit='s'))

##int, in units of seconds, with specified timezone
print(pd.Timestamp(5201314, unit='s', tz='US/Pacific'))

# + [markdown] magic_args="[markdown]"
# In Pandas, there are many useful attributes to do quick countings in Timestamp.
#
# - Counting the day of the...
# + year: using *day_of_year*, *dayofyear*
# - Counting the week number of the year: using *week*, *weekofyear*
# - Counting the number of days in that month: using *days_in_month*, *daysinmonth*
#
# -


# Counting the day of the week
ts = pd.Timestamp(2018, 3, 21)
print(ts.day_of_week)
print(ts.dayofweek)

# Counting the day of the year
print(ts.day_of_year)
print(ts.dayofyear)

# Counting the week number of the year
print(ts.week)
print(ts.weekofyear)

# Counting the number of days in that month
print(ts.days_in_month)
print(ts.daysinmonth)

# + [markdown] magic_args="[markdown]"
# Whether certain characteristic is true can also be determined.
#
# - Deciding if the date is the start of the...
# + month: using *is_month_start* [markdown]
# # - Similarly, deciding if the date is the end of the...
# + month: using *is_month_end* [markdown]
# # - Deciding if the year is a leap year: using *is_leap_year*
# -


# # Start?
print(pd.Timestamp(2000, 1, 1).is_year_start)
print(pd.Timestamp(2000, 2, 1).is_quarter_start)
print(pd.Timestamp(2000, 3, 1).is_month_start)

# # End?
print(pd.Timestamp(2000, 12, 31).is_year_end)
print(pd.Timestamp(2000, 12, 30).is_quarter_end)
print(pd.Timestamp(2000, 11, 30).is_month_start)

# Leap year?
print(pd.Timestamp(2000, 12, 31).is_leap_year)
print(pd.Timestamp(2001, 12, 30).is_leap_year)

# + [markdown] magic_args="[markdown]"
#
# Reference: 
# https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.html#

# + [markdown] magic_args="[markdown]"
# ## Table Styler
# ### Manipulate many parameters of a table using the table Styler object in pandas.
# **Xiying Gao**

# + [markdown] magic_args="[markdown]"
# ## Pandas.concat
# **Ziyin Chen- email: edwardzc@umich.edu**

# + [markdown] magic_args="[markdown]"
# ## General Discription
# * Concatenate pandas objects along a particular axis with optional set logic along the other axes.
#
# * Can also add a layer of hierarchical indexing on the concatenation axis, which may be useful if the labels are the same (or overlapping) on the passed axis number.

# + [markdown] magic_args="[markdown]"
# ## concat
# * used to combine tow dataframe or combining two series 
#     1. can be used to join two DataFrame or Series with or without similar column with the inclusion of `join = `
#     2. can be used to join two DataFrames either vertially or horizontally with `axis = 1`


# + [markdown] magic_args="[markdown]"
# ## Example 1 
# join two dataframe horizontaly and vertially
# -


import pandas as pd 
from IPython.display import display

dic1 = {'Name': ['Allen', 'Bill','Charle','David','Ellen'],
      'number':[1,2,3,4,5],
      'letter':['a','b','c','d','e']}
dic2 = {'A':['a','a','a','a','a'],
       'B':['b','b','b','b','b'],
       'number':[10,11,12,13,14]}
df1 = pd.DataFrame(dic1)
df2 = pd.DataFrame(dic2)
display(df1)
display(df2)

# + [markdown] magic_args="[markdown]"
# join vertially 
# -


df = pd.concat([df1,df2])
display(df)

# + [markdown] magic_args="[markdown]"
# join horizontally 
# -


df = pd.concat([df1,df2],axis =1 )
display(df)

# + [markdown] magic_args="[markdown]"
# ## Example 2 
# join with the common column
#
# -


df = pd.concat([df1,df2],join='inner')
display(df)

# + [markdown] magic_args="[markdown]"
# ## Windowing Operations
# **Mengtong Hu- mengtong@umich.edu**

# + [markdown] magic_args="[markdown]"
# - an operation that perfroms an aggregation over a sliding
#   partition of values on Series or DataFrame, similar to `groubby`.

# + [markdown] magic_args="[markdown]"
# ### Windowing Operations

# + [markdown] magic_args="[markdown]"
# - Specify the window=n argument in `.rolling()` for the window size. 
# - After specifiying the window size, apply the appropriate
#   statistical function on top of it. Examples of statistical
#   functions include: `.sum()`, `.mean()`, `.median()`, `.var()`, `.corr()`.
# - If the offest is based on a time based column such as 'window = "2D"', the correspond
#     time based index must be monotonic.
# - The example below computes the sum of 'A' for previous 2 days
# -


df = pd.DataFrame(np.arange(10),
   index = pd.date_range('1/1/2000', periods=10),
   columns = ['A'])
df['default sum'] = df['A'].rolling(window=3).sum()
df

# + [markdown] magic_args="[markdown]"
# ### Windowing Operations
# - The closed parameter in `.rolling()` is used to decide the inclusions
#     of the interval endpoints in rolling window 
#     - 'right' close right endpoint
#     - 'left' close left endpoint
#     - 'both' close both endpoints
#     - 'neither' open endpoints
# -


offset = '2D'
df["right"] = df.rolling(offset, closed="right").A.sum()  # default
df["both"] = df.rolling(offset, closed="both").A.sum()
df["left"] = df.rolling(offset, closed="left").A.sum()
df["neither"] = df.rolling(offset, closed="neither").A.sum()
df

# + [markdown] magic_args="[markdown]"
# ### Windowing Operations
# - `.apply()` function takes an extra func argument and performs self-defined rolling computations.

# + [markdown] magic_args="[markdown]"
# ## **Name**  : *Xin Luo*
# ## **EMAIL**  :  *luosanj@umich.edu*
# -
# #  Question 0
#
# ##  Pandas .interpolate() method
#
# * Method *interpolate* is very useful to fill NaN values.
# * By default, NaN values can be filled by other values with the same index for different methods.
# * Please note that NaN values in DataFrame/Series with MultiIndex can be filled by 'linear' method as
# <code>method = 'linear' </code>. 

import pandas as pd
import numpy as np
a = pd.DataFrame({'a' : [1, 2, np.nan, 5], 'b' : [4, np.nan, 6, 8]})
a.interpolate(method = 'linear')


# ### Parameters in .interpolate()
# ##### *parameter **'method'** : *str*, default *'linear'
#
#
# * Most commonly used methods:
#     * 1. **'linear'** : linear regression mind to fit the missing ones.
#     * 2. **'pad', 'limit'** :  Fill in NaNs using existing values. Note:Interpolation through padding means copying the value just before a missing entry.While using padding interpolation, you need to specify a limit. The limit is the maximum number of nans the method can fill consecutively.
#     * 3. **'polynomial', 'order'** : Polynomial regression mind with a set order to fit the missing ones. Note : NaN of the first column remains, because there is no entry before it to use for interpolation.

m =  pd.Series([0, 1, np.nan, np.nan, 3, 5, 8])
m.interpolate(method = 'pad', limit = 2)

n = pd.Series([10, 2, np.nan, 4, np.nan, 3, 2, 6]) 
n.interpolate(method = 'polynomial', order = 2)


# ##### parameter **'axis'** :  default *None*
# * 1. axis = 0 : Axis to interpolate along is index.
# * 2. axis = 1 : Axis to interpolate along is column.
#     

k = pd.DataFrame({'a' : [1, 2, np.nan, 5], 'b' : [4, np.nan, 6, 8]})
k.interpolate(method = 'linear', axis = 0)
k.interpolate(method = 'linear', axis = 1)


# ###  Returns
# * Series or DataFrame or None
# * Returns the same object type as the caller, interpolated at some or all NaN values or None if `inplace=True`.

# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
#
# + [DateTime in Pandas](#DateTime-in-Pandas) 
# + [Create DatetimeIndex](#Create-DatetimeIndex) 
# + [Convert from other types](#Convert-from-other-types) 
# + [Indexing with DatetimeIndex](#Indexing-with-DatetimeIndex) 
# + [Date/time components in the DatetimeIndex](#Date/time-components-in-the-DatetimeIndex) 
# + [Operations on Datetime](#Operations-on-Datetime) 

# ## DateTime in Pandas
#
# *Qi, Bingnan*
# bingnanq@umich.edu
#
# - Pandas contains a collection of functions and features to deal with time series data. A most commonly used class is `DatetimeIndex`.
#

# ## Create DatetimeIndex
#
# - A `DatetimeIndex` array can be created using `pd.date_range()` function. The `start` and `end` parameter can control the start and end of the range and `freq` can be `D` (day), `M` (month), `H` (hour) and other common frequencies.

pd.date_range(start='2020-01-01', end='2020-01-05', freq='D')

pd.date_range(start='2020-01-01', end='2021-01-01', freq='2M')


# ## Convert from other types
#
# - Other list-like objects like strings can also be easily converted to a pandas `DatetimeIndex` using `to_datetime` function. This function can infer the format of the string and convert automatically.

pd.to_datetime(["2020-01-01", "2020-01-03", "2020-01-05"])


# - A `format` keyword argument can be passed to ensure specific parsing.

pd.to_datetime(["2020/01/01", "2020/01/03", "2020/01/05"], format="%Y/%m/%d")


# ## Indexing with DatetimeIndex
#
# - One of the main advantage of using the `DatetimeIndex` is to make index a time series a lot easier. For example, we can use common date string to directly index a part of the time series.

idx = pd.date_range('2000-01-01', '2021-12-31', freq="M")
ts = pd.Series(np.random.randn(len(idx)), index=idx)

ts['2018-09':'2019-04']

ts['2021-6':]


# ## Date/time components in the DatetimeIndex
#
# - The properties of a date, e.g. `year`, `month`, `day_of_week`, `is_month_end` can be easily obtained from the `DatetimeIndex`.

idx.isocalendar()


# ## Operations on Datetime
#
# - We can shift a DatetimeIndex by adding or substracting a `DateOffset`

idx[:5] + pd.offsets.Day(2)

idx[:5] + pd.offsets.Minute(1)

get_ipython().system('/usr/bin/env python')
# coding: utf-8


# ### youngwoo Kwon
#
# kedwaty@umich.edu

# # Question 0 - Topics in Pandas

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import time


# ## Missing Data in Pandas 
#
# Pandas is very __flexible__ to the missing values
#
# * NaN is the default missing value
#
# * However, we should deal with the different types such as integer, boolean, or general object.
#
# * We should also consider that "missing" or "not available" or "NA".

# ## Detecting the Missing Values
#
# * Pandas provides `isna()` and `notna()` function to detect the missing values

df = pd.DataFrame(
    np.random.randn(4, 3),
    index=["a", "c", "e", "f"],
    columns=["one", "two", "three"],
)
df["five"] = df["one"] < 0
df2 = df.reindex(["a", "b", "c", "d", "e"])
df2

df2.isna()

df2.notna()


# ## More about the Missing Values
#
# * In Python, nan's don't compare equal, but None's do.
#
# * NaN is a float, but pandas provides a nullable integer array

None == None

np.nan == np.nan

print(df2.iloc[1,1])
print(type(df2.iloc[1,1]))

pd.Series([1, 2, np.nan, 4], dtype=pd.Int64Dtype())


# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   

# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Introduction to Python Idioms](https://github.com/boyazh/Stats507/blob/main/pandas_notes/pd_topic_boyazh.py) 
# + [Topic 2 Title](#Topic-2-Title)

# ## Topic Title
# Python Idioms
# **Boya Zhang**

get_ipython().system('/usr/bin/env python')
# coding: utf-8

# # Question 0

# ## Introduction to Python Idioms  
#   
# Boya Zhang (boyazh@umich.edu)  
#
# 10.16.21
#

# ## Overview  
#   
# 1. if-then/if-then-else
# 2. splitting
# 3. building criteria

# ## 1. if-then/ if-then-else 
#
# 1.1 You can use if-then to select specific elements on one column, and add assignments to another one or more columns: 
#         

import pandas as pd
df = pd.DataFrame({"A": [1, 3, 5, 7, 9], "B": [10, 20, 30, 40, 50], "C": [100, 200, 300, 400, 500]})
df


# * To assign to one or more column:

df.loc[df.A > 5, 'B'] = '> 5'
df


# * or

df.loc[df.A > 5, ['B','C']] = '> 5'
df


# * You can add another line with different logic, to do the ”-else“

df.loc[df.A <= 5, ['B','C']] = '< 5'
df


# 1.2 You can also apply "if-then-else" using Numpy's where( ) function

import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 3, 5, 7, 9], "B": [10, 20, 30, 40, 50], "C": [100, 200, 300, 400, 500]})
df['new'] = np.where(df['A'] > 5, '> 5', '< 5')
df


# ## 2. Splitting a frame with a boolean criterion

# You can split a data frame with a boolean criterion

import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 3, 5, 7, 9], "B": [10, 20, 30, 40, 50], "C": [100, 200, 300, 400, 500]})
df

df[df['A'] > 5]

df[df['A'] <= 5]


# ## 3. Building criteria 
# You can build your own selection criteria using "**and**" or "**or**".  
#
# 3.1 "... and"

import numpy as np
import pandas as pd

df = pd.DataFrame({"A": [1, 3, 5, 7, 9], "B": [10, 20, 30, 40, 50], "C": [100, 200, 300, 400, 500]})
df


# * ...and

df.loc[(df["B"] < 25) & (df["C"] >= 20), "A"]


# * ...or

df.loc[(df["B"] < 25) | (df["C"] >= 40), "A"]


# * you can also assign new value to a existing column using this method

df.loc[(df["B"] > 40) | (df["C"] >= 300), "A"] = 'new'
df


# ## Takeaways  
# There are a few python idioms that can help speeding up your data managemet.  
# * "if-then-else" allows you easily change the current column or add additional new columns based on the value of a specific column
# * "Splitting" allows you quickly select specific rows based on the value of a specific column
# * "Building criteria" allows you select specific data from one column or assign new values to one column based on the criteria you set up on other columns

# ## Topic Title
# Python Idioms
# **Xi Zheng**

# ## 1. pandas.Series.ne
#  * Return Not equal to of series and other, element-wise (binary operator ne).
#  * `Series.ne(other, level=None, fill_value=None, axis=0)`
#  - Parameters:  
#      - otherSeries or scalar value
#      - fill_valueNone or float value, default None (NaN)
#      - levelint or name
#      - Returns: series
#
# ## 2. Code Example
# ```python
# a = pd.Series([1, 1, 1, np.nan], index=['a', 'b', 'c', 'd'])
# b = pd.Series([1, np.nan, 1, np.nan], index=['a', 'b', 'd', 'e'])
# a.ne(b, fill_value=0)
# ```
# ## 3. Ouput and Explanation
# ```
# a :
#
# a    1.0
# b    1.0
# c    1.0
# d    NaN
# ```
#
# ```
# b: 
#
# a    1.0
# b    NaN
# d    1.0
# e    NaN
# ```
#
# ```
# a    False
# b     True
# c     True
# d     True
# e     True
# ```
# ## Takeaways
# The function tells the equivalence of corresponding elements in a and b, where the 'True' means 'not equal', and 'False' means 'equal'.

# # Topics in Pandas
#
# ## Sparse Data Structures
#
# #### Author: Chittaranjan (chitt@umich.edu)

# imports
import pandas as pd
import numpy as np


# ### Sparse Data Structures
# - Pandas provides a way of efficiently storing "sparse" data structures
# - A sparse data structure is one in which a majority of the values are
# omitted (to be interpreted as 0, or NaN, or any other value)
# - It can be thought of as a "compressed" representation, as all values are
# not explicitly stored in the data structure

# ### Creating a Sparse Data Frame
# - Sparse data frames can be created using `pd.arrays.SparseArray`
# - Has a dtype of `Sparse` which has two values associated with it,
#     - Type of non-omitted values (Eg: float, int etc)
#     - Value of the elements in the array that aren't actually stored
# (Eg: 0, nan)
#

s = pd.Series(pd.arrays.SparseArray([1] * 2 + [np.nan] * 8))
s


# `Sparse[float64, nan]` indicates that all values apart from `nan` are stored,
#  and they are of type float.

# ### Memory Efficiency
# - The `memory_usage` function can be used to inspect the number of bytes
# being consumed by the Series/DataFrame
# - Comparing memory usage between a SparseArray and a regular python list
# represented as a Series depicts the memory efficiency of SparseArrays

N = 1000  # number of elements to be represented

proportions = list(range(100, N+1, 100))
sparse_mems = []
non_sparse_mems = []
for proportion in proportions:
    sample_list = [14] * proportion + [np.nan] * (N - proportion)
    sparse_arr = pd.Series(
        pd.arrays.SparseArray(sample_list)
    )
    sparse_mem = sparse_arr.memory_usage()
    sparse_mems.append(sparse_mem)

    non_sparse_arr = pd.Series(sample_list)
    non_sparse_mem = non_sparse_arr.memory_usage()
    non_sparse_mems.append(non_sparse_mem)

x = list(map(lambda p: p / N, proportions))
_ = plt.plot(x, non_sparse_mems)
_ = plt.plot(x, sparse_mems)
_ = plt.ylabel("Memory Usage (bytes)")
_ = plt.xlabel("Proportion of values")
_ = plt.legend(["Non-Sparse", "Sparse"])
_ = plt.title("Comparison of Memory Usage (Size=1000)")


# ### Memory Efficiency (Continued)
# - The Sparse Arrays consume much less memory when the density is low
# (sparse-ness is high)
# - As the density increases to where 50-60% of the values are not nan
# (i.e ommittable), memory efficiency is worse

# ## Pivot Table

# **Stats 507, Fall 2021**

# **Xuechun Wang** <br>
# **24107190** <br>
# **xuechunw@umich.edu** <br>

# ## How Pivot table works

# - Pivot table is a table of grouped value that aggregates individual items of a more extensive table.
#  - The aggregations can be count, sum, mean, stats tool etc.
#  - Levels can be stored as multiIndex objects and columns of the result DataFrame.
#  - It arrange or rearrange data to provide a more direct insight into datasets
#  - **pd.pivot_table(data, values = None, index = None, aggfunc = 'mean'...)** can take more parameters
#  - Requires data and index parameter, data is the dataFrame passed into the function, index allow us to group the data 

#import packages
import pandas as pd
import numpy as np

#import used dataset as example
recs2015 = pd.read_csv("https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv")

#Pivot table can take single or multiple indexes via a list to see how data is grouped by
pd.pivot_table(recs2015, index = ['REGIONC','DOEID'])


# ### Pivot table: mean and sum calculation
#  - Apply different aggregation function for different feature
#  - We can calculate mean of NWEIGHT and sum of CDD65 after groupbying regions

pd.pivot_table(recs2015, index = 'REGIONC',aggfunc={'NWEIGHT':np.mean,'CDD65':np.sum, 'HDD65':np.sum})


# ### Pivot table: aggfunc functionality
#  - Aggregate on specific features with values parameter
#  - Meanwhile, can use mulitple aggfunc via a list

pd.pivot_table(recs2015, index = 'REGIONC', values = 'NWEIGHT', aggfunc = [np.mean, len])


# ### Pivot table: find how data is correlated
#  - Find relationship between feature with columns parameter
#  - UATYP10 - A categorical data type representing census 2010 urban type
#  -         U: Urban Area; R: Rural; C: Urban Cluster

pd.pivot_table(recs2015,index='REGIONC',columns='UATYP10',values='NWEIGHT',aggfunc=np.sum)


# ## Takeaways

#  - Pivot Table is beneficial when we want to have a deep investigation on the dataset. <br>
#  - Especially when we want to find out where we can explore more from the dataset. <br>
#  - Meanwhile, the aggfunc it involves effectively minimizes our work. <br>