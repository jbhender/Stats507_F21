---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise,author,date,markdown
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
    header: <a href="#slide-0-0"> <h3> Stats 507 - The Python Ecosystem </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# The Python Ecosystem
*Stats 507, Fall 2021*

James Henderson, PhD  
August 31, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Python 
<center> 
  <img src="https://www.python.org/static/img/python-logo@2x.png" width=50%> 
</center>

- Python is one of the most popular computing langauges. 
- It is used by both web developers and data scientists. 
- Python as a language is often characterized by its: readability, 
  simplicity, and explicitness. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Python 
- Python is an interpreted (as opposed to a compiled) language.
- Python is sometimes considered a "glue" language owing to its
  versatality. 
- Don't use the Python distributed with your OS.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Anaconda
 <center> 
   <img src="https://assets-cdn.anaconda.com/assets/resources/open-source/conda-artboard.svg" width=25%> 
  </center>
 
 - [Anaconda](https://www.anaconda.com/products/individual) is a popular
   Python distrubution that comes with:
   + a package and environment manager `conda` 
   + many preinstalled modules including:  Pandas, Numpy, Scipy, 
     IPython, and Jupyter.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Anaconda
 <center> 
   <img src="https://assets-cdn.anaconda.com/assets/resources/open-source/conda-artboard.svg" width=25%> 
  </center> 

  - Anacaonda Navigator provides graphical shortcuts to open 
    instances of Jupyter Notebooks, Spyder, and other tools. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Environments
- Environments allow us to isolate and manage dependencies
  + Environments can have different versions of key modules
  + ... or different versions of Python.  
  + Clone your environment to backup before updating dependencies.  

```
conda create --name 507b --clone 507 
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Conda Environments
- To get started, in your terminal application, `conda init [shell]`.
- Make sure `conda` is in your path.
- `venv` is an alternative. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Managing environments
 - list `conda env list`
 - create `conda create -n <env> python=3.9` 
 - activate `conda activate <env>`
 - deactivate `conda deactivate`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Managing dependencies
 - Python modules (libraries) can be managed with `conda`. 
 - `conda install`, `conda update` 
 - "Channels" (e.g. conda-forge) are locations where conda will look for modules.
 - `pip` is the primary alternative. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# IPython 
  <center> 
   <img src="https://ipython.org/_static/IPy_header.png" width=25%> 
 </center> 

- [IPython](https://ipython.org/) is an "interactive" Python interpreter. 
- IPython also provides the standard Python kernel for Jupyter notebooks. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# IPython 
 > \[IPython\] has become one of the most important tools in the modern
    Python data stack ... It encouarages an __execute-explore__ workflow instead of
 > the typical __edit-compile-run__ workflow of many other programming langauges. 
 > 
 > --<cite> Wes McKinney </cite>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Spyder
 <center> <img src="https://www.spyder-ide.org/static/images/spyder_logo.png?h=f4aab2c7" width=20%> </center>

  - Spyder is a GUI based IDE for Python. 
  - Pairs a text editor with an IPython console for interactive use.  
  - Offers linting, autocomplete, and other useful tools. 
  - Spyder is a good place to edit and develop python scripts (`.py`).
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Jupyter 
 <center> <img src="https://jupyter.org/assets/nav_logo.svg" width=25%> </center>

 - [Jupyter](https://jupyter.org) is an open-source project. 
 - Provides software and services for interactive computing
 - Spun off from IPython in [2014](https://en.wikipedia.org/wiki/Project_Jupyter)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Jupyter Notebooks
 - Jupyter notebooks (`.ipynb`) are one of the most popular ways to 
   share (and develop) data science. 
 - Jupyter notebooks are browser-based and can be run from a local server or
   through a number of web-based services. 
 - Support for many languages, but most popular with Python. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Console
- You can use an interactive Python interpreter at the command line.
- Most useful when working on a remote Linux server. 
- Be sure you are using the version of Python from your (conda) environment
   + ... and not the built-in version used by the OS. 
- Consider using IPython. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Command Line Text Editors
  - To edit scripts on remote servers, use a text editor.
  - Options: `vim`, `emacs`, `nano`, `atom`. 
  - (I use emacs.)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Command Line Text Editors
  - When learning a new text editor start with:
    - How to quit/exit, e.g. emacs `cntrl+x cntrl+c`.
    - How to save edits, e.g. emacs `cntrl+x cntrl+s`. 
    - Find a [cheatsheet][1] and keep it handy. 
    - Learn a bit at a time, then let muscle-memory take over. 
    - Supplement course materials with [tutorials][2]. 

 [1]: https://www.gnu.org/software/emacs/refcards/pdf/refcard.pdf
 [2]: https://www.gnu.org/software/emacs/tour/
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
#  Text Editors
  - Text editors can also be useful on your own machine.
  - Can edit in Spyder or Jupyter, but may prefer a specialized tool.
  - Options: `Visual Studio Code`, `Sublime Text`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Requirements
  - For most problem sets, you will be asked to submit:
     + a Jupyter notebook (`.ipynb`)
     + one ore more Python scripts (`.py`).
  - Occassionaly, may be asked to submit as `.html` or `.md`.
  - The [jupytext][1] library will be helpful here.

  [1]: https://jupytext.readthedocs.io/en/latest/index.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Suggestions
  - Use Spyder while focused on code.
  - Use VS code or another text editor when focused on 
    markdown cells. 
  - Use Jupyter to view and explore (and possibly develop). 
  - You will be required to turn in `.py` source code for notebooks. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# More suggestions
  - Use `conda` as your primary package manager.
  - Create an enviornment specific to this course ...
  - ... and clone to backup before new installs.
  - Take notes on the steps you take to solve a probelm in case 
    you need to do it again (or help a peer). 
  - Or keep a begining to end setup in a shell script. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Takeaways 
  - There are many options for editing Python code and
    interacting with a Python interpreter.
  - Start simple, experiment, and use what works for you. 
<!-- #endregion -->
