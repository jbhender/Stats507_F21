## Stats 507, Fall 2021

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jbhender/Stats507_F21/HEAD)

This is a github repository which I will used to share code
and notebooks with students in Stats 507.

The primary page for this course, including static versions of slides, is available at
[jbhender.github.io/Stats507/F21](jbhender.github.io/Stats507/F21).

### Notebooks

The folder [nb](./nb) collects notebooks from the course, including lecture
slides. Lecture slides are included both in the markdown `.md` format I 
authored them in and an associated `.ipynb` format viewable without 
[jupytext][jupy] enabled.

For the "tables" notebook, I've also included a version of the document
as a python script. This was created using the command:
`jupytext --to py:light tables.ipynb`.  Note that these files have
extra metadata, e.g `# + [markdown]`, relative to what yours might.
This metadata is here to enable me to show these as slides. 

[jupy]: https://jupytext.readthedocs.io/en/latest/index.html

### Problem Sets

Files related to problem sets, including example solutions can be found
in the [ps](./ps) folder.

### Demonstrations

Demonstrations can be found in the [demo](./demo/) folder. Currently these are:
  
  + [jupy_demo.py](./demo/jupy_demo.py)
  + [numpy_comp.py](./demo/numpy_comp.py).

### Binder

These are files to allow you to view notebooks in this repo through 
[Binder].  You can ignore these.

