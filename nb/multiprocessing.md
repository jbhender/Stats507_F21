---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Process Parallelism </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Process-based Parallelism with Multiprocessing 
*Stats 507, Fall 2021*

James Henderson, PhD  
November 16, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Parallel & Asynchronous Computing](#/slide-2-0)
 - [multiprocessing](#/slide-3-0)
 - [Pipes and Queues](#/slide-4-0)
 - [Pool](#/slide-5-0)
 - [Background Tasks](#/slide-6-0)
 - [asyncio](#/slide-7-0)
 - [Random Numbers](#/slide-8-0)
 - [Takeaways](#/slide-9-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## MP Demo
  - These slides are intended to be presented/read alongside the
    `multiprocess` demo from the course repo. 
  - The demo relies on a number of functions defined in `cv_funcs.py`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Parallel Computing in Data Science
  - Many core data science methods are *trivially parallel* - composed of
    a collection of independent tasks:
    + Monte Carlo approximations,
    + Bootstrap replication and other resampling methods,
    + Cross-validation,
    + Bagging estimators such as a random forest. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Built-in Parallelism
  - A number of functions (e.g. sklearn estimators) have built-in support
    for parallel computation:
      + `LogisticRegressionCV()` using `n_jobs` parameter,
      +  `RandomForestClassifier()` using `n_jobs` parameter.
  - Prefer built-in methods when available. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Asynchronous Computing 
 - [Asynchronous computing][async] refers to having events that occur 
    independently of the primary control flow in our program.  
 - In a traditional, *synchronous* program each statement or expression 
   *blocks* while evaluating -- it forces the program to wait until it 
   completes.
 - An *asynchronous* program has some statements that do not block -- allowing
   the control flow to continue until either:
    + the value of the non-blocking statement is needed, or
    + execution resources such as CPU cores are exhausted.

[async]:https://en.wikipedia.org/wiki/Asynchrony_(computer_programming)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Concurrent Programs for I/O bound tasks
 - Traditionally *concurrent* programming has been focused on I/O bound tasks.
 - If querying external servers or databases, would otherwise have to wait for 
   each query to finish and return before sending the next request.
 - Concurrency helps in this situation because it allows the program to wait 
   in multiple queues at once. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Parallel Computing 
 - Modern computers, including laptops and desktops, have multiple processors
   or cores. 
 - A parallel program takes advantage of this architecture to
   complete more than one task at a time -- reducing the "wall time" a 
   *CPU-bound* program takes to run. 
 - Concurrency including parallelism can be implemented using threads,
   processes, futures or other abstractions. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Parallelism is not Magic
 - When thinking of parallelizing some portion of a program, remember that 
   *parallelism is not magic*. 
 - There is some computational overhead involved in splitting the task, 
   initializing child processes, communicating data, and collating results.  
 - For this reason, there is usually little to be gained in parallelizing 
   already fast computations.
 - An overly parallelized program incurs more *overhead* than necessary to 
   use available resources. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Vectorization > Parallelism
 - Writing vectorized code is often more efficient than writing parallel code.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## `multiprocessing`
  - The built-in `multiprocessing` module provides *process-based parallelism*.
  - Other modules in the standard library that support parallelism and 
    asynchronous computations include:
     + `concurrent.futures`,
     + `threading`,
     + `asyncio`.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import multiprocessing as mp
import cv_funcs as cvf
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Process
- Create a child process using `mp.Process()`. 
- The `Process` object's `.start()` method *spawns* a new Python process.
- On Unix, can be started by forking (efficient).
- A *forked* child process has *read-only* access to the objects in the 
  parent process's namespace. 
- On Windows or MacOS (recently) only the "spawn" option for an independent
  process is supported. 
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Process
- The `target` argument is used to define a callable to be run when the 
  process has been initialized. 
- The `args` and `kwargs` parameters are used to pass arguments to the 
  callable passed to `target`. 
- A `Process` should be setup and started within a "main gate". 
- In an interactive session, local functions will not be recognized. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Process
- To block until a child process has completed, call its `.join()`
  method.
- This will also shutdown the child process.
- Can call `.close()` method to shutdown zombie processes.  
- Use `mp.active_children()` to see active child processes. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pipes and Queues
> When using multiple processes, one generally uses *message passing* for 
> communication between processes and avoids having to use any synchronization
> primitives like locks.

> For passing messages one can use Pipe() (for a connection between 
> two processes) or a queue (which allows multiple producers and consumers).
> 
> --[docs][pq]

[pq]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Queues
 - For *trivially parallel* tasks, use *queues* which easily generalize to 
   multiple processes.
 - A `Queue()` is implemented using a `Pipe()` but handles synchronization 
   implicitly. 
 - Create a `Queue` using `mp.Queue()` with (optionally) a maximum size. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Queues
- *Producer* processes use a queue's `.put()` method to enter items into the
  queue.
- *Consumer* processes use a queue's `.get()` method to accept an item from 
  the queue.  
- Both have optional `block` and `timeout` arguments.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Queue Pattern
 - We'll follow the pattern [here][mpq] which uses two queues:
     + `task_queue` sends tasks from the parent process to child processes,
     + `done_queue` sends results from the child processes to the parent 
        process.  
 - In this case, `task_queue` has a single *producer* and (potentially) 
   multiple *consumers*.
 - The `done_queue` has (potentially) multiple *producers* and a single
   *consumer*. 

 [mpq]: https://docs.python.org/3/library/multiprocessing.html#multiprocessing-programming
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Queue Pattern
 - In the pattern we'll use two key functions:
   + `worker()` iterates over tasks in the queue until it receives the 
     *sentinel* to stop ('STOP');
   + `calculate()` takes the tuple represent the task and calls the callable
     with the unpacked arguments.
 - We encapsulate the full pattern into `mp_apply()`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pool
 - A *pool* of worker processes can be setup with `mp.Pool()`. 
 - The `Pool` object has several methods for dispatching work to these 
   child/worker processes.
 - The most straightforward is `.map()` which takes a function and an iterable.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Pool
 - A `Pool` object must be explicitly closed using `.close()` which will wait
   for assigned processes to close.
 - A tidy way to ensure this implicitly is to use a `with` statement. 
 - The `.join()` method can be used *after* `.close()` to block until all
   tasks are completed. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Chunking
 - The `.map()` method accepts an argument `chunksize` to determine how 
   tasks are assigned to workers. 
 - Larger chunks result in less communication overhead. 
 - For tasks with predictable and low-variance run time, best to chunk so each
   worker processes a single chunk. 
 - For tasks with high-variance or long-tailed run times, better to use a 
   smaller chunk size to keep all workers busy for as long as possible. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Star maps
 - A `Pool` object's `.starmap()` method can be used to parallelize function
   calls over more than one argument. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Background task(s)
 - During model and notebook development, long-running tasks can interrupt
   our flow by blocking the active process (kernel).
 - Running these tasks asynchronously ("in the background") using a
   non-blocking workflow can help us to be more productive.
 - We implement this concept using the "queue" pattern in the functions
   `bg_task()` and `bg_get()`.
 - See also `Pool.map_async()`.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## asyncio
 - The asyncio is designed for writing concurrent I/O operations -- 
   particularly useful for working with websites.
 - There are three key concepts: 
    + Define asynchronous, non-blocking functions using `async def`.
    + Block and retrieve results using `await`,
    + Every asynchronous function call must be awaited.  
 - You can think of the "coroutine" as a value that will be available at some
   point in the future.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Background Tasks using asyncio
 - We implement the "background tasks" pattern using asyncio in `async_task()`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Random Numbers
 - Many statistical and machine learning applications rely on pseudo-random 
   numbers for things like  sampling from distributions and stochastic 
   optimization, e.g. bootstrap, Monte Carlo.
 - Care needs to be taken to ensure random number streams behave as expected 
   when using parallel computations.
 - Issues of both reproducibility and (pseudo)-independence. 
 - Read more about this at 
   https://numpy.org/doc/stable/reference/random/parallel.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
  - Many data science methods can be trivially parallelized.   
  - The multiprocessing module provides *process-based parallelism*. 
  - Reduce run-time by spreading computations across multiple Python sessions.
  - Run long-running code in the background during development. 
  - Use built-in methods for parallel computing when available.
<!-- #endregion -->
