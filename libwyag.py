# parse command-lines lib
import argparse

# git uses a special conf file format
import configparser

# date/time manipulation
from datetime import datetime

# read users/group id of files
try:
    import grp, pwd
except ModuleNotFoundError:
    pass

# support gitignore matching patterns
from fnmatch import fnmatch

# SHA-1
import hashlib

from math import ceil
import re

# access actual command-line arguments
import sys

# comprression
import zlib

# os and os.path -> filesystem abstraction routines
import os

argparser = argparse.ArgumentParser(description="The stupidest content ever")

# init, commit etc -> subparsers
# git COMMAND (declaration)
# dest states that the name of the chosen subparser will be returned as a string called command
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# bridges functions -> command args functions

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")


# git repo -> work tree (files version control live), git directory (git stores its own data)
# Repository object : 1) directory exists
#                     2) contains a subdirectory called .git
#                     3) read its configuration in .git/config
#                     4) check core.repositoryformatversion is 0

# We build a constructor : takes an argument "force" which disables all checks
# thats becuase repo_create() functions will later use Repository object. 
# So we need a way to create a Repository object

class GitRepository(object):
    """A git Repository"""
    
    worktree = None
    gitdir = None
    conf = None


#   force will disable all checks   
    def __init__(self, path, force=False) -> None:
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a git Repository {path}")

        # Read configuriation file in .git/config
        # config parser reads and writes INI files (.git/config files)
        # ConfigParser() allows me to add , store settings and treat file like a dictionary
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core","repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")

