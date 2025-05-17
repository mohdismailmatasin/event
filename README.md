# Event Script Utilities

This repository contains three Python scripts for basic file operations:

- `cp.py`: Copies files or directories with a detailed progress bar.
- `mv.py`: Moves or renames files or directories with a detailed progress bar.
- `dl.py`: Downloads files from HTTP/HTTPS URLs or copies local files/directories. It features a progress bar and supports multi-threaded copying for local directories.

## Usage

Each script can be run from the command line. For example:

### Copy

**Arguments:**

1. <source_path>: The path to the file or directory to be copied.
2. <destination_path>: The path where the source should be copied.
3. If <source_path> is a file and <destination_path> does not exist or is a file, <source_path> is copied to <destination_path>.
4. If <source_path> is a file and <destination_path> is an existing directory, <source_path> is copied into that directory with its original name.
5. If <source_path> is a directory, it's copied to <destination_path>. Destination directories are created if they don't exist.

**Features:**

1. Displays a progress bar showing the copy speed, percentage completed, and ETA.
2. Unconditionally copies file metadata (permissions, timestamps via shutil.copystat).
3. Automatically creates necessary parent directories for the destination path.

```sh
python cp.py source.txt destination.txt
```

Examples:

```sh
# Copy a file to a new name
python cp.py source.txt backup/destination.txt

# Copy a file into an existing directory
python cp.py important_document.pdf ~/Documents/Archive/

# Copy a directory and its contents
python cp.py ./MyProject ~/Backups/MyProject_backup
```

### Move

**Arguments:**

1. <source_path>: The path to the file or directory to be moved or renamed.
<destination_path>: The new path or name for the source.
2. If <source_path> is a file and <destination_path> does not exist or is a file, <source_path> is moved/renamed to <destination_path>.
3. If <source_path> is a file and <destination_path> is an existing directory, <source_path> is moved into that directory with its original name.
4. If <source_path> is a directory, it's moved/renamed to <destination_path>.
5. Destination directories are created if they don't exist.

**Features:**

1. Displays a progress bar showing the move speed, percentage completed, and ETA.
2. Operation involves copying to the destination and then removing the source.
3. Unconditionally preserves file metadata (permissions, timestamps via shutil.copystat) during the copy phase.
4. Automatically creates necessary parent directories for the destination path.
5. Source files/directories are removed after a successful move.

```sh
python mv.py <source_path> <destination_path>
```

**Examples:**

```sh
# Rename a file
python mv.py old_report.docx final_report.docx

# Move a file into an existing directory
python mv.py image.jpg ~/Pictures/Vacation/

# Move a directory to a new location
python mv.py ./ProjectAlpha ~/ArchivedProjects/ProjectAlpha_archived
```

### Download

```sh
python dl.py <destination_path> <source_url_or_path> [options]
```

**Arguments:**

1. <destination_path>: The local path where the file/directory should be saved or copied.
2. If <source_url_or_path> is a URL and <destination_path> is a directory, the file is saved into that directory, inferring the filename from the URL.
3. If <source_url_or_path> is a URL and <destination_path> is a file path, the file is saved to that specific path.
4. If <source_url_or_path> is a local file/directory, standard copy/move logic applies similar to cp.py.
5. <source_url_or_path>: The HTTP/HTTPS URL to download from, or the local file/directory path to copy.
Options:
6. --mirror: When specified, mirrors directory structure and attributes (metadata like permissions, timestamps via shutil.copystat) for local copy operations. By default, this is disabled unless the flag is provided.
7. -t N, --threads N: Specifies the number of threads (N) for parallel copying of local directories. (Default: 1). This option is ignored for URL downloads or single file copies.

**Features:**

1. Progress bar for both URL downloads and local copy operations.
2. Supports HTTP and HTTPS URL downloads.
Handles copying of local files and directories.
3. Multi-threaded copying for local directories can significantly speed up operations on large numbers of files.
4. Preserves file/directory metadata for local operations if --mirror is specified.
5. Automatically creates necessary parent directories for the destination path.

## Aliasing in `.zshrc`

To make these scripts easier to use, you can create aliases in your `~/.zshrc` file. Add the following lines (replace `/path/to/your/scripts` with the actual path):

```sh
alias cp="python3 /path/to/your/scripts/cp.py"
alias dl="python3 /path/to/your/scripts/dl.py ~/Downloads --mirror -t 16"
alias mv="python3 /path/to/your/scripts/mv.py"
```

After editing `.zshrc`, reload it with:

```sh
source ~/.zshrc
```

Now you can uoverride `cp.py`, `mv.py`, and use `dl.py` as commands in your terminal.
