# Event Script Utilities

This repository contains three Python scripts for basic file operations:

- `cp.py`: Copies files or directories with a detailed progress bar.
- `mv.py`: Moves or renames files or directories with a detailed progress bar.
- `dl.py`: Downloads files from HTTP/HTTPS URLs or copies local files/directories. It features a progress bar and supports multi-threaded copying for local directories.

## Usage

Each script can be run from the command line. For example:

### Copy

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

**Arguments:**

1. --mirror: When specified, mirrors directory structure and attributes (metadata like permissions, timestamps via shutil.copystat) for local copy operations. By default, this is disabled unless the flag is provided.
2. -t N, --threads N: Specifies the number of threads (N) for parallel copying of local directories. (Default: 1). This option is ignored for URL downloads or single file copies.

    ```sh
    python dl.py <destination_path> <source_url_or_path> [options]
    ```

**Features:**

1. Progress bar for both URL downloads and local copy operations.
2. Supports HTTP and HTTPS URL downloads.
Handles copying of local files and directories.
1. Multi-threaded copying for local directories can significantly speed up operations on large numbers of files.
2. Preserves file/directory metadata for local operations if --mirror is specified.
3. Automatically creates necessary parent directories for the destination path.

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