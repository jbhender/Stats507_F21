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
import matplotlib.pylab as pylab
import statsmodels.api as sm
import statsmodels.formula.api as smf
from collections import defaultdict
from sklearn.linear_model import LogisticRegression
from scipy.stats import logistic
from os.path import exists
from patsy import dmatrices

# figure options: -----------------------------------------------------------
params = {'legend.fontsize': 'large',
         'axes.labelsize': 'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large',
         'axes.titlesize': 'x-large'}
pylab.rcParams.update(params)

# ## The Isolet Data 
# The data for this demonstration comes from the UCI Machine Learning
# repository. There are 5 waves of data with the first 4 used for training 
# and the $5^{th}$ for testing.

# data: ---------------------------------------------------------------------
iso_train_file = 'isolet_train.feather'
cols = ['x' + str(i) for i in range(616)] + ['letter']
if exists(iso_train_file):
    df_train = pd.read_feather(iso_train_file)
else:
    # use delimited data
    iso_train = 'isolet1+2+3+4.data'
    df_train = pd.read_csv(iso_train, delimiter=',', header=None)
    # add column names
    cols = ['x' + str(i) for i in range(617)] + ['letter']
    df_train.columns = cols
    # save 
    df_train.to_feather(iso_train_file)

# ## Subjects 
# From the information file, we know that each person in the study was 
# recorded speaking each letter twice.  In the first two subsets, the
# letters are back to back; in the second two the full alphabet is completed
# twice in order.  We assume in these latter two that back to back alphabets
# come from the same subject.  Here we construct subjects ids using this 
# information.

# construct "ids" for the 30 subjects: ----------------------------------------
df_train['a'] = df_train['letter'] == 1
df_train['z'] = df_train['letter'] == 26
n, p = df_train.shape
id = np.cumsum(
    df_train['a'].iloc[1:, ].values * 
    df_train['z'].iloc[0:(n - 1), ].values
)
# the 3rd and 4th blocks are organized differently
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

# +
# construct folds: -----------------------------------------------------------
df_train['fold'] = (df_train['id'] - 1) // 30
df_train.groupby('fold').size()

# folds as array indices
folds = []
n = df_train.shape[0]
rows = np.arange(n)
for fold in range(4):
    train = np.asarray(df_train['fold'] != fold).nonzero()[0]
    test = np.asarray(df_train['fold'] == fold).nonzero()[0]
    folds.append((train, test))
# -

# ## Label the vowels  
# We'll start off by building models with the goal of distinguishing vowels
# from consonants rather than trying to identify individual models. We'll
# come back to the latter task later. 

# label vowels: --------------------------------------------------------------
df_train['vowel'] = 1
df_train['vowel'].where(
    np.in1d(df_train['letter'], [1, 5, 9, 15, 21]),
    0,
    inplace=True
)

# ## Principle Component Regression
# Our first set of models will use the singular value decomposition to 
# construct a set of orthogonal features. We'll use cross validation to
# compare the performance of models retaining different numbers of singular-
# vectors.  
#
# To avoid information leakage, we should perform all steps on each subset
# of the training data used to learn the models - this includes normalization
# constants.  We'll base the number of components on the proportion of 
# explained variance.  

# extract data to numpy: ------------------------------------------------------
x_train = df_train.loc[:, 'x0':'x616'].to_numpy()
y_train = df_train.loc[:, 'vowel'].to_numpy()
n, p = x_train.shape
# center and scale the data: --------------------------------------------------
x_all = x_train.copy()
x_all = (x_all - np.mean(x_all, axis=0)) / np.std(x_all, axis=0)

# singular value decomposition: -----------------------------------------------
svd = np.linalg.svd(x_all)
s = svd[1]
pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
ax = plt.scatter(x=range(len(s)), y=pct_var)
pct_var[:5]

# cross validation for determining the number of components: ------------------
metrics = defaultdict(list)
for fold, (train, val) in enumerate(folds):
    # training data
    x_in = x_train[train, :]
    y_in = y_train[train]
    n, p = x_in.shape
    
    # validation data
    x_v = x_train[val, :]
    y_v = y_train[val]
    
    # normalize training folds
    xbar = np.mean(x_in, axis=0)
    sd = np.std(x_in, axis=0)
    x_in = (x_in - xbar) / sd
    
    # normalize validation
    x_v = (x_v - xbar) / sd
    
    # svd
    svd = np.linalg.svd(x_in)
    s = svd[1]
    x_svd = sm.add_constant(svd[0])
    
    # project x_v onto singular vectors
    v_svd = sm.add_constant(np.dot(x_v, svd[2].T) * 1 / svd[1])

    # cumulative variance thresholds
    pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
    n_pc = (
        2 + np.arange(p)[np.cumsum(pct_var) > 0.8][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.9][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.95][0]
    ) 
    pcts = (0.8, 0.9, 0.95)
    
    for i, npc in enumerate(n_pc):
        # track current 
        metrics['fold'].append(fold)
        metrics['pct_var'].append(pcts[i])
        metrics['npc'].append(npc)

        # train model
        mod = sm.Logit(y_in, x_svd[:, :npc])
        res = mod.fit(disp=False)
        
        # record training fit
        metrics['ce_train'].append(-1 * res.llf / n)
        
        # make predictions on validation data
        lp = np.dot(v_svd[:, :npc], res.params)
        y_hat = logistic.cdf(lp)
        
        # evaluate predictions
        metrics['ce_val'].append(
            np.mean(
                -1 * y_v * np.log(y_hat) - (1 - y_v) * np.log(1 - y_hat)
            )
        )

        metrics['accuracy'].append(
            np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v))
        )
        metrics['n'].append(len(y_v))
        print((fold, pcts[i]))

metrics2 = pd.DataFrame(metrics)
metrics2.groupby('pct_var').mean()

ax2 = (
    metrics2
     .groupby('pct_var')[['ce_train', 'ce_val']]
     .mean()
     .plot
     .line()
    )

# Let's repeat the previous example using the logistic regression estimator
# from sklearn.  First, let's investigate its interface.

mod1 = LogisticRegression(
    penalty='none',
    fit_intercept=False,
    max_iter=10000,
    solver='saga'
)
res1 = mod1.fit(x_svd[:, :npc], y_in)

[res1.coef_.shape, res.params.shape]

np.array([res1.coef_[0, 0:10], res.params[0:10]]).T

yhat2 = res1.predict_proba(v_svd[:, :npc])
np.array(
    [np.round(yhat2, 3)[0:10, 1], np.round(y_hat[0:10], 3)]
).T


# We'll cotinue with an expanded version of this demo on November 9.
