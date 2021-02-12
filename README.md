# Branch Integration Tool

This is a simple command line tool to integrate code changes
from a source branch to the target branch using internal svn
commands. This tool also has commands to identify the changes
to merge to the target branch. 
  

Usage:

```
Usage: bit [OPTIONS] COMMAND [ARGS]...

  Branch Intigration Tool.

Options:
  --help  Show this message and exit.

Commands:
  build       Build Command
  clone       Clone Repository
  commit      Commit the change
  merge       Merge revision from source to current working repo branch
  merge_info  Merge Information: get the eligible revisions from source...
  update      Update repository.
```
