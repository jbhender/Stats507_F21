# # Billboard Demo
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *September 30, 2021*


# ## About
# This is a pandas demonstration using the [billboard][bd] data on songs
# in Billboard's US Top 100 from the year 2000. In this demontration we'll 
# make use of DataFrame methods we've been discussing as well as the
# plotting interface from pandas.  
#
# [bd]: https://tidyr.tidyverse.org/reference/billboard.html

# ## Imports
# We'll make use of the following imports.   

# libraries: ----------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os.path import exists

# ## The Billboard Data 
# The data for this demonstration comes from the R package `tidyr`. In the 
# code chunk below we check if the data is already available in a local file
# `billboard.csv`. If not, we download it from the tidyr GitHub repo. 

# data: ---------------------------------------------------------------------
bb_file = 'billboard.csv'
if exists(bb_file):
    df = pd.read_csv('billboard.csv')
else:
    df = pd.read_csv(
        'https://github.com/tidyverse/tidyr/raw/master/data-raw/billboard.csv'
    )
    df.to_csv(bb_file)
df.head()

# ## Tidy Up
# In the next chunk, we make the data tidy by melting to a longer format
# and removing weeks where each song is out of the top 100. Then we clean up 
# some columns and data types. 

# make the data longer: -----------------------------------------------------
df_long = (
    df.melt(
      id_vars=['artist', 'track', 'date.entered'],
      value_vars=['wk' + str(i) for i in range(1, 77)],
      var_name='week',
      value_name='position')
    .dropna()
    )
df_long.head()

# clean up columns: ----------------------------------------------------------
df_long['position'] = pd.to_numeric(df_long['position'], downcast='integer')
df_long['week'] = df_long['week'].str.replace('wk', '')
df_long['artist'] = pd.Categorical(df_long['artist'])
df_long.head()

# ## Number 1 Hits
# In this section we create some facts about songs that reached position 1.
# Some facts we'll create more than once to illusrate different functionality. 
#
# In creating `wks_at1` below, we need to use `observed=False` because "artist"
# is of type `pd.Categorical`. When one or more of the grouping variables are 
# categorical and `observed=True` (the default) the result uses unique 
# combinations of the categories -- not just those observed in the data. 

# count # of weeks at 1: -----------------------------------------------------
# weeks at number 1
wks_at1 = (df_long
           .query('position == 1')
           .groupby(by=['artist', 'track'], observed=True, as_index=False)
           .size()
           .query('size > 0')
           .sort_values('size', ascending=False)
           )
wks_at1


wks_at1b = (
  df_long
  .groupby(by=['artist', 'track'], observed=False)['position']
  .agg([('n', lambda x: np.sum(x == 1))])
  .query('n > 0')
  .sort_values('n', ascending=False)
)
wks_at1b

# Next, let's identify all songs that hit number 1 at any point and keep all 
# the associated data for those songs.

# keep all info for any song that hits number 1: -----------------------------
df_long['num1'] = (
    df_long
    .groupby(
        by=['artist', 'track'],
        observed=False,
        as_index=False
    )[['position']]
    .transform(lambda x: np.any(x == 1))
)
df_long.head()

# re-merge approach
wks_at1[['num1_rm']] = True
num1 = pd.merge(df_long, wks_at1, how='left', on=['artist', 'track'])
num1['num1_rm'].replace({np.nan: False}, inplace=True)
num1.head()

# ## Pandas "Chart Visualization"
# In this section we'll create a visualization of the Billboard position of
# the songs that hit number 1 in 2000. To "get our feet wet", we'll make a 
# plot for a single song.

# line plot for a given track
ax1 =(
    df_long
    .query('track == "Kryptonite"')
    .plot
    .line(
        x='week',
        y='position',
        xlabel='Weeks from Entry',
        ylabel='Chart Position',
        label='Kryptonite'
    )
)
ax1.invert_yaxis()

# ### Creating Dates
# Pandas has nice support for working with and plotting dates. Here, we'll
# convert the weeks since the song entered the Billboard chart into a date for
# use in our next visualization.


# use `date.entered` and `week` to create a date variable: --------------------
num1['week'] = pd.to_numeric(num1['week'])
num1['days'] = pd.Timedelta('7 days') * (num1['week'] - 1)
num1['date'] = pd.to_datetime(num1['date.entered']) + num1['days']

# alternate version
num1['date2'] = (
    pd.to_datetime(num1['date.entered']) +
    pd.Series(pd.Timedelta('7 days') * (num1['week'] - 1))
    )
num1.head()

# ### Facets
# We'll use subplots or "facets" to limit the number of lines appearing on a
# single set of axes.


# split into longer and shorter lived stays at top position: ------------------
num1_wide_a = (num1
               .query('size > 2')
               .pivot(index='date', columns='track', values=['position'])
               )
num1_wide_b = (num1
               .query('size <= 2')
               .pivot(index='date', columns='track', values=['position'])
               )
num1_wide_a.head()

# ### Visual
# In the chart that follows, we show the history of all of the songs that 
# reached number 1 in 2000. In the process we make use of a number of 
# customizations.  

# +
# figure 2: -------------------------------------------------------------------
# set up the figure
fig2, ax2 = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
_ = fig2.tight_layout()
_ = fig2.set_size_inches(16, 12)
# extend limits to create space for the legends
xl = pd.to_datetime(('1999-01-01', '2001-04-01'))
# top axes
num1_wide_a.plot.line(
    ax=ax2[0], y='position', xlim=xl, colormap='tab20', ls='-', lw=4
)
# add a dashed black line for the weeks at 1
num1_wide_a.where(lambda x: x == 1).plot.line(
    ax=ax2[0], y='position', color='black', ls='--', lw=2
)
# bottom axes
num1_wide_b.plot.line(ax=ax2[1], y='position', colormap='tab20', lw=4)
num1_wide_b.where(lambda x: x == 1).plot.line(
    ax=ax2[1], y='position', color='black', ls='--', lw=2
)

# "higher" on the chart (lower position) is better 
ax2[0].invert_yaxis()
# legends
_ = ax2[0].legend([j for i, j in num1_wide_a.columns], loc='center left')
_ = ax2[1].legend([j for i, j in num1_wide_b.columns], loc='center left')
_ = ax2[0].set_xlim(xl[0], xl[1])
# titles
_ = ax2[0].set_title('3 or more weeks at #1')
_ = ax2[1].set_title('1 or 2 weeks at # 1')

