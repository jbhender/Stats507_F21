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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Git </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Essentials
*Stats 507, Fall 2021*

James Henderson, PhD  
November 2, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview 1/2
  - [Version Control](#/slide-2-0)
  - [Remote Repositories](#/slide-3-0)
  - [Git Clone & SSH Keys](#/slide-4-0)
  - [Git init](#/slide-5-0) 
  - [Git Commit](#/slide-6-0)
  - [.gitignore](#/slide-7-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Overview 2/2
  - [Remote Repos](#/slide-8-0)
  - [Workflow: pull, commit, push](#/slide-9-0)
  - [git merge](#/slide-10-0)
  - [Hosting Remotes](#/slide-11-0)
  - [git branch](#/slide-12-0)
  - [Takeaways](#/slide-13-0)
<!-- #endregion -->
 
<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Version Control
  - A *version control* system is a tool for managing changes to files over 
    time.
  - A widely used tool for version control is "git". 
  - Another version control tool called subversion or SVN has also been 
    widely used, but "git" is the *de facto* standard for data science.
  - Git is generally already installed on most Linux-like systems.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Version Control
 - Version control is essential for collaborative projects. 
 - It can also help individual users more effectively and efficiently manage 
   their code. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Remote Repositories 
 - Git is a *distributed version control system* and every copy is a 
   repository that can contain the full history of the code.
 - A number of services are available for hosting *remote repositories*.
 - Remote repositories serve as a backup and facilitate collaboration.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Repository Hosting Services 
 - Popular services for hosting remote repositories: 
   + GitHub
   + BitBucket
   + [GitLab](https://gitlab.umich.edu).
 - We will use GitHub ... 
 - ... but I'll also show you how to host your own remote in your AFS space.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Clone
 - Use `git clone` to create a local copy of a remote repository.
 - Two choices for reading data:
   + ssh - best when you will both "push" and "pull",
   + https - fine when you only plan to "pull".
 - When using GitHub, you'll want to set up an ssh key.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## SSH Keys
 - SSH keys are a means for identify verification when using ssh.
 - A key pair consists of a public and a private key - never share your 
   private key.
 - Read more at [Git SSH Keys][gsk]. 

 [gsk]: https://www.atlassian.com/git/tutorials/git-ssh
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Init
- You do not need a remote repository to use git. 
- To begin tracking an existing project without a remote, 
  move to the top folder in the project tree and type `git init`.
- A folder `.git` will be created to track diffs, etc. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git commit
- Version history in Git is tracked through *commits*.
- A *commit* is a collection of changes 
  to source files that represent a particular point in the version history.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git add and commit
- To make a commit, we first use `git add` to place files in the 
 *staging area*.
- Then, we use `git commit -m "Commit Message"` to commit the changes.
- If using a remote, we will typically follow this with `git push`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git status
- Before creating a commit, it's a good idea to use `git status` to
  make sure all changes have been added to the staging area. 
- You can "pipe" this to a pager like "less" if there are a lot of files.
- If you have many files not under version control, create a `.gitignore` 
  file to keep them out of your status output.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Ignore
- The file `.gitignore` provides a list of specific files - or patterns
  using file *globs* - that git should ignore.
- Git will not only ignore these, but will also prevent you from adding 
  them on accident - you have to *force* add them using `git add -f`.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Ignore
- I'd recommend including the following in your `.gitignore` at a minimum:
  - `.*` : all hidden files
  - `*~` : temporary backups created by Emacs
  - `.DS_store`: if you ever work on Mac
  - Various log and error file types:
    - `*.log` 
    - `*.out` . 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Remote
- Git is used most effectively with a remote repository.  
- Create the remote repository first.
   + On GitHub do this through a web browser. 
- Using git with a remote repository is a great way to manage work across
  multiple computers.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Push, Pull, Fetch
- To send commits from the local repository to a remote, use `git push`.
- To acquire changes from the remote without merging them into the remote,
  use `git fetch`. 
- To acquire changes from the remote and *merge* them into the local branch,
  use `git pull`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Remote
- To link a local and remote repository, use `git remote`:
  + `git remote add origin git@github.com:user/repo.git`
  + `git push -u origin main`.
- This creates a remote named "origin" (e.g. associates the name origin 
  with the given "url"). 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Remote  
- We then set the (default) branch "main" on the remote as the "upstream"
  branch for our local (default) branch named "main". 
- These steps are handled automatically when using `git clone`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Workflow
- Here is a (my) typical git workflow:
   + (once) setup a remote repository for a project
   + (once per computer) clone that repository
   + Making changes:
      - `git pull` to sync local with remote,
      - edit files and work on project,
      - (when switching focus) `git add`, `git status`, `git commit`
      - `git push`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Workflow
- Recommended workflow:
   + Make a branch for work-in-progress changes,
   + Merge that branch into `main` after completing a logical chunk of work.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Git Merge
- A *merge* is used to combine git histories.
- `git pull` performs a merge automatically when able.
   + There are several types of merge.
   + I typically use *fast-forward* merges only. 
- Manage conflicts by:
  - editing code where conflicts occur
  - or choose one version over another.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Git Diff 
- `git diff` can be used to compare a file to the *index* (staging area)
- `git diff` can also be used to compare two files on disk among other uses.
- `git checkout` can be used to discard local changes and restore a file 
   to the version in the index. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Creating a remote
- You can create your own remote repositories for git.
- A *remote* must be initialized as a *bare* repository. 
- Use `git init --bare` to initialize a bare repository.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Remote in AFS
- Let's setup a remote repository `507_afs` in our AFS space.
- First, we'll create the remote:
  + login to the remote server: `ssh user@login.itd.umich.edu`
  + create a directory for your git remotes: `mkdir git_remotes`
  + make a project directory: `mkdir git_remotes/507_afs.git`
  + Move to the project directory and set it up as bare:
    - `cd git_remotes/507_afs.git`,
    - `git init --bare`. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Using a remote in AFS
 - To work with the directory, in your AFS space or elsewhere,
   clone the remote, add and commit files, push and pull.
 - From AFS:
   + Move to the parent folder where you'd like the repo to be
      - `mkdir ~/git`,
      - `cd ~/git`.
   + Clone the repository:
      - `git clone /afs/umich.edu/user/u/n/unique_name/git_remotes/507_afs.git`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Add some files
- Add some files:
  + `cd 507_afs`
  + `echo "## About" > README.md`
  + `git add README.md`
- Create the commit:
  +  `git status`
  + `git commit -m "Initial commit.`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Renaming primary branch
- Rename branch
  + `git branch -m master main`
  + Edit HEAD in the bare remote to reflect this change. 
- Push changes
  + `git push -u origin main`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Clone to the local computer
- `git clone unique_name@login.itd.umich.edu:/afs/umich.edu/users/u/n/unique_name/git_remotes/507_afs.git`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Branches
- There are several commonly used branching patterns used with git.
- A branch is an isolated line of development for code in a git repo.
- Working in branches helps to keep a clean commit history.  
- Create a branch using `git branch <name>`.
- View branches using `git branch`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Branches
- Use `git checkout` to switch branches.
- This means the version of the files on a specific branch become the version
  visible in the current file tree.
- Branches need their own upstream branches on remote repositories.
- Commits are specific to a branch.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Branches
- When you want to bring two branches into agreement, use `git merge`.
- The "receiving" branch should be active, use `git checkout`.
- Most common is a "fast-forward merge". 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways
 - Use git for (distributed) version control.
   + Version control is a good habit even for solo projects. 
 - `git clone` to copy an existing repo.
 - `git pull` to fetch and merge changes from remote to local.
 - `git add`, `git status`, `git commit` to commit changes to the version 
    history.
 - `git push` to send your changes to the upstream remote. 
 - Use branches to keep the commit history on the primary branch clean. 
<!-- #endregion -->