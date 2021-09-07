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
    header: <a href="#/slide-0-0"> <h3> Stats 507 -  Python Basics </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Python Basics
*Stats 507, Fall 2021*

James Henderson, PhD  
September 2, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Overview
  - <a href="#/slide-2-0"> Semantics </a>
  - <a href="#/slide-5-0"> (Strong) scalar types </a>
  - <a href="#/slide-12-0"> Indentation</a>
  - <a href="#/slide-13-0"> Functions </a>
  - <a href="#/slide-14-0"> Object Oriented </a>
  - <a href="#/slide-15-0"> Takeaways </a>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Interpreted
  - Python is an interpreted language.
  - This aids in interactive exploration.
  - But also means the order in which you run code (cells) matters. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Assignment
 - Assign named variables to values (objects) using `=`. 
 - We also say the variable name is *bound* to its value.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = 42
instructor = 'Dr. Henderson'
pi = 3.14
yeti = False
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Assignment
 - Assignment uses *dynamic referencing*. 
 - The type/class is determined from the value, not declared.
 - Type/class information belongs to the data, not the name
   bound to that data. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Aliasing
 - When we assign one variable to another, we do not 
   (usually) copy the associated data.
 - Instead we simply bind a new name to the same instance or
   location in memory. 
 - The two variables are said to be *aliased*. 
 - Primarily important for *mutable* classes. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Aliasing
 - Here is an example using the *mutable* `list` class. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = [42]; y = x; x.append('Jackie Robinson')
print(y)
y.append('Mariano Rivera')
print(x)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Aliasing
 - Test if two variables are aliased using `is`. 
 - Use a *mutable* object's `.copy()` method to copy its 
   values to a new location. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(x is y)
x = [42]
y = x.copy()
print(x is y)
x.append('Jackie Robinson')
print(y)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Scalar Types
 - Python has several "scalar" types in its built-in library: 
   `int`, `float`, `str`, `bool`, `None`, `bytes`. 
 - Other types are defined in external libraries such as Numpy. 
 - Cast between (some) types using functions of the same name.
 - Scalars are *immutable*. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = 5e-1
print(float(x))
print(str(x))
print(bool(x))
print(bool(int(x)))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Scalar Types
 - Check if a variable is of a particular type using `isinstance()`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = 5e100
print(isinstance(x, float))
print(isinstance(x, int))
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Numeric Types
 - Python's integer type `int` can hold arbitrarily large integers.
 - The `float` type is a double-precision (64-bit) floating point number.
 - Do math with (arithmetic) binary operators: 
   `+`, `-`, `*`, `/`, `//`, `%`, `**`. 
 - Floating point arithmetic is approximate.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(13 / 2)  # thanks Python 3
print(13 // 2) # integer divsion
print(13 % 2)  # mod
x = 2 ** 0.5
print(x ** 2 - 2)
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Boolean types
  - The `bool` type holds logical values.
  - In Python, these are `True` and `False`. 
  - Comparison operators return type `bool`.
  - Boolean operators act on and return type `bool`.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
eps1 = 1e-8
eps2 = 1e-16
z = (2 ** 0.5) ** 2 - 2
b1 = z < eps1
b2 = z > eps2
b1 and b2
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Ternary expressions
  - Python supports *ternary* (three-part) expressions in boolean operations.
  - Will reappear elswehere, e.g. conditional execution. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print((eps1 > z) and (z > eps2))
eps2 < z < eps1
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# String types
- Python's built in string type is flexible and has 
  a number of associated methods.
- One especially useful method is `.format()`.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
x = 42; n = 100
phat = x / n
se = (phat * (1 - phat) / n) ** 0.5
lwr, upr = phat - 1.96 * se, phat + 1.96 * se
ci_str = "{0:.1f}% (95% CI: {1:.0f}-{2:.0f}%)"
pretty = ci_str.format(100 * phat, 100 * lwr, 100 * upr)
pretty
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Format Example
 - Can also use the prefix `f` for a "glue" like syntax.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
from IPython.display import Markdown
Markdown(f'''
 > Life is {pretty} towels.
 >
 > --Unknown. 
 ''')
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Strong types
- Python is *strongly-typed* ...
- 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
try:
    5 + 'phi' 
except: 
    print('Error')
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Strong types
- Python is *strongly-typed* ...
- ... though `float` and `int` types play nicely.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
n = 5; phi = (1 + 5 ** 5e-1) / 2
print(isinstance(n, int))
print(isinstance(phi, float))
print(n * phi)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Indentation
 - Python uses indentation to structure code ... 
 - <p class='fragment'>
   ... unlike many other languages, e.g. R, C++, which use braces `{}`.
   </p>
 - <p class='fragment'> In Python, indentation is functional, 
    not just good style. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Indentation 
 - Functional whitespace makes python more readable to humans ... 
 - <p class='fragment'>
    ... but also potentially harder to debug (in the beginning). 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Indentation 
 - Limit difficulties by following the convention of indenting with 
   **4 spaces**. 
 - <p class='fragment'>
    Avoid tabs, `\t`,  but use the tab key when your editor is enabled
    to translate. 
  </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Indentation 
 - A colon `:` is used to denote the start of an indented block.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
k = 0
for i in range(10):
    k += i
print(k)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Functions
- Recognize function calls by `()` after the function name. 
- Functions take 0 or more *arguments*.
- Some arguments are required, others have *default values* and 
  can be omitted. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(round(3.141592653589793))
print(round(3.141592653589793, ndigits = 1))
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Functions
- Agruments can be passed by *position* or *keyword*. Use position for
  the most common arguments, and keywords otherwise. 
- Positional arguments must precede keyword arguments. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
print(round(3.141592653589793, ndigits=2))
print(round(3.141592653589793, 3))
# error
# round(digits = 2, 3.141592653589793)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Functions
 - <p class='fragment highlight-red'>
   ... are one of the most useful programming contructions.
   </p>
 - <p class='fragment highlight-red'>
   ... allow you to name and reuse blocks of code.
   </p>
 - <p class='fragment highlight-red'>
   ... help you to break complex problems into simpler parts. 
   </p>
 - <p class='fragment highlight-red'>
    ... make your code more readable. 
   </p>
 - <p class='fragment' >
   Rule of thumb: if you copy-and-paste the same code more than once, 
   it's probably better to encapsulate that code into a function. 
   </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Functions
 - Use the `def` keyword to define a new function.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
def n_vowels(s):
    n = 0
    for v in ['a', 'e', 'i', 'o', 'u']:
        n += s.count(v)
    return(n)
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Functions
 - Include a docstring on *all* named functions. 
 - Here's a template from Spyder - use this template every time.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
def s(x, y = 0):
    """
    Describe your function's purpose concisely. 

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y : TYPE, optional
      DESCRIPTION. The default is 0.

     Returns
     -------
     None.

    """
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Python is Object-Oriented
 - Everything in Python is an object. 
 - Objects are instances of a class with internal data and (usually)
   associated methods.
 - <p class='fragment'> 
    Methods are functions that belong to objects and have access to
    associated data. 
   </p>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Method Calls
  - Method calls take the form `object.method()`.
  - Here we create an object `book` of class `str` ...
  - ... and then call its `title()` method.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
book = "the hitchhiker's guide to the galaxy"
print(book.title())
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways
 - Python is an interpreted, strongly-typed language that uses
   dynamic references. 
 - Hierarchy is denoted using indentation(!) with `:` denoting
   the start of an indented block. 
 - Python is object-oriented. Use methods, but 
   follow a functional programming style.  
 - Use functions to keep DRY (and don't forget the docstring). 
<!-- #endregion -->
