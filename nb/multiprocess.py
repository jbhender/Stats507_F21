# # 
# # Multiprocess Parallelism
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *November 16, 2021*

# In this notebook we'll explore multi-process parallelism
# as implemented in Python's multiprocessing library. We'll
# use the following imports -- note that `cv_funcs` refers to
# `cf_funcs.py` which you can find in the same rep as this
# document. 

# imports: --------------------------------------------------------------------
import os
import time
import numpy as np
import pandas as pd
import multiprocessing as mp
import cv_funcs as cvf
import asyncio
from sklearn.ensemble import GradientBoostingClassifier

# ## Simple Examples
# In the code cells below, we explore `cvf.wait()` and review calling
# functions by unpacking tuples (for positional arguments) or 
# dictionaries (for keyword arguments).

cvf.wait(1)

# The two examples below remind us how function arguments can
# be unpacked from a tuple or dictionary.

# call by unpacking positional arguments
(cvf.wait(*(2, )))

# call by unpacking keyword arguments
cvf.wait(**{'i': 1})

# Here is our first example, note the "main gate". 

if __name__ == "__main__":
    print(mp.active_children())
    print('Not blocking: ' + time.ctime())
    p = mp.Process(target=cvf.wait, args=(10,))
    p.start()
    print('Blocking: ' + time.ctime())
    print(mp.active_children())
    p.join()
    print('Done: ' + time.ctime())
    print(mp.active_children())


# Here is a similar example showing that we do not need 
# to explicitly join a process for it to close on completeion.

if __name__ == "__main__":
    print(mp.active_children())
    print('Not blocking: ' + time.ctime())
    p = mp.Process(target=cvf.wait, args=(1,))
    p.start()
    print('Blocking: ' + time.ctime())
    print(mp.active_children())

(mp.active_children(), p.is_alive())

# ## Communicating with Queues
# Parallel tasks can be useful without communication if, for example,
# each task is called for its side effects - such as writing a result to
# disk. However, parallel computing is more powerful with inter-process
# communication. 
#
# In the next set of code cells, we'll a useful pattern for using
# first-in-first-out queues for trivially parallel tasks. Here are
# two sets of tasks we'll apply the pattern to.

# parameters: -----------------------------------------------------------------
n_processes = 2
tasks = [(cvf.wait, (i + 1, )) for i in range(10)]
tasks_2 = [(cvf.wait, (i, ) ) for i in (1, 6, 2, 7, 3, 8, 4, 9, 5, 10)]

np.sum([i[1][0] for i in tasks]), np.sum([i[1][0] for i in tasks_2])

# Here is the pattern applied to the first task list. 

# parallel execution: ---------------------------------------------------------
if __name__ == '__main__':
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit tasks
    for task in tasks:
        task_queue.put(task)

    # start processes
    for i in range(n_processes):
        mp.Process(target=cvf.worker, args=(task_queue, done_queue)).start()
    
    # get unordered results 
    results = []
    for i, task in enumerate(tasks):
        results.append((i, done_queue.get()))

    # stop child processes
    for i in range(n_processes):
        task_queue.put('STOP')


results

# Here is the same pattern applied to the second set of tasks.
# This second task list is constructed to illustrate what it means
# for the queue to be FIFO. 

# parallel execution: ---------------------------------------------------------
if __name__ == '__main__':
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit tasks
    for task in tasks_2:
        task_queue.put(task)

    # start processes
    for i in range(n_processes):
        mp.Process(target=cvf.worker, args=(task_queue, done_queue)).start()
    
    # get unordered results 
    results2 = []
    for i, task in enumerate(tasks_2):
        results2.append((i, done_queue.get()))

    # stop child processes
    for i in range(n_processes):
        task_queue.put('STOP')

# ## Pools
# The code cells below collect simple examples of using a 
# pool of worker processes to perform parallel computations.

print('Start: ' + time.ctime())
with mp.Pool(2) as p:
    results1 = p.map(cvf.wait, range(1, 11))
print('End: ' + time.ctime())

mp.active_children()

results1

# Notice the default chunking behavior in `results1`.
# Next, we explicitly set the chunksize to 5. 

print('Start: ' + time.ctime())
with mp.Pool(2) as p:
    results2 = p.map(cvf.wait, range(1, 11), chunksize=5)
print('End: ' + time.ctime())

results2

# Finally, let's use a chunksize of 1.

print('Start: ' + time.ctime())
with mp.Pool(2) as p:
    results3 = p.map(cvf.wait, range(1, 11), chunksize=1)
print('End: ' + time.ctime())
results3

# In these examples, we had relatively few tasks and didn't
# need to worry much about overhead. However, in, say, a 
# Monte Carlo study with 10,000 replciates we wouldn't want to use a
# chunksize of 1.

# ## Parallel Cross-Validation
# Next, we'll use the queue pattern above to parallelize 4-fold
# cross-validation for gradient boosted tree classifiers applied to
# the isolet data.  
#
# This first cell sets up the training data and divides it into folds.

# +
# training data: -------------------------------------------------------------
iso_train_file = 'isolet_train.feather'
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
# -

# Here is the first estimator we'll evaluate (at each boosting
# stage) using cross-validation.

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

# Here is a set of task to feed to the pattern. Be sure to examine the
# `cv_fold()` and `gb_score()` functions. 

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


# Notice that we are not creating four copies of the data.

assert cv_tasks[0][1][1] is cv_tasks[1][1][1]

# Here is the queue pattern applied to the cross-validation tasks.

# parallel execution: ---------------------------------------------------------
if __name__ == '__main__':
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # submit tasks
    for task in cv_tasks:
        task_queue.put(task)

    # start processes
    for i in range(n_processes):
        mp.Process(target=cvf.worker, args=(task_queue, done_queue)).start()
    
    # get unordered results 
    results = []
    for task in cv_tasks:
        results.append(done_queue.get())

    # stop child processes
    for i in range(n_processes):
        task_queue.put('STOP')

# format results as a DataFrame: ----------------------------------------------
df_results = [pd.DataFrame(r[1]) for r in results]
for i, df in enumerate(df_results):
    _ = df.insert(0, 'label', results[i][0])
    _ = df.insert(1, 'estimators', np.arange(1, df.shape[0] + 1))

# ### Functional Version
# When we have a pattern we want to apply repeatedly, we should 
# encapsulate it into a function. I do this in `mp_apply()`. 

results2 = cvf.mp_apply(cv_tasks, 2)

df_results2 = [pd.DataFrame(r[1]) for r in results2]
for i, df in enumerate(df_results2):
    _ = df.insert(0, 'label', results2[i][0])
    _ = df.insert(1, 'estimators', np.arange(1, df.shape[0] + 1))

df_results2 = pd.concat(df_results2, axis=0)
df_results2

# ## Long-Running Tasks
# Asynchronous computation can be useful during model and notebook
# development even if you only have a single task to run. Specifically,
# creating a child process to evaluate a long-running task allows you to
# continue to work and test ideas in the main process, while the long-running
# task runs in the background. 
#
# To do this, we can set `block=False` in `queue.get()` to prevent a check
# on whether the result is completed from blocking. 

print(mp.active_children())

# +
long_task = (cvf.wait, (30, ))

# background execution: -------------------------------------------------------
if __name__ == '__main__':
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # submit task
    task_queue.put(long_task)

    # start process
    p1 = mp.Process(target=cvf.worker, args=(task_queue, done_queue))
    p1.start()
    
mp.active_children()
# -

# get result without blocking 
if not 'long_task_result' in locals():
    try:
        long_task_result = done_queue.get(False)
        print('Assigned task.')
        # stop child process
        task_queue.put('STOP')        
    except:
        if p1.is_alive():
            print('Task still running.')
        else:
            print('Child process inactive.')
else:
    print('Task already assigned.')

if not p1.is_alive():
    print(long_task_result)

# The functions `bg_task()` and `bg_get()` encapsulate this pattern.

p, tq, dq = cvf.bg_task(long_task)

res = cvf.bg_get(p, tq, dq)

res

# ## asyncio
# Here is a short example asyncio module for the 
# long-running background task example. 

# +
async def main():
    """
    Hello world example from asyncio docs. 
    """
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')
    
await main()
# -

p = main()
time.sleep(0.5)
print('main is not blocking')
await p

async def async_task(task): 
    return(task[0](*task[1]))

task_future = async_task(tasks[3])
print("Not blocking")
res = await task_future
(task_future, res)
