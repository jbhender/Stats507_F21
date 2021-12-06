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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Regex </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Regular Expressions
*Stats 507, Fall 2021*

James Henderson, PhD  
October 21, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
  - [Regular Expressions](#/slide-2-0)
  - [Examples and Concepts](#/slide-4-0)
  - [Regex Crossword](#/slide-11-0)
  - [Takeaways](#/slide-12-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Regular Expressions
  - *Regular expressions* are a way to describe patterns in strings.
  - Patterns may be abstract. 
  - Common *regex* vocabulary ...
  - ... but details differ between implementations and standards. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Imports
  - Here are the imports we will use in these slides. 
  - `re` is a built-in Python module for regular expressions
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
import numpy as np
import pandas as pd
import re
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Example
- The file `fruit.txt` is a list of fruits distributed with R's 
  stringr library. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df = pd.read_csv('./fruits.txt')
fruits = list(fruits_df['fruit'].values)
fruits_df.head()
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Pandas
- Pandas has several vectorized string functions that understand
  regular expressions:
  + `contains`, 
  + `match`, `fullmatch`,
  + `count`, 
  + `findall`, 
  + `replace`, 
  + `extract`, 
  + `split`.
<!-- #endregion -->

```python
fruits_df[fruits_df['fruit'].str.match('^a')]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Search / Contains
- `str.contains()` returns a bool indicating whether a pattern
  is found in each entry of a string series.
- It is based on `re.search()`. 
- Find all two-word fruits by searching for a space. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
#[re.search(' ', fruit) is not None for fruit in fruits]
two_word_fruits = []
for fruit in fruits:
    if re.search(' ', fruit):# is not None:
        two_word_fruits.append(fruit)
two_word_fruits
```
<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Search / Contains
- Find all two-word fruits by searching for a space. 
- Let's use this method to explore regex concepts. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains(' ')]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Regex Concepts - Simple search
- Find all fruits with an "a" anywhere in the word. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('a')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Anchors
- A caret `^` indicates the match must come at the 
  beginning of the string.  
- Find all fruits beginning with an "a".
- This is known as an *anchor*.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('^a')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Anchors
- A dollar sign `$` indicates the match must come at the 
  end of the string.  
- Find all fruits ending with an "a".
- This is also known as an *anchor*.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('a$')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Anchors in Pandas
- Pandas also has vectorized `.startswith()` and `.endswith()`
  methods.  
- Find all fruits starting or ending with an "a".
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[
  np.logical_or(
    fruits_df['fruit'].str.startswith('a'),
    fruits_df['fruit'].str.endswith('a')
  )
]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Or
- A bar `|` can be used as an *or* operator in regular
  expressions.   
- Find all fruits starting or ending with an "a".
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('^a|a$')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Bracket Expressions
- Multiple acceptable matches can be collected into a 
  bracket expression. 
- Find all fruits starting with a vowel.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('^[aeiou]')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Bracket Expressions
- Inside a bracketed expression, a caret `^` means to
  match anything but the listed characters.  
- Find all fruits ending with a consonant other than n, r, or t.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('[^aeiounrt]$')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Ranges
- Bracket expressions understand the following ranges:
  + `[a-z]` - lowercase letters
  + `[A-Z]` - uppercase letters
  + `[0-9]` - digits
- These can be used together, e.g. `[A-Za-z0-9]`. 
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Quantifiers
- Numbers in braces `{}` can be used to specify a 
  a specific number (or range) of matches. 
- Find all fruits ending with two consecutive consonants
  other than n, r or t.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('[^aeiounrt]{2}$')]
#fruits_df[fruits_df['fruit'].str.contains('[^aeiour]{2, 3}$')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Quantifiers
- How would we find all fruits with two consecutive vowels? 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
#fruits_df[fruits_df['fruit'].str.contains('')]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Wild Card and Quantifiers
- The quantifier `*` indicates 0 or more matches, `?` indicates
  0 or 1 matches, and `+` indicates one or more matches.
- A *dot* (or period) `.` can be used to match any single character.
- These are often used together, e.g. `.*` matches anything but a   
  newline (`\n`) character.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Wild Card Example
- Find all fruits with two consecutive vowels, twice, separated
  by a single consonant. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
rgx0 = '[aeiou]{2}.[aeiou]{2}'
fruits_df[fruits_df['fruit'].str.contains(rgx0)]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Regex Concepts - Wild Card with Quantifier Example
- Find all fruits with two consecutive vowels, twice, separated
  by one or more consonants. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
first = True
if first:
    rgx1 = '[aeiou]{2}.+[aeiou]{2}'
    fruits_df[fruits_df['fruit'].str.contains(rgx1)]
else:
    fruits_df[
      np.logical_and(
        fruits_df['fruit'].str.contains(rgx1),
        ~fruits_df['fruit'].str.contains(rgx0)
      )

```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Escape sequences
- Characters with special meanings like `.` can be escaped
  using a backslash `\`, e.g. `\.`.
- Some can also be placed in brackets `[.]`. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits.append('507@umich.edu')
print(fruits[len(fruits) - 1])

for f in fruits:
    if re.search('\.', f):
        print(f)
    if re.search('[.]', f):
        print('[' + f + ']')
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Escape sequences
- Because `\` is used as an escape character, a literal backslash 
  `\`needs to be escaped. 
- Commonly appears in file paths on Windows. 
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits.append(r'C:\path\file.txt')
fruits[len(fruits) - 1]
```

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Escape sequences
> To avoid unwanted escaping with \ in a regular expression, 
> use raw string
> literals like r'C:\x' instead of the equivalent 'C:\\x'.
> 
>   -- Wes McKinney
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
for f in fruits:
    if re.search(r'\\', f):
        print(f)
    if re.search('\\\\', f):
        print('ugh!')
        print(f)
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Character Classes
- Various escape sequences can be used to represent specifc classes
  of characters.
  + words: `\w` roughly `[a-zA-z0-9]+`,
  + non-words: `\W`,
  + digits: `\d = [0-9]`, 
  + non-digits: `\D`,
  + whitespace: `\s`,
  + non-whitespace: `\S`.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('\s')]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Groups
- Use parantheses to create groups.  
- Groups can be referred back to using an escaped integer. 
- Let's find all fruits with:
  + a double letter
  + a double letter other than "r"
  + a double letter at the end of the word.
<!-- #endregion -->

```python slideshow={"slide_type": "code"}
fruits_df[fruits_df['fruit'].str.contains('(.)\\1')]
#fruits_df[fruits_df['fruit'].str.contains('([^r])\\1')]
#fruits_df[fruits_df['fruit'].str.contains('(.)\\1$')]
```

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Regex Crosswords 
- Let's practice regular expression concepts by solving 
  the intermediate puzzles from <https://regexcrossword.com>.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways
- Regular expresions are used to describe patterns in strings.
- Use these patterns to search, find and replace, extract or 
  otherwise work with strings. 
- Use regular expressions whenever you can. 
<!-- #endregion -->
