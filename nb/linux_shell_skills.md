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
    header: <a href="#/slide-0-0"> <h3> Stats 507 - Linux Shell Skills </a>
    progress: true
    scroll: true
    theme: solarized
    transition: convex
---

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Linux Shell Skills
*Stats 507, Fall 2021*

James Henderson, PhD  
October 26 & 28, 2021
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Overview 1/2
 - [Terminal applications and ssh](#/slide-2-0)
 - [*Nix file system](#/slide-3-0)
 - [HOME, PATH, SHELL](#/slide-4-0)
 - [Text Editors](#/slide-5-0)
 - [Pagers](#/slide-6-0)
 - [Tmux](#/slide-7-0)
 - [Process Control](#/slide-8-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Overview 2/2
 - [File & Data Transfer](#/slide-9-0)
 - [Pipes and Redirection](#/slide-10-0)
 - [Compression and Archiving](#/slide-11-0)
 - [Useful tools](#/slide-12-0)
 - [Shell Scripting](#/slide-13-0)
 - [Takeaways](#/slide-14-0)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## SSH and command line
  - `ssh` or [secure shell][ssh] is a cryptographic network application used 
    to connect to a remote command line application. 
  - A [command line interface][cli] is a means of interacting with a computer
    through lines of text. 

  [ssh]: https://en.wikipedia.org/wiki/Secure_Shell
  [cli]: https://en.wikipedia.org/wiki/Command-line_interface
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Terminal Applications
  - A *terminal application* is a text-based command line interface for 
    interacting with a computer. 
  - If you use a Mac or Linux OS you have access to a terminal installed on
    your computer as *Terminal*
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Terminal Applications
  - If you are running a Windows OS, you will need to install a terminal 
    or a stand alone ssh client:
    + [Putty](https://www.putty.org/) is an ssh client you can use
       to connect to university Linux servers;
    + [git for windows](https://gitforwindows.org/) includes a command line
       interface that includes the bash shell.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Virtual Machines
  - You can also access a virtual windows machine using 
    [MiDesktop](https://midesktop.umich.edu), with both Putty and 
    git for windows available through AppsAnywhere.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## AFS 
 = You need to have an AFS home directory to connect to university Linux 
   servers. 
 - If you do not have one, you can set it up by visiting
   http://mfile.umich.edu/ and selecting the 'AFS Self-Provisioning Tool'. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Hosts
 - You can connect to a UM Linux server using `ssh`.
 - Replace `unique_name` with your UM unique name (the part of your 
   UM email address preceding `@umich.edu`).
 - User name can be omitted if your username for you computer is the same
   or by aliasing the connection.  
 - Use `hostname` to see name of host you were connected to. 

```bash slideshow={"slide_type": "code"}
  ssh unique_name@login.itd.umich.edu
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## *Nix File System
 - In Linux essentially everything is a file: 
   + program executables,
   + system configurations,
   + your data and source files.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## File Tree
  - Files are organized hierarchically into directories.
  - This hierarchy begins with the *root* directory `/`. 
  - Directories can contain files and sub-directories with locations 
    in the directory hierarchy separated by a forward slash - `/`.
  - This collection of directories  and files is called a *file tree*.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## File Tree Navigation
 - Use the following commands to navigate and interact with the file tree:
   + `ls` (list files), `ls -a`, `ls -l`
   + `cd` (change directories)
   + `pwd` (print the current or *working* directory)
   + `mkdir` (make directory), `mkdir -p`
   + `rmdir` (remove directory)
   + `rm` (remove a file), `rm -r`
   + `mv` Move a file or directory
   + `find` Find a file.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## File Tree Navigation
 - In working with the file tree, it is helpful to know:
   + `.` refers to the current directory,
   + `..` refers to the parent directory, one step up the file tree.
   + `cd` invoked with no arguments will return you to your home directory.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Hidden files
 - Configuration files and others used by programs are often named as 
   *hidden files* also called *dot files*. 
 - The names of dot files begin with a `.`. 
 - To see these files, use `ls -a`.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Filename Wildcards Tree Navigation
 + Use *filename wildcards* to refer to groups of files matching 
   specific patterns:
    - `*` matches any sequence of characters
    - `?` matches any single character.
 + `.*` matches all dot files.
 + `ps1.*` would match all extensions to files named 
   `ps1` (e.g. `ps1.py`, `ps1.light.py`, `ps1.ipynb`).
 + `ps?.py` would match `ps1.py` and `ps2.py` but not
   `ps1.light.py`. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Environment Variables
 - Environment variables determine certain aspects of how the OS behaves and
   responds to your instructions. 
 - Here are a couple of important ones:
   + `HOME`  (location of your home directory)
   + `SHELL` (the shell you are using to interface with the machine)
   + `PATH`  (locations to search for executable programs)
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Shells
 - In the [Bash shell](https://www.gnu.org/software/bash/manual/bash.html) 
   (among others), use `$` to access the value of an environment variable. 
 - The `echo` command can be used to print these values to the screen, e.g.
   `echo $SHELL`.
 - Recognize the bash shell by its prompt `$` vs the `%` prompt used
   by csh, zsh, and other shells.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## PATH
 - Use `which` to search your `$PATH` for an executable command. 
 - Will find the matching command appearing first in the locations specified
   in `PATH`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tilde Expansion
 - A tilde `~` will often be expanded as `$HOME`.
 - Useful for specifying absolute file paths when supported, e.g.
    `~/github/Stats_507/` vs `/Users/jbhender/github/Stats507`. 
 - Not supported everywhere. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Text Editors
 - To edit files in the shell, you will need to use a text editor.
 - Some popular choices are:
    + [emacs](https://www.gnu.org/software/emacs/tour/)
    + [vi / vim](https://www.vim.org/)
    + [nano](https://www.nano-editor.org/)
 - Find a cheat-sheet and pick an editor to learn the basics of if you
   haven't already.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Emacs 1, 2, 3
- `emacs README.md` will open (or create) a file named `README.md`
- Keyboard shortcuts:
  + `cntrl+x`, `cntrl+s` to save
  + `cntrl+x`, `cntrl+w` to write (save as)
  + `cntrl+x`, `cntrl+c` to close.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Emacs 4, 5, 6
- Keyboard shortcuts:
  + `cntrl+g` to quit command window,
  + `cntrl+k` "kill" (delete) to end of line,
  + `cntrl+a` (`cntrl+e`) move to start (end) of line.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Emacs 5, 7, 8
- `cntrl+x` to search,
- `esc` (meta), `shift+5` find and replace,
- `cntrl+x`, `shift+9` define keyboard macro,
  + `cntrl+x`, `shift+0` to end,
  + `cntrl_x`, `e` to execute, then `e` to execute again.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Pagers
 - A page viewer is a program for viewing a (text) file at the command line.
 - Most common defaults are `more` and `less`.
 - I prefer `less`:
   + `less README.md` to open, `-S` to scroll.
   + `q` to quit,
   + `/` to search, `n` for next match,
   + `space bar` to page.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Tmux
 - To create a persistent connection you can leave and come back to use
   `tmux`, a *terminal multiplexer*.
 - The program `screen` is another option.  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tmux - Sessions and Windows
 - `tmux new -s 507_live` creates a new *session* named `507_live`.
 - The (default) tmux command prefix is `cntrl+b`:
    + `cntrl+b`, `c` *creates* a new window,
    + `cntrl+b`, `n` (`p`) moves to the next (previous) window, 
    + `cntrl+b`, `[0-9]` will move to a specific window number.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tmux - Detach and Attach
 - Use `cntrl+b`, `d` to *detach* (or type `tmux detach`) a session.
 - To attach to a *target* session named `507_live`, `tmux a -t 507_live`.
 - To list available sessions, `tmux ls`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Tmux - Panes
 - A single window can be split into one or more *panes*. 
 - `cntrl+b`, `shift+'` splits the active window horizontally.
 - `cntrl+b`, `shift+5` splits the active window vertically.
 - `cntrl+b`, `arrow` (or `o`) to move between panes. 
 - `cntrl+b`, `space bar` to cycle through layouts. 
 - `cntrl+b`, `z` to *zoom* (or focus) the active pane. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Process Control
- Suspend an active process using `cntrl+z` (processing stops)
- Run a suspended job in the background using the command `bg`.
- Run a batch job in the background using `&`. 
- Bring a job to the foreground using `fg`. 
- Specify a job number using, e.g. `%1`. 
- Use `jobs` to see all jobs. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Transferring Data
- There are several ways to transfer data or files to or from
  a remote host:
  + `scp` - most common way to transfer small to medium sized files,
  + `wget` - download data directly to the remote host from the web,
  + `sftp` - interactive file transfer. 
  + for scripts, using `git` and a "third-party" server such as
    GitHub or BitBucket (more in next lecture).  
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## scp
- Like `cp` for copying to and from local locations, `scp` or 
  *secure copy* is used to transfer to and/or from remote locations.
- `scp host:/path/to/folder/file.txt ./`  will copy from `file.txt` from
  the remote host (`host`) to the current (local) directory.
- Conversely, `scp ./file.txt host:/path/to/folder` will copy the (local)
  file `file.txt` to the specified folder on remote host `host`. 

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## wget
- Use `wget` to download files from the web directly to a remote host:
`wget https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv`
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## sftp
- For interactive transfer using ftp connect to a remote host using `sftp`.
- Navigate the file tree as usual using `cd`, `pwd`, `ls`.  
- Use `put` to copy a file from the local connection to the remote.
- Use `get` to copy a file from the remote to local. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Streams
 - There are three standard streams or channels used to communicate data in
   most computer programs: 
   - `stdin`  or *standard input*, 
   - `stdout` or *standard output*, and,
   - `stderr` or *standard error*. 
 - In the Linux shell, these streams are files located in the `/dev/` 
   directory, e.g. `/dev/stdin`, `/dev/stdout` and `/dev/stderr`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## file re-directions
 - Most command line tools utilize `stdout` and `stderr` to communicate to the 
   user as these streams print to the console.
 - Redirect these streams using the symbols `>` (for `stdout`) 
   and `&` (for `stderr`). 
 - Similarly we can redirect the contents of a regular file to `stdin` using 
   `<`, e.g. `< file.txt`.

<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Stream Re-Direction Examples
 - Print "hello!" to `stdout` using `echo`.
 - Redirect the same text to `welcome.txt`.
 - Append to that file using re-direction with `>>`. 
 - Redirect the file `welcome.txt` to `stdin` for the `tr` or *translate* tool.

```bash
echo hello!
echo hello! > welcome.txt
echo 'stats 507!' >> welcome.txt
< welcome.txt tr '[a-z]' '[A-Z]'
```
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Pipes
 - Build pipelines combining multiple command line tools
   by redirecting `stdout` from one command to `stdin` for the next using
   a pipe `|`. 
 - Short pipelines such as these are often called "one-liners".  
 - More examples in section 2.3 (especially 2.3.4 and 2.3.5) of 
   [Data Science at the Command Line][dscl2]

```bash
echo 'hello stats 507!' | tr '[a-z]' '[A-Z]' | tr ' ' \n
```   

[dscl2]: https://www.datascienceatthecommandline.com/chapter-2-getting-started.html#essential-gnulinux-concepts
<!-- #endregion -->


<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Compression and Archiving
 - Large files often contain redundant data and can be stored
   using less space on disk in a compressed format. 
 - Compression can make reading from or writing to a file more efficient as
   reading  the bits off disk is an "I/O-bound" task while 
   decoding/decompressing is a "CPU-bound" task. 
 - This is particularly useful when reading from or writing to network volumes
   and on shared systems with I/O bottlenecks.


<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Disk utilization
 - The `du` or *disk utilization* utility can be used to see the space 
   on disk used by one or more files.
 - Use the `-h` option to print values in *human* readable units. 
 - Use `-s` to get *sum* totals for a directory or files matching a *glob*.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## gzip
 - There are many compression formats tools.
 - One of the most popular is `gzip`. 
 - The command `gzip file.txt` compresses `file.txt` into `file.gz`.
 - The original extension is stored in the compressed file.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## gzip
 - The file can be uncompressed using `gunzip file.gz` or `gzip -d file.gz`
 - Retain the compressed copy and unzip directly to standard output using the
   `-c` option: `gunzip -c file.gz > file.txt`. 
 - The `zcat` command is a shortcut that does the same thing.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## tar
 - A *tarball* is an archive of a file tree and often compressed. 
 - Useful for transferring whole directories between machines manually.  
 - It is also a way to cleanly archive files from projects you would like to 
   retain, but no longer need to use frequently. 
 - Many programs have the ability to work directly with archived and/or 
   compressed data.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## tar
 - Two common use cases are:
   + creating an archive `tar cvfz name.tgz ./parent_folder`,
   + and extracting the archive `tar xvfz name.tgz`.
 - The extension `.tgz` is short for `.tar.gz` indicating that the archive has 
   been compressed using `gzip`.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## head & tail 
 - An advantage of the command line is the ability to work with large files
   using streams so that only a small portion of the file is read at a time. 
 - The `head` and `tail` commands are useful in this respect:   
   + `head` - read the first *n* lines of a file
   + `tail` - read the last *n* lines of a file 
 - `tail` can be used with a `+` to read from line *n*.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## Other helpful commands
 - `wc` - count words or use `wc -l` to count lines.
 - `grep` - find lines in files that match string patterns using regular
    expressions. 
 -  `nl` - number the lines in a file.
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "subslide"}} -->
## More helpful commands
 - `sort` - sort a file on one or more fields.
 - `cut` -  extract select columns from a delimited file.
 - `paste` - concatenate files line by line.
 - `join` - merge two files based on a common field.
 - For more, see Chapter 5 of [Data Science at the Command Line][dscl5]
 
[dscl5]: https://www.datascienceatthecommandline.com/chapter-5-scrubbing-data.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Shell scripting 
 - A shell script is a program constructed from shell commands.  
 - Use to construct tools for re-use as well as to document data acquisition
   and processing steps to make analyses easier to reproduce. 
 - We will review shell demonstrations from the course repo as time permits.
 - For more on shell scripting, see [Chapter 4][dscl4] from 
   *Data Science at the Command Line*. 

[dscl4]: https://www.datascienceatthecommandline.com/chapter-4-creating-reusable-command-line-tools.html
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways 1/2
 - Use a terminal application for a command-line interface to you
   own computer and ssh to connect to university Linux servers.
 - In Linux everything is a file - learn to navigate the file tree. 
 - Use an editor to edit, a pager to view, and shortcut keys in both. 
 - Create persistent sessions using `tmux`, a *terminal multiplexer*. 
<!-- #endregion -->

<!-- #region {"slideshow": {"slide_type": "slide"}} -->
## Takeaways 1/2
- Working with data streams through pipes and redirection is
  a primary attraction of the Linux shell.
- Use `scp`, `sftp`, or `wget` to get data to and from remote hosts. 
- Compress files on remote volumes for faster (repeated) reads and writes. 
- Shell scripts are useful both for creating tools for reuse and for
  documenting data cleaning steps. 
- Learn shell patterns and skills a bit at a time.  
<!-- #endregion -->
