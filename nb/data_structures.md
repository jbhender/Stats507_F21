---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise,markdown
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  markdown:
    extensions: footnotes
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Built-In Data Structures </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Python's Built-In Data Structures
*Stats 507, Fall 2021*

James Henderson, PhD  
September 7 & 9, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Overview 
 - <a href="#slide-1-0"> tuple </a>
 - <a href="#slide-8-0"> \[list\] </a>
 - <a href="#slide-13-0"> {"dict": dictionary} </a>
 - <a href="#slide-19-0"> sequence functions </a>
 - <a href="#slide-23-0"> {set} </a>
 - Slide contents based on Chapter 3 of *Python for Data Analysis*, 
   vol 2 by Wes McKinney.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# <a name="tuple"> Tuples </a>
  - Tuples are fixed-length sequences of python objects.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Constructing Tuples
  - Construct tuples using a comma-separated sequence.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tup = 'pi', ['py'], 'pie'
print(tup)
print(type(tup))
print(tup.__class__)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Constructing Tuples
  - Or use `tuple()` to convert from another sequence object
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(
    tuple("data")
)
```

```python slideshow={"slide_type": "fragment"}
print(tuple(["py", "thon"]))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Tuples - Indexing and Immutability
  - Index into tuples using `[]`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = tup[0]
print(x)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Tuples - Indexing and Immutability
  - Tuples are immutable ... 
  - <p class="fragment">
      ... but their contents need not be.
    </p>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
try:
    tup[1] = "python"
except:
    print("Tuples are immutable")
```

```python slideshow={"slide_type": "fragment"}
tup[1].append("3.9")
print(tup)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Tuples - Operators
  - Tuples can be concatenated using `+` ... 
  - <p class='fragment'>
    ... or replicated using `*`. 
    </p>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tup2 = tup + tup
print(tup2)
```

```python slideshow={"slide_type": "fragment"}
tup3 = 3 * tup 
print(tup3)
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Tuples - Unpacking 
  - A tuple can be *unpacked* by assiging to a tuple-like expression.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
answer = 42, ("life", "universe", "everything")
a1, a2 = answer
print(a1)
print(a2)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Tuples - Unpacking
  - This works for nested tuples as well. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
answer = 42, ("life", "universe", "everything")
a1, (a2_1, a2_2, a2_3) = answer
print(a2_2)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Tuples - Swapping Variables
  - You can swap variables by unpacking a transitory tuple.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
a, b = 42, 3.14
b, a = a, b
print((a, b))
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Tuples - `*_`
  - Functions often use tuples to return multiple values.
  - Use `*_` to capture unwanted values ...
  - <p class="fragment">... or `*name` to unpack into a list `name`. </p>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
num, (word1, *_) = answer
print(num)
print(word1)
```

```python slideshow={"slide_type": "fragment"}
print(_)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Tuple methods 
<div class="row">
  <div class="column">
    <p> Tuples have few associated methods because they are immutable. </p>
    <p> One useful method is, `count()`. </p>
  </div>
  <div class="column">
    <img src='img/pipe.jpeg' align='center'></img>
    <small align='center'> 
     https://en.wikipedia.org/wiki/File:MagrittePipe.jpg 
    </small>
  </div>
</div>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
tuple("Leci n'est pas une pipe.").count('e')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Lists
 - Lists are Python's most flexible built-in data structure.  
 - Create lists using `[]` or the `list()` function.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
my_list = (
    ["Leci n'est pas une pipe.", 
     (1, 2, 3, 5, 7, 11), 
     range(3)
     ])
for x in my_list:
    print(type(x))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# List indexing and mutability
 - Index into a list to access, set, or update an item
   in a given *position* using `[]`. 
 - List are *mutable* and can be changed in place.  
 - The `list()` function can be used to instantiate 
   iterators (or generators). 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(my_list[1:2])
list(my_list[2])
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# List methods
 - Removing elements: `.pop()`, `.remove()`.
 - Adding elements: `.append()`, `.insert()`, `.extend()`
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(my_list.pop(0)) # a position
my_list.remove(range(0, 3)) # takes a value
print(my_list)
my_list.append((17, 19, 23, 31, 37))
print(my_list)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# List methods
 - Adding elements: `.append()`, `.insert()`, `.extend()`
 - Concatenate lists with `+`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
prime = list(my_list[0]) + list(my_list[1])
prime.insert(6, 13)
prime.extend([43, 47, 53])
prime
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# List slices
 - Lists, like most *sequence objects*, support `start:stop` slicing.
 - `[start, stop)`: `0:n` returns the first `n` elements. 
 - `start` defaults to 0, `stop` to the length of the list. 
 - Negative indexing is supported. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(prime[3:8])
prime[16:17] = [57, 59]
p = prime
(p[:3] == p[0:3]) & (p[3:len(p)] == p[3:]) & (p[len(p) - 1] == p[-1])
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# List slices
 - A second colon can be used to specify a step size. 
 - Specifying a step of `-1` reverses the list. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(prime[1::2])
print(prime[::-1])
print(prime[0:-1][::-1])
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# List comprehensions
- List comprehensions allow you to concisely create new lists.
- Basic syntax: `[expr for val in collection if condition]`
- Use to make your code easier to read, don't overuse. 
- Work with other sequence objects as well. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
a = [x for x in my_list if isinstance(x, tuple)]
b = []
for x in my_list:
    if isinstance(x, tuple):
        b.append(x)
a == b
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Exercise
- Place the lists `a`, `b`, `c`, `d`, and `e` below into groups such that all
  members of the group have the same value.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = list(range(10))
y = list(range(0, 10, 2)) #[0, 2, 4, 6, 8]

a = y[::-1]
b = x[1:4:2]
c = x[::2][::-1]
d = x[x[1]:y[2]:y[1]]
e = [i
     for i in x
     if 0 < i < 4 and i % 2 == 1] 
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# List comprehensions
- List comprehensions can be *nested* but be wary of
  impact on readability. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
flat1 = [
  x
  for tup in my_list
  if isinstance(tup, tuple) 
  for x in tup]

flat2 = []
for tup in my_list:
    if isinstance(tup, tuple):
        for x in tup:
            flat2.append(x)

flat1 == flat2 
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Dicts
 - The dictionary class `dict` is used to associate
   *key-value* pairs.
 - Dictionaries are also known as *associative arrays* or
    *hash maps*.  
 - Collectively a *key-value* pair is called an *item*. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Dicts
> `dict` is likely the most important built-in Python
> data structure.
>
> <cite> --Wes McKinney </cite>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Creating objects of class dict
 - Create dictionaries using `{}` and a colon to 
   separate the key from the associated value ...
 - or using the `dict()` function.    
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
new_dict = {} # new_dict = dict()
res1 = {"mean": 4.2, "se": 0.21}
res2 = dict(mean=4.2, se=0.21)
res1 == res2  # same keys and values
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Hashed keys
 - A hash function maps an object to an integer.
 - Dictionary keys must be *hashable*, generally true for
   immutable classes. 
 - Because `dict` objects use a hash table, key lookup happens in
   constant time no matter how big the `dict` is. 
 - In contrast, value look up in lists is done by linear search. 
 - Keys have no inherent order.    
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Indexing dicts
 - Index into a `dict` (to access, set, or update) using `[]`. 
 - Access items with graceful fail using `.get()`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(res["mean"])
res["lwr"] = res["mean"] - 1.96 * res["se"]
print(res.get("upr"))
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Default values for dicts
 - You can specify what value `.get()` or `.pop()` 
   returns for a missing key.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(res.get("upr", "Not computed."))
x = {"a": 1, "b": 2, "c": 3}
for i in tuple("abcd"):    
    x.update({i: x.get(i, 0) + 1})
x
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# dict methods
- `.keys()`, `.values()`, `.items()`
- already seen `.get()` and `.update()`
- `.pop()`, `.copy()`
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
for k, v in d.items():
    print('{' + '{0}: {1}'.format(k, v) + '}')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# dict comprehension
- Analgous to list comprehension, but use key-expr: value-expr 
  at start. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
d = {i: np.sqrt(i) for i in range(10)}
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Built-in sequence functions
- Python has several built-in functions that simplify common
  patterns seen when working with lists:
    + `sorted`
    + `reversed`
    + `enumerate`
    + `zip`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Enumerate
- `enumerate()` returns (index, value) pairs for sequences. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = [4, 9, 10, 29, 42, 17]
d = {}
for idx, val in enumerate(x):
    d.update({val: idx})
d
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Sorted & reversed
- `sorted()` returns a list with a sorted copy of a sequence object. 
- `reversed()` returns a *generator* for iterating over items in a sequence
  in reversed order. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(sorted(d))
list(reversed(d.values()))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Zip
- `zip()` concatenates sequence objects element-wise into a "list" of tuples.  
- commonly used to iterate over multiple sequences
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
list(zip(d.keys(), d.values()))
for k, v in zip(d.keys(), d.values()):
    print('{' + '{0}: {1}'.format(k, v) + '}')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Sets
- Just as in math, a set is an unordered collection.
- The set class is mutable and akin to dictionary keys. 
- Methods for common set operations. 
- I'm going to skip over further discussion of sets, but this doesn't mean
  you shouldn't use them when appropriate. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
even = {x for x in range(0, 20) if x % 2 == 0}
div4 = {x for x in range(0, 20) if x % 4 == 0}
print(div4 < even)  # subset
print(div4 & even)  # intersection
print(div4 ^ even)  # symmetric difference
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways 1/3
 - Python has four primary built-in sequence types. 
 - Tuples (but not necessarily their contents) are *immutable*, 
   can be unpacked, and are a common structure for function returns.
 - Lists are flexible, *mutable*, and a good default structure. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways 2/3
 - `dicts` are a mutable set of *key-value* pairs, keys are unique
   and are hashed making random look-ups efficient.  
 - Sets are like dicts without values, and are useful for ...
   <p class='fragment'> wait for it ... </p> 
   <p class='fragment'> set logic. </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways 3/3
- Built in sequence functions: 
  + `enumerate`
  + `zip`
  + `sorted`
  + `reversed`
- Use "whenever you can" for concision and clarity. 
<!-- #endregion -->
