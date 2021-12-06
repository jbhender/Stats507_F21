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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - OOP </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Object Oriented Programming
*Stats 507, Fall 2021*

James Henderson, PhD  
November 23, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
  - [Object Oriented Programing](#/slide-2-0)
  - [Classes](#/slide-3-0)
  - [Methods](#/slide-4-0)
  - [Attributes](#/slide-5-0)
  - [Inheritance](#/slide-6-0)
  - [Takeaways](#/slide-7-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Object Oriented Programming
> Object-oriented programming (OOP) is a programming paradigm based on the 
> concept of "objects", which can contain data and code: data in the form of 
> fields (often known as attributes or properties), and code, in the form of
> procedures (often known as methods). 

<https://en.wikipedia.org/wiki/Object-oriented_programming>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Object Oriented Programming
> A feature of objects is that an object's own procedures can access and often
> modify the data fields of itself (objects have a notion of this or self).
> In OOP, computer programs are designed by making them out of objects that 
> interact with one another.

<https://en.wikipedia.org/wiki/Object-oriented_programming>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Classes
 - A *class* is a programer-defined object type. 
 - Define a class using the `class` keyword and an indented body. 
 - Class names use `CamelCase` by convention. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """
    pass
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Constructor
 - The class name is callable as a *constructor* function that
   creates an *instance* of the class. 
 - Modify the constructor by defining an `.__init__()` method. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))

s1 = Secret(42)
print(s1)    
assert isinstance(s1, Secret)
s1
```
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Methods
 - *Methods* are functions that belong to a class.  
 - Method calls have access to a class's data -- attributes and other 
   methods. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Dunder Methods
 - "*Dunder*" methods defined with a double underscore have a special role 
    and are how Python handles *method overloading*. 
 - The `__str__` defines a simple string representation of an object and
   controls how it prints.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))
    
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(self.hidden)    

s2 = Secret(42)
print(s2)
s2
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Dunder Methods
 - The `__repr__` method provides an official representation of the object and
   controls how it is represented without explicit printing.  

 > Called by the `repr()` built-in function to compute the “official” string
 > representation of an object.  
 > If at all possible, this should look like a valid Python expression that
 > could be used to recreate an object with the same value ... 

 <https://docs.python.org/3/reference/datamodel.html#descriptors>
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))
    
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(self.hidden)    
    
    def __repr__(self):
        """Official string representation"""
        return(self.hidden)

s3 = Secret('Life')
s3
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
##  Methods
 - More often we define methods intended to be used with instances
   of our class directly. 
 - Here we define a `.reveal()` method to return the value of the secret. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))
    
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(self.hidden)    
    
    def __repr__(self):
        """Official string representation."""
        return(self.hidden)

    def reveal(self):
        """
        Reveal the secret
        """
        return(self.value)    

s5 = Secret('the Universe')
print(s5)
s5.reveal() 
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Attributes
 - In general, a user can assign arbitrary attributes to a class.  
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
s5.arbitrary = 42
s5.arbitrary
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Attributes
 - In general, a user can assign arbitrary attributes to a class.  
 - We can restrict this by defining `__slots__` -- a string or iterable of 
   strings limiting the allowed attributes. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    __slots__ = ('value', 'hidden')
    
    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))
    
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(self.hidden)    
    
    def __repr__(self):
        """Official string representation."""
        return(self.hidden)

    def reveal(self):
        """
        Reveal the secret
        """
        return(self.value)    

s6 = Secret("You've got mail!")
try:
    s6.arbitrary = 42
except:
    print("Secret has no attribute 'arbitrary'.")
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Attributes as Metadata
 - We can use attributes to store metadata. 
 - Here we modify methods based on whether the instance has been 
   previously revealed. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class Secret:
    """
    Hold a string or number but display a placeholder when printing.
    """

    __slots__ = ('value', 'hidden', 'secret')
    
    def __init__(self, x):
        """
        Initialize an object of class Secret.
        """
        self.value = x
        self.hidden = 'x' * len(str(x))
        self.secret = True
    
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        if self.secret:
            return(self.hidden)    
        else:
            return(self.value)
    
    def __repr__(self):
        """Official string representation."""
        return(self.__str__())

    def reveal(self):
        """
        Reveal the secret
        """
        self.secret = False
        return(self.value) 

    def hide(self):
        """
        Make a revealed secret hidden again. 
        """
        self.secret = True
        return(None)

s_new = Secret("You've got mail!")
x = s_new.reveal()
s_new.hide()
(x, s_new)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Inheritance
 - A *child* (*derived*) class is a special case of a *parent* (*base*) class.
 - The child class *inherits* from the parent class:
   + it can access methods from the parent class,
   + it should have all attributes associated with the parent class. 
 - Using inheritance makes code easier to maintain by limiting repetition. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Derived Classes
 - Define a *derived* class by passing the name of the *base* class
   in parentheses within the `class` statement, e.g. `class Derived(Base)`.
 - Inherited methods (e.g. `.reveal()`) only need to be redefined if we wish 
   to modify them. 
 - It may be better, here, to add `str()` to the base `Secret` class for the
   `__str__()` and `__repr()__` methods. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class SecretTuple(Secret):
    """
    A secret tuple is a tuple of secrets with more methods. 
    """
    
    def __init__(self, x):
        """
        Initialize a SecretTuple as a tuple of Secrets. 
        """
        assert isinstance(x, tuple)
        self.value = x
        self.hidden = tuple(Secret(x[i]).hidden for i in range(len(x)))
        
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(str(self.hidden))
    
    def __repr__(self):
        """Official string representation."""
        return(str(self.hidden))

s7 = SecretTuple(('Life', 'the universe', 'everything'))
assert isinstance(s7, SecretTuple) and isinstance(s7, Secret) 
[s7, s7.reveal()]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Inheritance
 - Is `__slots__` inherited? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
try:
    s7.arbitrary = 42
    print(s7.arbitrary)
except:
    print("Secret has no attribute 'arbitrary'.")
```


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Inheritance
 - Is `__slots__` inherited? 
 - A derived class has the attributes of the base class, but may have 
   additional attributes as well. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class SecretTuple(Secret):
    """
    A secret tuple is a tuple of secrets with more methods. 
    """
    __slots__ = ('partial_secret')

    def __init__(self, x):
        """
        Initialize a SecretTuple as a tuple of Secrets. 
        """
        assert isinstance(x, tuple)
        self.value = x
        self.hidden = tuple(Secret(x[i]).hidden for i in range(len(x)))
        
    def __str__(self):
        """
        Display 'hidden' value when a Secret is printed.
        """
        return(str(self.hidden))
    
    def __repr__(self):
        """Official string representation."""
        return(str(self.hidden))

s8 = SecretTuple((4, 9, 21))
try:
    s8.arbitrary = 42
    print(s8.arbitrary)
except:
    print("Secret has no attribute 'arbitrary'.")

try:
    s8.secret = False
    print(s8)
except:
    print("Secret has no attribute 'arbitrary'.")    
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Inheritance
 - Inheritance is asymmetrical, `.reveal_part()` is not available to
   objects of class `Secret()`. 
 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class SecretTuple(Secret):
    """
    A secret tuple is a tuple of secrets with more methods. 
    """
    
    __slots__ = ('partial_secret')

    def __init__(self, x):
        """
        Initialize a SecretTuple as a tuple of Secrets. 
        """
        assert isinstance(x, tuple)
        self.value = x
        self.hidden = tuple(Secret(x[i]).hidden for i in range(len(x)))
        self.secret = True
        self.partial_secret = [True for i in range(len(x))]

    def __str__(self):
        hidden_parts = tuple(
          self.value[j] if s else self.hidden[j] for j in partial_secret
        )
        return(str(hidden_parts))
    
    def __repr__(self):
        return(self.__str()__)
    
    def __getattr__(self, x):
        if x == 'value':
            return(x.hidden)
        else:
            return(self.x)
    
    def reveal_part(self, i):
        """
        Partially reveal the secret. 
        """
        try:
          i_iter = iter(i)
        except:
            i = (i, )
        part = (
            self.value[j] if j in i else h for j, h in enumerate(self.hidden)
        )
        for j in i:
          partial_secret[i] = False
 
        return(tuple(part))

s8 = SecretTuple(('Life', 'the universe', 'everything'))
s8.reveal_part(1) 
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Indexing
  - Define the "dunder" method `__getattr__` to make an object *subsettable*
    using brackets. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
class SecretTuple(Secret):
    """
    A secret tuple is a tuple of secrets with more methods. 
    """
    
    def __init__(self, x):
        """
        Initialize a SecretTuple as a tuple of Secrets. 
        """
        assert isinstance(x, tuple)
        self.value = x
        self.hidden = tuple(Secret(x[i]).hidden for i in range(len(x)))
        
    def __str__(self):
        return(str(self.hidden))
    
    def __repr__(self):
        return(str(self.hidden))
    
    def __getattr__(self, x):
        """
        Subset a SecretTuple using a tuple of indices or an integer (no slices).
        """
        if x == 'value':
            return(x.hidden)
        else:
            return(self.x)
    
    def reveal_part(self, i):
        """
        Partially reveal the secret. 
        """
        try:
          i_iter = iter(i)
        except:
            i = (i, )
        part = (
            self.value[j] if j in i else h for j, h in enumerate(self.hidden)
        )
 
        return(tuple(part))

s10 = SecretTuple(('Life', 'the universe', 'everything'))
assert isinstance(s9[1], Secret)
s10[1]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Base Methods
 - Use `.super()` to access base methods within the definition of
   a derived class. 
 - Let's use the base `.hide()` method in conjunction with a specific 
   `.hide()` method for the `SecretTuple()` class. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
 - Use OOP when its necessary to encapsulate both data and methods. 
 - Prefer a functional or procedural style otherwise. 
<!-- #endregion -->

