# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

clone-helper is a single-file Python script that clones git repositories into a structured directory hierarchy based on the repository's hostname and path. It maps remote URLs to local paths (e.g., `git@github.com:user/repo.git` → `~/src/github.com/user/repo`).

The script outputs a `cd` command that can be sourced by the shell, allowing users to automatically navigate to the cloned directory.

## Core Architecture

### URL Parsing

The script uses a regex pattern (`git_url_re`) that matches both SSH (`git@host:path`) and HTTPS (`https://host/path`) git URLs. It extracts:

- `host`: The git server hostname (e.g., `github.com`)
- `path`: The repository path (e.g., `user/repo`)

The regex is defined at module level and handles trailing slashes and `.git` suffixes.

### Directory Structure Logic

- **SRC_PATH constant** (line 11): Default root directory for all clones (`~/src`). This is the primary configuration point.
- Clone path construction: `{SRC_PATH}/{host}/{path}`
- Empty directory check: Allows cloning into existing but empty directories (git's behavior)

### SSH Configuration

The script uses `GIT_SSH_COMMAND='ssh -o BatchMode=yes'` to prevent interactive SSH prompts (e.g., host key verification). This makes the script suitable for automation but requires SSH keys to be pre-configured.

### Output Behavior

- Default mode: Prints informational messages + final `cd` command
- Quiet mode (`-q`/`--quiet`): Only prints the `cd` command (designed for shell sourcing)

## Testing

No automated tests exist. To test manually:

```bash
# Test basic cloning
./clone.py git@github.com:user/repo.git

# Test quiet mode (sourcing)
source <(./clone.py -q git@github.com:user/repo.git)

# Test HTTPS URLs
./clone.py https://github.com/user/repo.git

# Test existing directory handling
./clone.py <url-already-cloned>

# Test empty directory handling
mkdir -p ~/src/test.com/user/repo
./clone.py git@test.com:user/repo.git
```

## Making Changes

When modifying the script:

- The regex pattern is central to URL parsing - test both SSH and HTTPS formats
- Error messages should print to stderr, but the final `cd` command always goes to stdout (for sourcing)
- Maintain the distinction between quiet and verbose output modes
- Be careful with the empty directory check - it must align with git's behavior
