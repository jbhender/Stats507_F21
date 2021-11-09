# # Isolet Demo
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *November 4, 2021*


# ## About
# This is a [SciKit Learn][skl] demonstration using the [isolet][iso]
# data with labeled vocalizations of features extracted from recordings
# of people speaking single English letters.
#
# [skl]: https://scikit-learn.org/
# [iso]: https://archive.ics.uci.edu/ml/machine-learning-databases/isolet/

# ## Imports
# We'll make use of the following imports.   

# libraries: ----------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from collections import defaultdict
from sklearn.linear_model import LogisticRegression, lasso_path, enet_path
from sklearn.svm import l1_min_c
from os.path import exists

import sklearn as skl
skl.__version__

 from patsy import dmatrices

# ## The Isolet Data 
# The data for this demonstration comes from the UCI Machine Learning repository.  
# There are 5 waves of data with the first 4 used for training and the $5^{th}$ for
# testing.

# +
# data: ---------------------------------------------------------------------
iso_train_file = 'isolet_train.feather'
#url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/isolet/'
cols = ['x' + str(i) for i in range(616)] + ['letter']
if exists(iso_train_file + 'x'):
    df_train = pd.read_feather(iso_train_file)
else:
    # download data
    iso_train = 'isolet1+2+3+4.data'
    df_train = pd.read_csv(iso_train, delimiter=',', header=None)
    # add column names
    cols = ['x' + str(i) for i in range(617)] + ['letter']
    df_train.columns = cols
    # save 
    df_train.to_feather(iso_train_file)
    

#
# -

df_train.iloc[:10, 610:].dtypes


# construct "ids" for the 30 subjects
df_train['a'] = df_train['letter'] == 1
df_train['z'] = df_train['letter'] == 26
n, p = df_train.shape
id = np.cumsum(
    df_train['a'].iloc[1:, ].values * 
    df_train['z'].iloc[0:(n - 1), ].values
)
# the 3rd and 4th blocks are ogranized differently
id2 = 59 + (np.array(id) - 59 + 1) // 2
id = np.where(id > 59, id2 , id)
id = [1] + list(1 + id)
df_train['id'] = id


# ## Construct Folds
# Next we divide the data into folds for cross-validation.
# We'll use 4-fold cross-validation for simplicity. It's important
# that we put all the data from a given "id" into the same fold. 
# Failing to do so risks information "leakage" - it's easier to 
# teach a model to recognize vowels from the same set of speakers 
# than a new set of speakers.

# construct folds: ----------------------------------------------------------
df_train['fold'] = (df_train['id'] - 1) // 30

df_train.groupby('fold').size()

df_train['vowel'] = 1
df_train['vowel'].where(
    np.in1d(df_train['letter'], [1, 5, 9, 15, 21]),
    0,
    inplace=True
)

# +
# sklearn logistic regression model
lr1 = LogisticRegression(penalty='elasticnet', l1_ratio=0, max_iter=200, C=0.01, solver='saga')
loss = defaultdict(list)
# cross validation for unregularized regression
for fold in range(4):
    # hold-out fold and rest
    df_learn = df_train.query('fold != @fold')
    df_val = df_train.query('fold == @fold')
    
    # fit model to all but the hold-out fold
    X = df_learn.loc[:, 'x0':'x616'].to_numpy()
    y = df_learn['vowel'].to_numpy()
    s = np.std(X, axis=0)
    X /= s
    res = lr1.fit(X, y)
    # predictions and evaluation metrics
    Xv = df_val.loc[:, 'x0':'x616'].to_numpy() / s
    yv = df_val['vowel'].to_numpy()
    yhat = res.predict_proba(Xv)[:, 1]
    loss['fold'].append(fold)
    loss['entropy'].append(
        np.mean(
            -1 * yv * np.log(yhat) - (1 - yv) * np.log(1 - yhat)
        )
    )
    loss['accuracy'].append(np.mean(np.where(yhat > 0.5, yv, 1 - yv)))
    loss['n'].append(len(yv))

loss1 = pd.DataFrame(loss)
loss1

# +
#cs = l1_min_c(X, y, loss="log") * np.logspace(0, 7, 16)
#np.logspace(0, 7, 16)
# sklearn logistic regression model
lr2 = LogisticRegression(penalty='elasticnet', l1_ratio=1, max_iter=2000, C=0.00001, solver='saga')
loss = defaultdict(list)
# cross validation for unregularized regression
for fold in range(4):
    # hold-out fold and rest
    df_learn = df_train.query('fold != @fold')
    df_val = df_train.query('fold == @fold')
    
    # fit model to all but the hold-out fold
    X = df_learn.loc[:, 'x0':'x616'].to_numpy()
    y = df_learn['vowel'].to_numpy()
    s = np.std(X, axis=0)
    X /= s
    res = lr2.fit(X, y)
    # predictions and evaluation metrics
    Xv = df_val.loc[:, 'x0':'x616'].to_numpy() / s
    yv = df_val['vowel'].to_numpy()
    yhat = res.predict_proba(Xv)[:, 1]
    loss['fold'].append(fold)
    loss['entropy'].append(
        np.mean(
            -1 * yv * np.log(yhat) - (1 - yv) * np.log(1 - yhat)
        )
    )
    loss['accuracy'].append(np.mean(np.where(yhat > 0.5, yv, 1 - yv)))
    loss['n'].append(len(yv))

loss2 = pd.DataFrame(loss)
loss2
# -

pd.merge(loss1, loss2, on=['fold', 'n']).mean()

folds = []
n = df_train.shape[0]
rows = np.arange(n)
for fold in range(4):
    train = np.asarray(df_train['fold'] != fold).nonzero()[0]
    test = np.asarray(df_train['fold'] == fold).nonzero()[0]
    folds.append((train, test))

X = df_train.loc[:, 'x0':'x616'].to_numpy()
y = df_train.loc[:, 'vowel'].to_numpy()
alphas_lasso, coefs_lasso, _ = lasso_path(X, y, max_iter=1000, eps=0.001)


# +
f_all = 'vowel ~ '
for f in range(616):
    f_all += 'x' + str(f) + ' + '
f_all = f_all + 'x616'
#mod0 = sm.dm(f_all, data=df_train)
df_train.loc[:, 'x0':'x616'] = (
    (df_train.loc[:, 'x0':'x616'] - df_train.loc[:, 'x0':'x616'].mean()) /
    df_train.loc[:, 'x0':'x616'].std()
)
    

y, x = dmatrices(f_all, data=df_train)
# -

#pca = sm.multivariate.PCA(x, demean=True)
svd = np.linalg.svd(x[:, 1:])

#[i.shape for i in svd]
s = svd[1]
pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
plt.scatter(x=range(len(s)), y=pct_var)

p = len(pct_var)
n_vars = (
    np.arange(p)[np.cumsum(pct_var) > 0.8][0],
    np.arange(p)[np.cumsum(pct_var) > 0.9][0],
    np.arange(p)[np.cumsum(pct_var) > 0.95][0]
)
    

for i, (j, k) in enumerate([(10, 20), (30, 40)]):
    print((i, j, k))

folds

for nv in n_vars:
    for train, val in folds:
        # train the model
        x_train = svd[0][train, :nv]
        y_train = y[train]
        mod = sm.Logit(y_train, x_train)
        res = mod.fit()
        
        # make predictions on validation data
        x_val = svd[0][val, :nv]
        lp = np.dot(x_val, res.params())
        y_hat = 1 / (1 +  np.exp(-1 * lp))
        
        # evaluate predictions
        y_val = y[val]
    loss['fold'].append(fold)
    loss['entropy'].append(
        np.mean(
            -1 * yv * np.log(yhat) - (1 - yv) * np.log(1 - yhat)
        )
    )
    loss['accuracy'].append(np.mean(np.where(yhat > 0.5, yv, 1 - yv)))
    loss['n'].append(len(yv))


# +
loss = defaultdict(list)
# cross validation for unregularized regression
for fold in range(4):
    # hold-out fold and rest
    df_learn = df_train.query('fold != @fold')
    df_val = df_train.query('fold == @fold')
    
    # fit model to all but the hold-out fold
    X, y = df_learn.loc[:, 'x0':'x616'], df_learn['vowel']
    Xv, yv = df_val.loc[:, 'x0':'x616'], df_val['vowel']
 
    # fit model to all but the hold-out fold
    mod0 = sm.Logit(y, X)
    res0 = mod0.fit()
    mod1 = sm.Logit(yv, Xv)
    yhat = 1 / (1 + np.exp(-1 * mod1.predict(res0.params)))
    
    loss['fold'].append(fold)
    loss['entropy'].append(yv * np.log(yhat) - (1 - yv) * np.log(1 - yhat))
    loss['accuracy'].append(np.mean(np.where(yhat > 0.5, yv.values, 1 - yv.values)))
    loss['n'].append(len(yv))

pd.DataFrame(loss)
# -




mod1.exog.shape

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

skl.lin

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

