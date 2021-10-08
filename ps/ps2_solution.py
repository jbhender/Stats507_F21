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
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   markdown:
#     extensions: footnotes
# ---

# ## Problem Set 2, Solution
# **Stats 507, Fall 2021**  
# *James Henderson, PhD*  
# *September 30, 2021*
#
# This question was inspired by and borrows heavily from this 
# [question][soq] on <https://stackoverflow.com> featured in their newsletter
# [The Overflow][of]. 
#
# [soq]: https://stackoverflow.com/questions/69025133/filtering-list-of-tuples-based-on-condition
# [of]: https://stackoverflow.blog/2021/09/10/the-overflow-90-a-patent-on-a-time-machine/

# ## Contents
# + [Question 0](#Question-0)
# + [Question 1](#Question-1)
# + [Question 2](#Question-2)
# + [Question 3](#Question-3)

# ## Question 0
# In this question, you were asked to write a code review for the following
# Python snippet.
#
# ```python
# sample_list = [(1, 3, 5), (0, 1, 2), (1, 9, 8)]
# op = []
# for m in range(len(sample_list)):
#    li = [sample_list[m]]
#        for n in range(len(sample_list)):
#            if (sample_list[m][0] == sample_list[n][0] and
#                    sample_list[m][3] != sample_list[n][3]):
#                li.append(sample_list[n])
#        op.append(sorted(li, key=lambda dd: dd[3], reverse=True)[0])
# res = list(set(op))
# ```
#
# **Purpose**: The snippet takes a list of tuples and, after a small 
# correction, returns a list of tuples having the maximum 3rd element among
# tuples sharing a common first element. 
#
# **Review**: 
#  
# *Correctness*: 
#  The code accomplishes the intended task with the exception that
#  the sample tuples should be indexed with "2" rather than "3" if we intend
#  to sort on the 3rd element. The function also breaks ties among tuples
#  sharing first and third elements by taking the one appearing first in the
#  list. The author should clarify if this is the intended behavior.
#
# *Style*: 
#  + Both the inner `for` loop and the `op.append` line are overindented
#    and should align with `li` above it.
#  + Aligning the two conditions in the `if` statement (on the 's') would be
#    easier to read. 
#
# *Efficiency*:  
#  + There are two nested loops ranging over the entire sample list, so that every 
#    pair of tuples is compared twice. It should only be necessary to compare each
#    pair of tuples once.
#  + Sorting a list of tuples sharing a first element with each tuple
#    is an expensive way to find the tuple with the maximum 3rd element.
#    Could this be resolved in the condition passed to if? 
#  + Generalizing the roles of '0' and '2' ("3") would make this easier to read
#    and, if encapsulated into a function, reuse. 

# ## Imports
# The remaining questions will use the following imports.

# modules: --------------------------------------------------------------------
import numpy as np
import pandas as pd
from os.path import exists
from math import floor 
from timeit import Timer
from collections import defaultdict
from IPython.core.display import display, HTML
# 79: -------------------------------------------------------------------------

# ## Question 1
# In this question we use NumPy and a list comprehension to define a function
# that generates arbitrary lists of tuples containing integers. 
#

# function to generate sample lists of tuples: -------------------------------
def gen_list_of_tuples(n, tup_size=3, low=0, high=1000, rng=None):
    """
    Generate a list of n tuples of length tup_size of integers low to high.

    Parameters
    ----------
    n : integer
        The number of tuples in the list.
    tup_size : integer, optional
        The length of the tuples created. The default is 3.
    low : integer, optional
        The low end of the range to generate integers from.
    high : integer, optional
        The high end of hte range to generate integers from.
    rng: A random number generator object, e.g. from np.random.default_rng().
        If None, one is created within the context of the function.
    
    Returns
    -------
    A list of length `n` with tuples of size `tup_size` consting of uniform
    random integers in [low, high).
    """
    
    # setup random number generator, if needed
    if rng is None:
        rng = np.random.default_rng()
    
    # generate a numpy array
    ints = rng.integers(0, 1000, tup_size * n)
    ints.shape = (n, tup_size)
    # convert to a list of tuples
    # ex_list = [tuple(ints[i, ]) for i in range(n)]
    ex_list = [tuple(x) for x in ints]
    return(ex_list)


assert len(gen_list_of_tuples(10)) == 10
assert all([isinstance(x, tuple) for x in gen_list_of_tuples(5, 3)])
# You weren't required to add this check. 
assert all([len(x) == 3 for x in gen_list_of_tuples(5, 3)])

# ## Question 2
# In this question you were asked to encapsulate the warmup snippet into a 
# function and then to write two additional functions accomplishing the same 
# task. The first such function, in part b, was intended to resemble the
# snippet with the improvements you suggested in the warm up. The second, in
# part c, should be an original approach to the problem. The final step in
# this question was to compare the run-time efficiency of the three versions. 
#

# ### a) Encapsulate snippet into a flexible function
# Here is an encapsulation of the snippet that generalizes the question a bit
# so that the sorting index (`by`) and comparator index (`max_of`) are
# parameters.  Though not explicitly instructed to, you should also have made
# the input list a parameter.

# approach 1, from the snippet: -----------------------------------------------
def max_tup_op(tuple_list, max_of=2, by=0):
    """
    Find tuples with maximum value in one position by unique value in another.
    
    Among all tuples in `tuple_list` sharing a common value in the `by`
    position, find those also having maximum value in the `max_of` position. 

    Parameters
    ----------
    tuple_list : list of tuples
        The list of tuples to organize as described above.
    max_of : int, optional
        The position within the tuples to maximize. The default is 2.
    by : int, optional
        The position determining which tuples to compare. The default is 0.

    Returns
    -------
    A list of all tuples, where, for each unique `by` value, the maximum
    value in the `max_of` position is achieved.
    """
    op = []
    for m in range(len(tuple_list)):
        li = [tuple_list[m]]
        for n in range(len(tuple_list)):
            if (tuple_list[m][by] == tuple_list[n][by] and
                tuple_list[m][max_of] != tuple_list[n][max_of]):
                li.append(tuple_list[n])
        op.append(sorted(li, key=lambda dd: dd[max_of], reverse=True)[by])
    return(list(set(op)))


# tests
sample_list = [(5, 16, 2), (5, 10, 3), (5, 8, 1), (21, 24, 1)]
sample_res = [(5, 10, 3), (21, 24, 1)]
# additional test for behavior when tuples are tied.
sample_list2 = sample_list + [(5, 8, 3)]

assert set(max_tup_op(sample_list)) == set(sample_res)
sample_res2 = max_tup_op(sample_list2)
sample_res2

# ## b) Implement suggestions from your code review. 
# Here is a version based on my suggestions in the code review.

# approach 1a, lightly modified: ---------------------------------------------
def max_tup_cr(tuple_list, max_of=2, by=0):
    """
    Find tuples with maximum value in one position by unique value in another.
    
    Among all tuples in `tuple_list` sharing a common value in the `by`
    position, find those also having maximum value in the `max_of` position. 

    Parameters
    ----------
    tuple_list : list of tuples
        The list of tuples to organize as described above.
    max_of : int, optional
        The position within the tuples to maximize. The default is 2.
    by : int, optional
        The position determining which tuples to compare. The default is 0.

    Returns
    -------
    A list of all tuples, where, for each unique `by` value, the maximum
    value in the `max_of` position is achieved.
    """
    op = set()
    by_prev = set() # keep track of tuples already sorted
    for m, tup0 in enumerate(tuple_list):
        li = set([tup0])
        by_val = tup0[by]
        if by_val in by_prev:
            continue
        by_prev.update([by_val])
        mx = tup0[max_of]
        for n in range(m + 1, len(tuple_list)):
            tup1 = tuple_list[n]
            if tup1[by] == by_val:
                if tup1[max_of] > mx:
                    li = set([tup1])
                    mx = tup1[max_of]
                elif tup1[max_of] == mx:
                    li.update([tup1])
        op.update(li)
    return(list(op))


assert set(max_tup_cr(sample_list)) == set(sample_res)
assert set(max_tup_cr(sample_list2)) == set(sample_res2)

# ## c) Solve the same problem from scratch.
# In this part, you were asked to write your own solution to the problem 
# solved by the original snippet - finding tuples taking an observed maximum
# at one position among those with common values at another position. It was
# suggested to use a `dict` or `defaultdict` in your solution. 
#
# Below are a couple of approaches (you were only required to implement one).
# The first is (or at least *was* when the assignment was written) the accepted
# answer from the original stack overflow post. Note that this solution solves 
# the stated problem with the original sample list of tuples, but doesn't
# handle ties in the same way (only returning the tuple appearing first). 

# approach 2, using default_dict from the accepted answer: -------------------
def max_tup_answer(tuple_list, max_of=2, by=0):
    """
    Find tuples with maximum value in one position by unique value in another.
    
    Among all tuples in `tuple_list` sharing a common value in the `by`
    position, find those also having maximum value in the `max_of` position. 

    Parameters
    ----------
    tuple_list : list of tuples
        The list of tuples to organize as described above.
    max_of : int, optional
        The position within the tuples to maximize. The default is 2.
    by : int, optional
        The position determining which tuples to compare. The default is 0.

    Returns
    -------
    A list of all tuples, where, for each unique `by` value, the maximum
    value in the `max_of` position is achieved.
    """
    d = defaultdict(list)
    for e in tuple_list:
        d[e[by]].append(e)
    return([max(val, key=lambda x: x[max_of]) for val in d.values()])


assert set(max_tup_answer(sample_list)) == set(sample_res)
#assert set(max_tup_answer(sample_list2)) == set(sample_res2)
(set(max_tup_answer(sample_list2)), 
 set(max_tup_answer([(5, 8, 3)] + sample_list)) 
 )

# This is my original approach inspired by the accepted answer and a comment
# asking whether the maximum could be resolved at time of sorting. It's a bit
# more verbose, partially out of a need to use sets to keep track of all 
# unique tied tuples.

# approach 3, tracking result: -----------------------------------------------
def max_tup(tuple_list, max_of=2, by=0, lowest=-np.Inf):
    """
    Find tuples with maximum value in one position by unique value in another.
    
    Among all tuples in `tuple_list` sharing a common value in the `by`
    position, find those also having maximum value in the `max_of` position. 

    Parameters
    ----------
    tuple_list : list of tuples
        The list of tuples to organize as described above.
    max_of : int, optional
        The position within the tuples to maximize. The default is 2.
    by : int, optional
        The position determining which tuples to compare. The default is 0.

    Returns
    -------
    A list of all tuples, where, for each unique `by` value, the maximum
    value in the `max_of` position is achieved.
    """
    top_tup = {}
    for tup in tuple_list:
        old = top_tup.get(tup[by], (lowest, None))
        if old[0] < tup[max_of]:
            top_tup.update({tup[by]: (tup[max_of], set([tup]))})
        elif old[0] == tup[max_of]:
            top_tup.update({tup[by]: (tup[max_of], old[1].union(set([tup])))})
    op = set()            
    [op.update(i[1]) for i in top_tup.values()]
    return(list(op))

assert set(max_tup(sample_list)) == set(sample_res)
assert set(max_tup(sample_list2)) == set(sample_res2)

# Finally, here is an almost identical approach that tracks the maximum and the
# tuples achieving that maximum separately, rather than using a tuple as in the
# previous answer.

# approach 4, tracking result: -----------------------------------------------
def max_tup2(tuple_list, max_of=2, by=0, lowest=-np.Inf):
    top_max = {} # dictionary of maxima
    top_tup = defaultdict(set)
    for tup in tuple_list:
        a = top_max.get(tup[by], lowest)
        if a < tup[max_of]:
            top_tup.update({tup[by]: set([tup])})
            top_max.update({tup[by]: tup[max_of]})
        elif a == tup[max_of]:
            new = top_tup.get(tup[by]).union(set([tup]))
            top_tup.update({tup[by]: new})
    op = set()            
    [op.update(i) for i in top_tup.values()]
    return(list(op))

assert set(max_tup2(sample_list)) == set(sample_res)
assert set(max_tup(sample_list2)) == set(sample_res2)

# ## d) Monte Carlo comparison of runtimes
# Finally, we compare the approaches above in terms of their running time 
# efficiency using the function from question 1 to generate sample tuples. 

# First, let's make sure they all (save for the `max_tup_answer()`) return
# the same result (viewed as a set) on a larger list. 

# check that all but tup_answer return the same set or results: ---------------
tup_list = gen_list_of_tuples(1000, tup_size=3, low=0, high=1000)
assert (
    set(max_tup_op(tup_list)) ==  set(max_tup_cr(tup_list)) == 
    set(max_tup(tup_list)) == set(max_tup2(tup_list))
)

# In this example, I'm going to estimate the average running time using
# n = 100 randomly generated lists of length 100 and 100 lists of length 500.
# We'll repeated the trial 10 times to estimate the average run time of this
# task.  

# compare efficiency on randomly generated lists: -----------------------------
n_lists, list_len, tup_len, val_max = 100, (100, 500), 3, 100
n_mc = 10

rng = np.random.default_rng(10 * 1 + 2021)
func_list = [max_tup_op, max_tup_cr, max_tup_answer, max_tup, max_tup2]
res = defaultdict(list)
for ll in list_len:
    l = [gen_list_of_tuples(ll, tup_len, 0, val_max, rng) 
        for i in range(n_lists)]
    for r in range(n_mc):
        res['List Length'].append(ll)
        for f in func_list:
            t0 = Timer("[f(i) for i in l]", globals={"f": f, "l": l})   
            res[f.__name__].append(t0.timeit(1))

tab = (pd.DataFrame(res)
 .groupby('List Length')
 .agg(lambda x: (
    '<center>{0:4.2f} <br> ({1:4.2f}, {2:4.2f})</center>'.format(
        np.mean(x), 
        np.mean(x) - 1.96 * np.std(x) / np.sqrt(len(x)),
        np.mean(x) + 1.96 * np.std(x) / np.sqrt(len(x))
    )))
).to_html(escape=False, justify='left')

cap = """
<b> Table 1.</b> <em> Timing comparisons.</em>
Time, in seconds, for each function to identify group-wise maxima for
{0:d} lists of tuples, with each list containing the number
of tuples show under the 'List Length' heading. Values are shown as
means and 95% confidence intervals from {1:d} Monte Carlo trials. 
Note that while `max_tup_answer()` is the most efficient, in the case of ties
it does not return the same result as the others. 
""".format(n_lists, n_mc)
tb = tab.rsplit('\n')
tb.insert(1, cap)
tab = '<center>'
for i, line in enumerate(tb):
    tab += line
    if i < (len(tb) - 1):
        tab += '\n'
tab += '</center>'
display(HTML(tab))

# In the results, note the scaling as the list length increases from 100 to
# 500. The original (`max_tup_op`) and the "code review" (`max_tup_cr()`)
# take \~20-25 times longer (quadratic scaling) while the remaning methods
# scale approximately linearly (\~5 times longer).

# ## Question 3
# In this question we clean an append demographic and dentition data from
# several cohorts of the NHANES data. 

# file location: -------------------------------------------------------------
path = './'

# column maps: ---------------------------------------------------------------
# new names for demo cols
demo_cols = {
    'SEQN': 'id',
    'RIDAGEYR': 'age',
    'RIAGENDR': 'gender',
    'RIDRETH3': 'race',
    'DMDEDUC2': 'education',
    'DMDMARTL': 'marital_status',
    'RIDSTATR': 'exam_status',
    'SDMVPSU': 'psu',
    'SDMVSTRA': 'strata',
    'WTMEC2YR': 'exam_wt',
    'WTINT2YR': 'interview_wt'
    }

# new names for ohx cols
ohx_cols = {'SEQN': 'id', 'OHDDESTS': 'dentition_status'}
tc_cols = {'OHX' + str(i).zfill(2) + 'TC':
           'tc_' + str(i).zfill(2) for i in range(1, 33)}
ctc_cols = {'OHX' + str(i).zfill(2) + 'CTC':
            'ctc_' + str(i).zfill(2) for i in range(2, 32)}
_, _ = ctc_cols.pop('OHX16CTC'), ctc_cols.pop('OHX17CTC')

ohx_cols.update(tc_cols)
ohx_cols.update(ctc_cols)

# columns to convert to integer
demo_int = ('id', 'age', 'psu', 'strata')
ohx_int = ('id', )

# levels for categorical variables
demo_cat = {
    'gender': {1: 'Male', 2: 'Female'},
    'race': {1: 'Mexican American',
             2: 'Other Hispanic',
             3: 'Non-Hispanic White',
             4: 'Non-Hispanic Black',
             6: 'Non-Hispanic Asian',
             7: 'Other/Multiracial'
             },
    'education': {1: 'Less than 9th grade',
                  2: '9-11th grade (Includes 12th grade with no diploma)',
                  3: 'High school graduate/GED or equivalent',
                  4: 'Some college or AA degree',
                  5: 'College graduate or above',
                  7: 'Refused',
                  9: "Don't know"
                  },
    'marital_status': {1: 'Married',
                       2: 'Widowed',
                       3: 'Divorced',
                       4: 'Separated',
                       5: 'Never married',
                       6: 'Living with partner',
                       77: 'Refused',
                       99: "Don't know"
                       },
    'exam_status': {1: 'Interviewed only',
                    2: 'Both interviewed and MEC examined'
                    }
    }

ohx_cat = {
    'dentition_status': {1: 'Complete', 2: 'Partial', 3: 'Not Done'}
    }

tc = {
      1: 'Primary tooth present',
      2: 'Permanent tooth present',
      3: 'Dental Implant',
      4: 'Tooth not present',
      5: 'Permanent dental root fragment present',
      9: 'Could not assess'
      }

ctc = (
 {
  'A': 'Primary tooth with a restored surface condition',
  'D': 'Sound primary tooth',
  'E': 'Missing due to dental disease',
  'F': 'Permanent tooth with a restored surface condition',
  'J':
    'Permanent root tip is present but no restorative replacement is present',
  'K': 'Primary tooth with a dental carious surface condition',
  'M': 'Missing due to other causes',
  'P':
    'Missing due to dental disease but replaced by a removable restoration',
  'Q':
    'Missing due to other causes but replaced by a removable restoration',
  'R':
    'Missing due to dental disease but replaced by a fixed restoration',
  'S': 'Sound permanent tooth',
  'T':
    'Permanent root tip is present but a restorative replacement is present',
  'U': 'Unerupted',
  'X': 'Missing due to other causes but replaced by a fixed restoration',
  'Y': 'Tooth present, condition cannot be assessed',
  'Z': 'Permanent tooth with a dental carious surface condition'
 })

# read data: -----------------------------------------------------------------
base_url = 'https://wwwn.cdc.gov/Nchs/Nhanes/'
cohorts = (
    ('2011-2012', 'G'),
    ('2013-2014', 'H'),
    ('2015-2016', 'I'),
    ('2017-2018', 'J')
    )
# demographic data
demo_file = path + '/demo.feather'

if exists(demo_file):
    demo = pd.read_feather(demo_file)
else:
    demo_cohorts = {}
    for cohort, label in cohorts:

        # read data and subset columns
        url = base_url + cohort + '/DEMO_' + label + '.XPT'
        dat = pd.read_sas(url).copy()
        dat = dat[list(demo_cols.keys())].rename(columns=demo_cols)

        # assign cohort and collect
        dat['cohort'] = cohort
        demo_cohorts.update({cohort: dat})

    # concatenate and save
    demo = pd.concat(demo_cohorts, ignore_index=True)
 
    # categorical variables
    for col, d in demo_cat.items():
        demo[col] = pd.Categorical(demo[col].replace(d))
    demo['cohort'] = pd.Categorical(demo['cohort'])

    # integer variables
    for col in demo_int:
        demo[col] = pd.to_numeric(demo[col], downcast='integer')

    demo.to_feather(demo_file)
demo.shape

# dentition data
ohx_file = path + '/ohx.feather'

if exists(ohx_file):
    ohx = pd.read_feather(ohx_file)
else:
    ohx_cohorts = {}
    for cohort, label in cohorts:

        # read data and subset columns
        url = base_url + cohort + '/OHXDEN_' + label + '.XPT'
        dat = pd.read_sas(url).copy()
        dat = dat[list(ohx_cols.keys())].rename(columns=ohx_cols)

        # assign cohort and collect
        dat['cohort'] = cohort
        ohx_cohorts.update({cohort: dat})
 
    # concatenate
    ohx = pd.concat(ohx_cohorts, ignore_index=True)

    # categorical variables
    for col, d in ohx_cat.items():
        ohx[col] = pd.Categorical(ohx[col].replace(d))
    
    for col in tc_cols.values():
        ohx[col] = pd.Categorical(ohx[col].replace(tc))

    # ctc columns get read in as bytes
    for col in ctc_cols.values():
        ohx[col] = ohx[col].apply(lambda x: x.decode('utf-8'))
        ohx[col] = pd.Categorical(ohx[col].replace(ctc))

    ohx['cohort'] = pd.Categorical(ohx['cohort'])
    # integer variables
    for col in ohx_int:
        ohx[col] = pd.to_numeric(ohx[col], downcast='integer')

    # save
    ohx.to_feather(ohx_file)
ohx.shape
# ---

# The demographic and dentition datasets just created have 39,156 and 35,909 cases, respectively.
