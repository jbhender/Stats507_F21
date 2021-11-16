#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Cross-Validation functions for multi-process parallelism
#
# Author: James Henderson  
# Date: November 14, 2021  
# 79: -------------------------------------------------------------------------

# imports: --------------------------------------------------------------------
import os
import time
import numpy as np
import multiprocessing as mp

# function(s) to parallelize: -------------------------------------------------
def wait(i):
    """
    Wait i seconds and then return the process id.

    Parameters
    ----------
    i -  int or float
    The time, in seconds, to wait before returning the process id. 

    Returns
    -------
    The process id where wait is called.
    """
    start = time.ctime()
    time.sleep(i)
    end = time.ctime() 
    return((i, os.getpid(), start, end))


def cv_fold(fit, x, y, idx_train, idx_val, score, label=None):
    """
    Compute score for a cross-validation fold.

    Parameters
    ----------
    fit - callable.
    A callable to fit an estimator to the training data.
    x, y - ndarray
    Features and labels for training and validation folds.
    idx_train, idx_val - ndarray or slice.
    Indices for subsetting x and y into training and validation folds.
    score - callable
    Function with signature (res, x, y) for scoring validation sample
    predictions from the estimator fit to training data. 
    label - string or None, optional.
    An optional label for tracking results during parallel execution. 
    The default is None.

    Returns
    -------
    A tuple (label, metrics) where metrics is the object returned by the 
    function passed to score. 

    """
    # fit model
    res = fit(x[idx_train], y[idx_train])
    
    # compute score(s)
    metrics = score(res, x[idx_val], y[idx_val])

    # return scores and label
    return((label, metrics))


def gb_score(res, x_v, y_v):
    """
    Compute cross entropy and accuracy at each stage of boosting model.

    Parameters
    ----------
    res = an object returned by sklearn.GradientBoosting*
    It's fit method should be called. Th object's staged_predict_proba()
    method is called. 

    x_v, y_v - Validation features and labels

    Returns
    -------
    A dictionary with entries `ce_val` and `ac_val` for the validation 
    cross-entropy and accuracy after each boosting stage.
    """
    # compute predictions after each stage
    y_hat = np.asarray(list(res.staged_predict_proba(x_v)))[:, :, 1]
    
    # cross entropy on validation set at each stage
    ce_val = np.mean(
        np.where(y_v == 0, -1 * np.log(1 - y_hat), -1 * np.log(y_hat)),
        axis=1
    )
    
    # accuracy
    ac_val = np.mean(np.where(y_hat > 0.5, y_v, 1 - y_v), axis=1)

    return({"ce_val": ce_val, "ac_val": ac_val})

# multiprocess helper functions: ----------------------------------------------
def calculate(func, args):
    """
    Call func(*args) as part of a worker process.

    Parameters
    ----------
    func - callable function
    args - a tuple of positional args for func

    Returns
    -------
    The result of `func(*args)`

    """
    result = func(*args)
    return(result)

def worker(input, output):
    """
    Function run by worker processes.

    Taken from
    <https://docs.python.org/3/library/multiprocessing.html
    #multiprocessing-programming>

    Parameters
    ----------
    input, output - Queues.
    Input and output queues.

    Returns
    -------
    None, called for it's side effects.      
    """
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)


def mp_apply(tasks, n_processes=2):
    """
    Compute tasks in parallel.

    Parameters
    ----------
    tasks - list of tuples.
    A list of tasks, each formulated as a tuple with first element a callable
    and second a tuple of positional arguments. 
    n_processes - int, optional.
    The number of child processes used to compute the tasks. The default is 2.

    Returns
    -------
    The unordered results of the computed tasks.

    """
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # submit tasks
    for task in tasks:
        task_queue.put(task)

    # start processes
    for i in range(n_processes):
        mp.Process(target=worker, args=(task_queue, done_queue)).start()
    
    # get unordered results 
    results = []
    for i, task in enumerate(tasks):
        results.append(done_queue.get())

    # stop child processes
    for i in range(n_processes):
        task_queue.put('STOP')
    
    return(results)

# background functions: -------------------------------------------------------
def bg_task(task):
    """
    Run a task in a child process without blocking using a queue.

    To retrieve the results us `bg_get()`. 

    Parameters
    ----------
    task - tuple
    A tuple with first argument a callable and second a tuple of positional
    parameters.

    Returns
    -------
    A tuple of handles for the child process, task queue, and done queue. 
    """
    # create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit task
    task_queue.put(task)

    # start process
    p = mp.Process(target=worker, args=(task_queue, done_queue))
    p.start()

    # return handles
    return((p, task_queue, done_queue))

def bg_get(p, task_queue, done_queue, block=False):
    """
    Get the result of a completed task with or without blocking. 

    Also cleans up the child process if completed and returning a result. 

    Parameters
    ----------
    p, task_queue, done_queue - handles
    Handles for the child process and queues as returned by `bg_task()`. 
    block - bool, optional.
    Whether the call should block (wait until the task completes) or not. The
    default is False (do not block).

    Returns
    -------
    The result of the task, if complete, else None.
    """
    # get result without blocking 
    try:
        result = done_queue.get(block)
        # stop child process
        task_queue.put('STOP')
        return(result)
    except:
        if p.is_alive():
            print('Task still running.')
        else:
            print('Child process inactive.')
    return(None)

async def async_task(task): 
    """
    Compute task without blocking.

    The task must later be awaited to avoid an error.

    Parameters
    ----------
    task - tuple.
    A tuple of length 2 or 3 with callable in its first position. The second
    position should hold a tuple of positional arguments or a dictionary of 
    keyword arguments to be unpacked in its second. If length 3, positional
    arguments must precede keyword arguments. 

    Returns
    -------
    A coroutine object. Use `await` to block and get the result returned by
    the callable in task. 
    """
    if len(task) == 3:
        return(task[0](*task[1], **task[2]))
    elif isinstance(task[1], tuple):
        return(task[0](*task[1]))
    else:
        return(task[0](**task[1]))

# 79: -------------------------------------------------------------------------
