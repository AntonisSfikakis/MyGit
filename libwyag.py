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

