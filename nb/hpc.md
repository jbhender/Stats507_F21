---
jupyter:
  jupytext:
    cell_metadata_json: true
    notebook_metadata_filter: rise
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  rise:
    autolaunch: true
    enable_chalkboard: true
    header: <a href="#/slide-0-0"> <h3> Stats 507 - HPC, GreatLakes, & Slurm</a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## HPC, Great Lakes, & Slurm
*Stats 507, Fall 2021*

James Henderson, PhD  
November 18, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview
 - [Accessing Great Lakes](#/slide-2-0)
 - [Allocations](#/slide-3-0)
 - [Lmod (pre-installed software)](#/slide-4-0)
 - [Python Batch Jobs](#/slide-5-0)
 - [Slurm basics](#/slide-6-0)
 - [Job Arrays](#/slide-7-0)
 - [Takeaways](#/slide-8-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Great Lakes
 - [Great Lakes][gl] is the university's high-performance 
   computing (HPC) cluster. 
 - Consists of ~13,000 cores (CPU and GPU). 
 - Uses a job scheduler for "production" work. 

[gl]: arc.umich.edu/greatlakes/
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Access
 - Access Great Lakes using ssh: `ssh user@greatlakes.arc-ts.umich.edu`.
 - Will be connected to a *login node*, `gl-loginX.arc-ts.umich.edu`. 
 - Use *login nodes* for file management, testing code, etc. 
 - Home directory `/home/user/` is unique to GL -- it is not AFS.
 - Access AFS at `/afs/`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Access - VPN
 - Access to Great Lakes is restricted to the campus network.
 - To access from off campus, `ssh` to `login.itd.umich.edu` and 
   "hop" to Great Lakes (ssh from the login pool to Great Lakes). 
 - Alternately, use the campus [VPN][vpn].
 - VPN is also useful for accessing library resources. 

[vpn]: https://its.umich.edu/enterprise/wifi-networks/vpn/getting-started
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Access - OnDemand
- You can also use Great Lakes through a web browser using "Open OnDemand". 
- Navigate to <https://greatlakes.arc-ts.umich.edu>.
- See the [user guide][glug] for additional help.

[glug]: https://arc.umich.edu/greatlakes/user-guide/
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Allocations
  - Jobs on the Great Lakes cluster require an *allocation*. 
  - You have access to the course allocation ?`stats507f21_class`
  - See your allocations using the custom command: `my_accounts`.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Allocations
 - Rates are based on how many resources you request (cores and memory) 
    and how long your job runs.   
 - You have a budget of $60.91 for the class account.  
 - Custom command `my_job_estimate` to get an estimate of the per hour rate. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pre-installed software
 - Pre-installed software built to work in the GL environment is managed
   through *Lmod* using the `module` command.
 - Use sub-commands `module keyword` or `module spider` to search for modules.
 - Use `module load` to request software and a license, if needed, e.g.,
  `module load tensorflow`.
 - Use `module list` to see currently loaded modules. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pre-installed in jobs
 - Load modules *before* submitting jobs and use option:
   `#SBATCH --get-user-env` 
 - Or load modules within job script. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Python Version
 - We'll use tensorflow in the final weeks of the course.
 - Use `module spider tensorflow` to see installations.
 - Load the latest version, `module load tensorflow/2.5.0`.
 - Use `module list` to see others loaded and read info for the specific
   Python installation.
 - Add packages locally `pip install --user ` 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Batch Jobs
- Execute a Python script non-interactively (in *batch* mode) at the 
  command line using `python script.py`. 
- Provide commands as a string using `-c` option.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Batch Jobs
- Often helpful to provide arguments to your script from the command line.
- Use `sys.argv` for a list of command line arguments.
- For example, if you run `script.py` as `python3.9 script.py a b 3 D` then
  `sys.argv` is a list `['script.py', 'a', 'b', '3', 'D']`. 
- Use these to alter source files, number of processes, etc. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Slurm
- Slurm is a "workload manager" or *job scheduler*.
- We use Slurm to request HPC resources for a compute *job*.
- Provide options to Slurm as special comments `#SBATCH` in a shell (`.sh`)
  script.
- These options must come *before* any shell commands - they may only be
  preceded by comments and blank lines. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Slurm
- We'll review key options from the Great Lakes [user guide][glug].
- Submit job script using the `sbatch` command.  
- Examples in course repo: `run-mp_isolet.sh` and `mp_isolet.py`. 
- I use the convention of naming these scripts starting with `run` and 
  including the name of the script each runs. 
- See the [cheat sheet][slurmsc] for additional commands to inspect job 
  status. 

[glug]: https://arc.umich.edu/greatlakes/user-guide/
[slurmsc]: https://arc.umich.edu/wp-content/uploads/sites/4/2020/05/Great-Lakes-Cheat-Sheet.pdf
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Queueing time
- Smaller jobs requesting fewer CPUs and/or less memory will tend to run 
  sooner than larger jobs.
- Resources are more likely to be available sooner for smaller jobs.
- Users with less overall (recent) usage generally have higher priority than
  heavy users.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Job Arrays
- A *job array* allows you to submit a set of jobs with similar parameters.
- Add `#SBATCH --array ` and a set of indices, e.g., `1-4` or  `1,2,4`. 
- Use the array index in a file name (`%a`) or in your shell script using 
  `${SLURM_ARRAY_TASK_ID}`. 
- Useful patterns: use as a command line argument or as part of filename.
- See example `run-array-mp_isolet.py`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
 - Great Lakes is an HPC cluster that provides:
   + many asynchronous CPU cycles,
   + flexible memory,
   + GPUs.
 - Slurm is the job manager and scheduler.
 - Interact with slurm using `#SBATCH` directives in a shell script and the
   `sbatch` command. 
 - Use `sys.argv` to access command line arguments when running Python in 
   batch mode. 
 - Use job-arrays to achieved additional parallelism. 
<!-- #endregion -->
