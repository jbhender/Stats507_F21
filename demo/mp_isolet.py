#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Cross-validate a gradient boosted tree model for the isolet data. 
# Stats 507, Fall 2021
#
# Author: James Henderson
# Date: November 17, 2021
# 79: -------------------------------------------------------------------------

# imports: --------------------------------------------------------------------
import os
import sys
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
import cv_funcs as cvf
import asyncio
from sklearn.ensemble import GradientBoostingClassifier

# command line arguments: -----------------------------------------------------
n_processes = int(sys.argv[1])

# training data: --------------------------------------------------------------
path = '~/github/Stats507_F21/demo/'
iso_train_file = path + 'isolet_train.feather'
df_train = pd.read_feather(iso_train_file)

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

# construct folds: -----------------------------------------------------------
df_train['fold'] = (df_train['id'] - 1) // 30

# folds as array indices
folds = []
n = df_train.shape[0]
rows = np.arange(n)
for fold in range(4):
    train = np.asarray(df_train['fold'] != fold).nonzero()[0]
    test = np.asarray(df_train['fold'] == fold).nonzero()[0]
    folds.append((train, test))
    
# label vowels: --------------------------------------------------------------
df_train['vowel'] = 0
df_train['vowel'].where(
    np.in1d(df_train['letter'], [1, 5, 9, 15, 21]),
    1,
    inplace=True
)

# NumPy arrays: --------------------------------------------------------------
x_train = df_train.loc[:, 'x0':'x616'].to_numpy()
y_train = df_train.loc[:, 'vowel'].to_numpy()

# estimator: -----------------------------------------------------------------
gb0 = GradientBoostingClassifier(
    loss='deviance',
    n_estimators=100, # number of trees
    learning_rate=.1,  
    subsample=1,
    max_depth=16, 
    max_features='sqrt',
    verbose=0
)

# cross-validation tasks: -----------------------------------------------------
cv_tasks = []
for fold, (idx_train, idx_val) in enumerate(folds):
    task = (cvf.cv_fold, 
            (gb0.fit, 
             x_train, 
             y_train, 
             idx_train,
             idx_val, 
             cvf.gb_score,
             'gb0_fold' + str(fold)
            )
           )
    cv_tasks.append(task)


# parallel execution: ---------------------------------------------------------
print('CV start:' + time.ctime())
results0 = cvf.mp_apply(cv_tasks, n_processes)
print('CV end:' + time.ctime())

df_results0 = [pd.DataFrame(r[1]) for r in results0]
for i, df in enumerate(df_results0):
    _ = df.insert(0, 'label', results0[i][0])
    _ = df.insert(1, 'estimators', np.arange(1, df.shape[0] + 1))

df_results0 = pd.concat(df_results0, axis=0)
df_results0.reset_index(inplace=True)
df_results0.to_feather(path + 'df_results0.feather')

# 79: -------------------------------------------------------------------------  
