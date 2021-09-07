# ---
# jupyter:
#   jupytext:
#     cell_metadata_json: true
#     notebook_metadata_filter: rise,author,date,markdown
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   markdown:
#     extensions: footnotes
#   rise:
#     autolaunch: true
#     enable_chalkboard: true
#     header: <a href="#slide-0-0"> <h3> Stats 507 - Tables in Notebooks </a>
#     progress: true
#     scroll: true
#     theme: solarized
#     transition: convex
# ---

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Tables in Notebooks
# *Stats 507, Fall 2021*
#
# James Henderson, PhD  
# September 7, 2021

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Contents
#  - <a href="#slide-2-0"> Intro </a>
#  - <a href="#slide-6-0"> Pandas </a>
#  - <a href="#slide-7-0"> itable </a>

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # # Why?
# - Tables are a useful and efficient way to summarize key information.  
# - An initial table describing the data used in a notebook or research
#   article provides context for the results to follow. 

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Table 1
#  - "Table 1" is a short-hand throughout much of the research world
#     referring to a table of descriptive statistics at the start of a
#     manuscript's result section.
#  - "Table 1" is often organized so that columns correspond to levels 
#    of a key exposure. 
#  - See an example [here][1] (refer to *Table 2*). 
#
# [1]: 
# https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003730

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Tables vs Figures
# - Tables are generally more efficient for summarizing a series of 
#   discrete summaries. 
# - Figures are better for displaying key relationships and distributions. 
# - Tables and figures can be complementary to one another.  

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Modules
#   - For basic HTML or markdown tables, use pandas.
#     - HTML natively
#     - For markdown, `conda install tabulate`
#   - For interactive [DataTables][1], use the binding provided
#     by [itables][2].   
#   -  `pip install itables`
#
#   [1]: https://datatables.net/
#   [2]: https://mwouts.github.io/itables/

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Pandas Methods
# - `DataFrame` objects from pandas have methods:
#   - `.to_html()`
#   - `.to_markdown()`.

# + {"slideshow": {"slide_type": "code"}}
# %run s ring_df.py #constructs a data frame dat
print(dat.to_html())

# + [markdown] {"slideshow": {"slide_type": "subslide"}}
# # Pandas Methods
# - `DataFrame` objects from pandas have methods:
#   - `.to_html()`
#   - `.to_markdown()`.

# + {"slideshow": {"slide_type": "code"}}
# #%run string_df.py
print(dat.to_markdown())

# + [markdown] {"slideshow": {"slide_type": "subslide"}}
# # Displaying HTML
# - To render the HTML in the notebook, use `display()` and
#   `HTML()` from IPython.

# + {"slideshow": {"slide_type": "code"}}
from IPython.core.display import display, HTML
display(HTML('<h2> Hello <br> World!</h2>'))
display(HTML(dat.to_html(index=False)))

# + [markdown] {"slideshow": {"slide_type": "subslide"}}
# # Displaying Markdown
# - To render markdown in the notebook, use `display()` and 
#   `Markdown()` from IPython.

# + {"slideshow": {"slide_type": "code"}}
from IPython.core.display import display, Markdown
display(Markdown('## Hello <br> World!'))
display(Markdown(dat.to_markdown(index=False))) 

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Interactive Data Tables
# - [DataTables][1] is a plug-in for the jQuery Javascript library
#   that facilates interactivity such as search and pagination in HTML tables. 
# - Useful for large tables.  
#
# [1]: https://datatables.net/

# + [markdown] {"slideshow": {"slide_type": "subslide"}}
# # itables
#   - [itables][1] provides a Jupyter binding to the DataTables library 
#     for pandas DataFrames or series. 
#   - Use its `show()` function to display a pandas DataFrame as a 
#     datatable in your notebook. 
#
# [1]: https://mwouts.github.io/itables/

# + {"slideshow": {"slide_type": "code"}}
from itables import show
show(dat)

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # How it works
#  - This is out of scope for the course, but, if you're interested,
#    here's a [tutorial][1] describing how the binding works.
#
#  [1]: https://mcermak.medium.com/guide-to-interactive-pandas-dataframe-representation-485acae02946

# + [markdown] {"slideshow": {"slide_type": "slide"}}
# # Takeaways
#  - Give your notebooks a professional polish by including 
#    *nicely formatted* and thoughtfully structured tables.
#  - Unless you are explicitly discussing a dataset, avoid
#    code-oriented `variable_names`in favor of well chosen English. 
