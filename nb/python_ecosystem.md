---
jupyter:
  author: James Henderson, PhD
  date: August 9, 2021
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise,author,date,markdown
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  markdown:
    extensions: footnotes
  rise:
    enable_chalkboard: true
    header: <a href="/#0"> <h3> Stats 507 - The Python Ecosystem </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# The Python Ecosystem
*Stats 507, Fall 2021*

James Henderson, PhD  
August 24, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Python 
<center> <img src="./img/python.png" width=10%> </center>
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Anaconda
 <center> <img src="./img/anaconda_org_logo.svg" width=50%> </center>
 
 - [Anaconda](https://www.anaconda.com/products/individual) is a popular
   python distrubution that comes with:
   + a package and environment manager `conda` 
   + many preinstalled modules including Numpy, Scipy, 
     Jupyter, and Pandas.  
 - Anacaonda Navigator provides instances of Jupyter Notebooks, Spyder,
   and other tools. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Conda Environments
- Environments allow us to isolate and manage dependencies
  + Environments can have different versions of key modules
  + ... or different versions of Python
  + Update dependencies in a new environment for testing code. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Conda Environments
- To get started, in your terminal application, `conda init`.
- Make sure `conda` is in your path.
- `venv` is an alternative 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Managing environments
 - list `conda env list`
 - create `conda create -n <env> python3.8` 
 - activate `conda activate <env>`
 - deactivate `conda deactivate`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Managing dependencies
 - Python modules can be managed with conda
 - `conda install`, `conda update` 
 - "Channels" (e.g. conda-forge) are locations where conda will look for modules
 - `pip` is the primary alternative
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Spyder
 <center> <img src="./img/spyder_logo.png" width=10%> </center>

  - Spyder is a GUI based IDE for Python. 
  - Pairs a text editor with an IPython console for interactive use.  
  - Offers linting, autocomplete, and other useful tools. 
  - Good place to edit and develop python scripts `.py`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Jupyter 
 <center> <img src="./img/jupyter_logo.png" width=10%> </center>

 - [Jupyter](https://jupyter.org) is an open-source project
 - Provides software and services for interactive computing
 - Spun off from IPython in [2014](https://en.wikipedia.org/wiki/Project_Jupyter)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Jupyter Notebooks
 - Jupyter notebooks (`.ipynb`) are one of the most popular ways to 
   share (and develop) data science. 
 - Jupyter notebooks are browser-based and can be run from a local server or
   through a number of web-based services. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Console
- You can also use an interactive python interpreter at the command line.
- Most useful when working on a remote Linux server
- Be sure you are using the version of python from your (conda) environment
   + ... and not the built-in version used by the OS. 
- Consider using IPython, the basis of Jupyter python kernel. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# Command Line Text Editors
  - To edit scripts on remote servers, use a text editor.
  - Options: `vim`, `emacs`, `nano`, `atom`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
# Command Line Text Editors
  - When learning a new text editor start with:
    - How to quit/exit, e.g. emacs `cntrl+x cntrl+c`.
    - How to save edits, e.g. emacs `cntrl+x cntrl+c`. 
    - Find a cheatsheet and keep it handy. 
    - Learn a bit at a time, then let muscle-memory take over. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
#  Text Editors
  - Text editors can also be useful on your own machine.
  - Can edit in Spyder or Jupyter, but may prefer a specialized tool.
  - Options: `Visual Studio Code`, `Sublime Text`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
# 
<!-- #endregion -->
