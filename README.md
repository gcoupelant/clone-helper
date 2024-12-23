# Clone Helper

Simple script to help clone repositories mapping the remote URL to a local path

## Installation

After cloning this repository, simply create an executable script in your `$PATH`, passing all argument to the `clone.py` file.

For example, from the cloned repository directory, you can run:

```bash
$ echo "$PWD/clone.py \$@" | sudo tee /usr/local/bin/clone-helper
$ sudo chmod +x /usr/local/bin/clone-helper
```

For an even better experience, you can also source the output of the command (which is `cd` followed by the target directory).
That way your terminal will automatically change directory, even if it already exist.

Add the following function to you `.bashrc`:
```bash
function clone {
    source <(clone-helper -q $@)
}
```

### Root of your source directory

By default, the script uses `~/src` as the root directory for cloning. You can change this by editing the script's `SRC_PATH` constant.

## Usage

The script will use the repository hostname, path and name to construct the target directory.

For example, cloning https://github.com/gcoupelant/clone-helper:

```bash
$ clone git@github.com:gcoupelant/clone-helper.git
```

This will clone the repository to `~/src/github.com/gcoupelant/clone-helper` and change you current directory to it.
