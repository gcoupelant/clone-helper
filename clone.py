#! /usr/bin/env python3

import argparse
import os
import re
import subprocess
import sys
from operator import itemgetter
from pathlib import Path

SRC_PATH = "~/src"

# Create the regex for the url
git_url_re = re.compile(
    r"^(?:git@|https?:\/\/)(?P<host>\S+?)(?::|\/)(?P<path>\S+?)\/?(?:.git)?$")


# Create the type parser
def git_url_type(arg_value):
    match = git_url_re.search(arg_value)
    if not match:
        raise argparse.ArgumentTypeError("invalid git url")
    return match


# Create the parser
my_parser = argparse.ArgumentParser(
    description=
    f'Clone a repository in {SRC_PATH}, creating any intermediate directory')

# Add the arguments
my_parser.add_argument("url", type=git_url_type, help="the git url to clone")
my_parser.add_argument("-q", "--quiet", action="store_true")

# Execute the parse_args() method
args = my_parser.parse_args()

# Extract info from the url
git_url_host, git_url_path = itemgetter('host', 'path')(args.url.groupdict())
clone_path = Path(os.path.expanduser(SRC_PATH), git_url_host, git_url_path)

# Check if directory already exist
# TODO: Check if the directory is empty, since git can clone in that case
if clone_path.exists():
    if not args.quiet:
        print('Error: target directory already exists.\n\nAccess it using:', file=sys.stderr)
    print(f"cd {clone_path}")
    raise SystemExit()

# Clone the repository
git_clone_url = f'git@{git_url_host}:{git_url_path}.git'
subprocess.check_call(['git', 'clone', git_clone_url, clone_path])

# Print helper to `cd` in the directory
if not args.quiet:
    print('\nAccess cloned directory:')
print(f'cd {clone_path}')
