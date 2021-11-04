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

Within the problem set (ps) folder, is a sub-folder "exemplars" containing
student solutions that stood out as particulary good. Thank you to the students
who agreed to have their solutions posted.

### Demonstrations

Demonstrations can be found in the [demo](./demo/) folder. Currently these are:
  
  + [jupy_demo.py](./demo/jupy_demo.py)
  + [numpy_comp.py](./demo/numpy_comp.py)
  + [isolet_demo.py](./demo/isolet_demo.py)..

#### shell

Within demo the [shell](./demo/shell) directory contains full length demos
and short examples illustrating syntax for useful shell programming patterns.

Here are short descriptions:

 - `dups.txt`, `nhanes_files.txt` example text files for use with the
    shell examples.
 - `ex_while_read.sh` illustrates the `while read` pattern for looping.
 - `ex_check_dup_lines.sh` illustrates checking for duplicate lines in
    a file using `sort`, `uniq`, `wc` and an `if` statement. The `if`
    statement syntax here is for bash and may error in other shells,
    e.g. zsh.
 - `ex_variable_expansion.sh` demonstrates the difference between single
    and double quotes in terms of the latter allowing variable expansion.
 - `recs_data.sh` downloads the 2009 and 2015 RECS data and associated codebooks.
 - `cutnames.sh` is an executable program for extracting columns from a csv file
    by name. 
 - `nhanes_demo.sh` downloads several cohorts of NHANES data, converts to
    csv, selects columns, and appends into a single dataset.

### Binder

These are files to allow you to view notebooks in this repo through 
[Binder].  You can ignore these.

