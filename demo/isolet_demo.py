# # Isolet Demo
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *November 4-11, 2021*


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
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
import sklearn as skl
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
# and the $5^{th}$ for testing. See here for the source: 
# https://archive.ics.uci.edu/ml/machine-learning-databases/isolet/

# +
# data: ---------------------------------------------------------------------

# training
iso_train_file = 'isolet_train.feather'
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

# -

# testing
iso_test_file = 'isolet_test.feather'
if exists(iso_test_file):
    df_test = pd.read_readfeather(iso_test_file)
else: 
    iso_test = 'isolet5.data'
    df_test = pd.read_csv(iso_test, delimiter=',', header=None)
    # add column names
    cols = ['x' + str(i) for i in range(617)] + ['letter']
    df_test.columns = cols

# ## Subjects 
# From the information file, we know that each person in the study was 
# recorded speaking each letter twice.  In the first two subsets, the
# letters are back to back; in the second two the full alphabet is completed
# twice in order.  We assume in these latter two that back to back alphabets
# come from the same subject.  Here we construct subjects ids using this 
# information.

# construct "ids" for the 30*4 subjects: --------------------------------------
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
print(df_train.groupby('fold').size())

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
df_train['vowel'] = 0
df_train['vowel'].where(
    np.in1d(df_train['letter'], [1, 5, 9, 15, 21]),
    1,
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

# +
# extract data to numpy: ------------------------------------------------------
x_train = df_train.loc[:, 'x0':'x616'].to_numpy()
y_train = df_train.loc[:, 'vowel'].to_numpy()
n, p = x_train.shape

# center and scale the data: --------------------------------------------------
x_all = x_train.copy()
x_all = (x_all - np.mean(x_all, axis=0)) / np.std(x_all, axis=0)
# -

# singular value decomposition: -----------------------------------------------
svd_all = np.linalg.svd(x_all)
s = svd_all[1]
pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
ax = plt.scatter(x=range(len(s)), y=pct_var)
pct_var[:5]

# u and v are orthonormal: ----------------------------------------------------
u, vh = svd_all[0][:, :5], svd_all[2][:5, :]
(np.round(np.dot(u.T, u)[:5, :5], 3), 
 np.round(np.dot(vh, vh.T)[:5, :5], 3)
)

u = np.dot(x_all, svd_all[2].T) / svd_all[1]
np.allclose(svd_all[0][:, :617], u)
np.allclose(np.std(x_in, axis=0), 1)

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
    v_svd = sm.add_constant(np.dot(x_v, svd[2].T) / svd[1])

    # cumulative variance thresholds
    pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
    n_pc = (
        2 + np.arange(p)[np.cumsum(pct_var) > 0.8][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.9][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.95][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.97][0],
        
    ) 
    pcts = (0.8, 0.9, 0.95, 0.97)
    
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
        y_hat = np.where(y_hat > 0.999, 0.999, y_hat)
        y_hat = np.where(y_hat < 1e-3, 1e-3, y_hat)

        # evaluate predictions
        metrics['ce_val'].append(
            np.mean(
                np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat))

            )
        )

        metrics['accuracy'].append(
            np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v))
        )
        metrics['n'].append(len(y_v))
        print((fold, pcts[i]))

metrics1 = pd.DataFrame(metrics)
metrics1.groupby('pct_var').mean()

clean_names = {
    'ce_train': 'Train Error',
    'ce_val': 'Cross-Validation Error'
}
ax2 = (
    metrics1
    .rename(columns=clean_names)
    .groupby('pct_var')[list(clean_names.values())]
    .mean()
    .plot
    .line()
)
_ = ax2.set_ylabel('Cross Entropy')
_ = ax2.set_xlabel('% Variance Explained')

# ## Logistic Regression in Scikit-Learn

# Let's repeat the previous example using the logistic regression estimator
# from sklearn.  First, let's investigate its interface.

mod1 = LogisticRegression(
    penalty='none',
    fit_intercept=False, #we have a column already
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


# We can repeat the cross-validation above with these solutions. 

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
    v_svd = sm.add_constant(np.dot(x_v, svd[2].T) / svd[1])

    # cumulative variance thresholds
    pct_var = np.power(s, 2) / np.sum(np.power(s, 2))
    n_pc = (
        2 + np.arange(p)[np.cumsum(pct_var) > 0.8][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.9][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.95][0],
        2 + np.arange(p)[np.cumsum(pct_var) > 0.97][0],
        
    ) 
    pcts = (0.8, 0.9, 0.95, 0.97)
    
    for i, npc in enumerate(n_pc):
        # track current 
        metrics['fold'].append(fold)
        metrics['pct_var'].append(pcts[i])
        metrics['npc'].append(npc)

        # train model
        mod = LogisticRegression(
            penalty='none',
            fit_intercept=False, #we have a column already
            max_iter=10000,
            solver='saga'
        )
        res = mod.fit(x_svd[:, :npc], y_in)
        
        # record training fit 
        y_hat = res.predict_proba(x_svd[:, :npc])[:, 1]
        y_hat = np.where(y_hat > 0.999, 0.999, y_hat)
        y_hat = np.where(y_hat < 1e-3, 1e-3, y_hat)
        
        metrics['ce_train'].append(
            np.mean(
                np.where(y_in == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat))
            )
        )
        
        # make predictions on validation data
        y_hat = res.predict_proba(v_svd[:, :npc])[:, 1]
        y_hat = np.where(y_hat > 0.999, 0.999, y_hat)
        y_hat = np.where(y_hat < 1e-3, 1e-3, y_hat)
        
        # evaluate predictions
        metrics['ce_val'].append(
            np.mean(
                np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat))

            )
        )

        metrics['accuracy'].append(
            np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v))
        )
        metrics['n'].append(len(y_v))
        print((fold, pcts[i]))

metrics2 = pd.DataFrame(metrics)
metrics2.groupby('pct_var').mean()

ax3 = (
    metrics2
    .rename(columns=clean_names)
    .groupby('pct_var')[list(clean_names.values())]
    .mean()
    .plot
    .line()
)
_ = ax3.set_ylabel('Cross Entropy')
_ = ax3.set_xlabel('% Variance Explained')

# Let's compare the two solutions in terms of performance. 

vrbls = ['pct_var', 'ce_val', 'accuracy']
pd.merge(
    metrics1.reset_index()[vrbls],
    metrics2.reset_index()[vrbls],
    on=['pct_var']
).groupby('pct_var').mean()

# ## Ridge Regression
#
# Sci-kit learn has a built-in cross-validation functions for
# tuning hyperparameters like the amount of penalization. These
# functions do not support unpenalized regression. Let's see how
# well we can do with the full data matrix using a ridge $L_2$
# penalty. We'll start with a log-scale grid, then refine based 
# on the approximate location of the minimum. 

# rough grid for size of ridge penalty: ---------------------------------------
lr_cv = LogisticRegressionCV(
    cv=folds,
    Cs=[1e-3, 1e-2, 1e-1, 1, 1e1, 1e2],
    penalty='l2',
    scoring='neg_log_loss',
    max_iter=int(1e5)
)
cv_res1 = lr_cv.fit(x_all, y_train)

print(np.mean(cv_res1.scores_[1], axis=0))
cv_res1.C_

lr_cv2 = LogisticRegressionCV(
    cv=folds,
    Cs=np.logspace(-2, 0, 12),
    penalty='l2',
    scoring='neg_log_loss',
    max_iter=int(1e5)
)

cv_res2 = lr_cv2.fit(x_all, y_train)

# minimal entropy from ridge
print(np.min(-1 * np.mean(cv_res2.scores_[1], axis=0)))
cv_res2.Cs_
cv_res2.coefs_paths_[1].shape

df_loss = pd.DataFrame({
    'C': cv_res2.Cs_,
    'log_loss': -1 * np.mean(cv_res2.scores_[1], axis=0)
    #'se': np.std(cv_res2.scores_[1], axis=0) / 2
})
ax4 = (df_loss
 .plot
 .scatter(x='C', y='log_loss', label='Ridge', linestyle='-')
)
_ = (df_loss
 .plot
 .line(ax=ax4, x='C', y='log_loss', label='')
)
_ = ax4.set_ylabel('Cross-Entropy Loss')
_ = ax4.legend()

# ## Lasso
# Next let's using an $L_1$ penalty and apply the Lasso, which will
# tend to produce a sparse solution.

lasso_path = skl.linear_model.lasso_path(x_all, y_train, n_alphas=600)

lr_cv3 = LogisticRegressionCV(
    cv=folds,
    Cs=np.logspace(-4, 4, 9),
    penalty='l1',
    scoring='neg_log_loss',
    max_iter=int(1e5),
    solver='saga'
)

cv_res3 = lr_cv3.fit(x_all, y_train)

# minimal entropy from ridge
print(-1 * np.mean(cv_res3.scores_[1], axis=0))
cv_res3.Cs_

lr_cv4 = LogisticRegressionCV(
    cv=folds,
    Cs=np.logspace(-1, 0, 8)[1:7] * 0.5,
    penalty='l1',
    scoring='neg_log_loss',
    max_iter=int(1e5),
    solver='saga',
    n_jobs=2
)

cv_res4 = lr_cv4.fit(x_all, y_train)

print(-1 * np.mean(cv_res4.scores_[1], axis=0))
cv_res4.C_

# ## Elastic Net
# The elastic net interpolates between ridge and lasso using a 
# weighted combination of both the $L_1$ and $L_2$ penalties. 

(cv_res3.C_, cv_res4.C_)

lr_cv5 = LogisticRegressionCV(
    cv=folds,
    Cs=(2 * cv_res3.C_, cv_res4.C_),
    l1_ratios=(0, .2, .4, .6, .8, .9, 1),
    penalty='elasticnet',
    scoring='neg_log_loss',
    max_iter=int(1e5),
    solver='saga',
    n_jobs=2
)

lr_cv5 = lr_cv5.fit(x_all, y_train)

lr_cv5.scores_[1].shape

entropy = (-1 * np.mean(lr_cv5.scores_[1], axis=0))
entropy.T

# ## Random Forests
#

rf1 = RandomForestClassifier(
    n_estimators=100, # number of trees
    criterion='entropy',
    max_depth=6,      # maximum number of splits
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=0.5,  # smaller yields more regularization
    n_jobs=2
)

res_rf1 = rf1.fit(x_all, y_train)

res_rf1.oob_score_

rf2 = RandomForestClassifier(
    n_estimators=500, # number of trees
    criterion='entropy',
    max_depth=6,      # maximum number of splits
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=0.5,  # smaller yields more regularization
    n_jobs=2
)
res_rf2 = rf2.fit(x_all, y_train)
res_rf2.oob_score_

rf3 = RandomForestClassifier(
    n_estimators=500, # number of trees
    criterion='entropy',
    max_depth=8,      # maximum number of splits
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=0.5,  # smaller yields more regularization
    n_jobs=2
)
res_rf3 = rf3.fit(x_all, y_train)
res_rf3.oob_score_

rf4 = RandomForestClassifier(
    n_estimators=500, # number of trees
    criterion='entropy',
    max_depth=8,      # maximum number of splits
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=1,  # smaller yields more regularization
    n_jobs=2
)
res_rf4 = rf4.fit(x_all, y_train)
res_rf4.oob_score_

rf5 = RandomForestClassifier(
    n_estimators=500, # number of trees
    criterion='entropy',
    max_depth=12,      # maximum number of splits
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=0.5,  # smaller yields more regularization
    n_jobs=2
)
res_rf5 = rf5.fit(x_all, y_train)
res_rf5.oob_score_

res_rf5.predict_proba(x_all).shape

rf6 = RandomForestClassifier(
    n_estimators=500, # number of trees
    criterion='entropy',
    max_depth=None, 
    max_features='sqrt',
    oob_score=True,   # use CV otherwise
    max_samples=0.5,  # smaller yields more regularization
    n_jobs=2
)
res_rf6 = rf6.fit(x_all, y_train)
res_rf6.oob_score_

# cross validation for tuning RF hyperparameters: -----------------------------
max_d = (8, 10, 12, 14, 16, None)
metrics = defaultdict(list)
for fold, (train, val) in enumerate(folds):
    # training data
    x_in = x_train[train, :]
    y_in = y_train[train]
    n, p = x_in.shape
    
    # validation data
    x_v = x_train[val, :]
    y_v = y_train[val]
    
    for i, md in enumerate(max_d):
        # track current 
        metrics['fold'].append(fold)
        metrics['max_depth'].append(md)

        # train model
        rf = RandomForestClassifier(
            n_estimators=500,  # number of trees
            criterion='entropy',
            max_depth=md,      # maximum number of splits
            max_features='sqrt',
            max_samples=0.5,   # smaller yields more regularization
            n_jobs=2
        )
        res_rf = rf.fit(x_in, y_in)
        
        # record training fit 
        y_hat = res_rf.predict_proba(x_in)[:, 1]
        y_hat = np.where(y_hat > 0.999, 0.999, y_hat)
        y_hat = np.where(y_hat < 1e-3, 1e-3, y_hat)
        
        metrics['ce_train'].append(
            np.mean(
                np.where(y_in == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat))
            )
        )
        
        # make predictions on validation data
        y_hat = res_rf.predict_proba(x_v)[:, 1]
        y_hat = np.where(y_hat > 0.999, 0.999, y_hat)
        y_hat = np.where(y_hat < 1e-3, 1e-3, y_hat)
        
        # evaluate predictions
        metrics['ce_val'].append(
            np.mean(
                np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat))

            )
        )

        metrics['accuracy'].append(
            np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v))
        )
        metrics['n'].append(len(y_v))
        print((fold, md))

metrics_rf = pd.DataFrame(metrics)
metrics_rf['max_depth'] = np.where(
    pd.notna(metrics_rf['max_depth']),
    metrics_rf['max_depth'],
    0
)
metrics_rf.groupby('max_depth').mean()

# Notice that while the accuracy is improved relative
# to our best elastic-net model, the entropy is not. 

# ## Gradient Boosted Trees
# Gradient boosted decision trees is one of the best off-the-shelf
# model classes for rectangular data. They can, however, take more
# care in training than the other models we've discussed.  Generally,
# we need to tune the number of boosting rounds (number of trees),
# the learning rate, tree depth, and the number of variables used to
# build each tree. 
#
# The learning rate and number of boosting rounds in particular 
# interact directly in the sense that we generally need more rounds of
# boosting when using a smaller learning rate. 

# fit an initial model to estimate an initial learning rate: ------------------
gb0 = GradientBoostingClassifier(
    loss='deviance',
    n_estimators=500, # number of trees
    learning_rate=.1,  
    subsample=1,
    max_depth=16, 
    max_features='sqrt',
    verbose=1
)
gb0.fit(x_train, y_train)

y_hat = gb0.staged_predict_proba(x_train)
print(type(y_hat))
yh = np.asarray(list(y_hat))
yh.shape

# demonstration of asessing performance at each round: ------------------------
y_hat = np.asarray(list(gb1.staged_predict_proba(x_v)))[:, :, 1]
y_hat.shape
np.mean(
    np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat)),
    axis=1
)

# +
# cross validation for tuning GBT hyperparameters: ----------------------------
gb1 = GradientBoostingClassifier(
    loss='deviance',
    n_estimators=100, # number of trees
    learning_rate=.1,  
    subsample=1,
    max_depth=16, 
    max_features='sqrt',
    verbose=0
)

metrics = defaultdict(list)
for fold, (train, val) in enumerate(folds):
    
    # training data
    x_in = x_train[train, :]
    y_in = y_train[train]
    
    # validation data
    x_v = x_train[val, :]
    y_v = y_train[val]

    # fit model
    gb1.fit(x_in, y_in)
    y_hat = np.asarray(list(gb1.staged_predict_proba(x_v)))[:, :, 1]
    
    # validation loss
    metrics['ce_val'].append(np.mean(
        np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat)),
        axis=1
    ))
    
    # accuracy
    metrics['accuracy'].append(
        np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v), axis=1)
    )

    print(fold)
    
# -

# validation cross-entropy vs round: ------------------------------------------
loss = np.asarray(metrics['ce_val'])
cv_gb_loss = np.mean(loss, axis=0)
fig, ax5 = plt.subplots(nrows=1)
plt.plot(range(100), cv_gb_loss, label='mean', color='black', linewidth=2)
for fold in range(4):
    plt.plot(
        range(100),
        loss[fold, :],
        label='fold ' + str(fold),
        alpha=0.5
    )
_ = ax5.legend(loc='upper right')

(np.min(cv_gb_loss), np.min(loss, axis=1))

# at what stage is the validation loss minimized?: ---------------------------
(
    (cv_gb_loss <= np.min(cv_gb_loss)).nonzero(), # average 
    (loss.T <= np.min(loss, axis=1)).nonzero()    # each fold
)
#loss.T[50:55, 1]

n_rounds = (cv_gb_loss <= np.min(cv_gb_loss)).nonzero()[0][0]
n_rounds

# update parametrs and then refit model to full train data: ------------------
gb1.set_params(**{'n_estimators': n_rounds})
print((gb1.n_estimators_, gb1.n_estimators))
gb1.fit(x_train, y_train)
print((gb1.n_estimators_, gb1.n_estimators))

# ## Evaluation on Test Data 
# The final step in our demonstration is to evaluate the peformance of our
# selected model on the held out test data. 

# +
# subject identification: ----------------------------------------------------
df_test['a'] = df_test['letter'] == 1
df_test['z'] = df_test['letter'] == 26
n, p = df_test.shape
id = np.cumsum(
    df_test['a'].iloc[1:, ].values * 
    df_test['z'].iloc[0:(n - 1), ].values
)

# label vowels: --------------------------------------------------------------
df_test['vowel'] = 0
df_test['vowel'].where(
    np.in1d(df_test['letter'], [1, 5, 9, 15, 21]),
    1,
    inplace=True
)

# extract data to numpy: ------------------------------------------------------
x_test = df_test.loc[:, 'x0':'x616'].to_numpy()
y_test = df_test.loc[:, 'vowel'].to_numpy()
# -

# evalaute test performance: --------------------------------------------------
yh_test = gb1.predict_proba(x_test)[:, 1]
ce_test = np.mean(
    np.where(
        y_test == 0, 
        -1 * np.log(1 - yh_test),
        -1 * np.log(yh_test)
    )
)
ac_test = np.mean(np.where(yh_test > 0.5, y_test, 1 - y_test))
np.round((ce_test, ac_test), 3)
