# TX

`tx` is a script that automates the setup of TMUX sessions. It can create predefined TMUX sessions based on a JSON template or individual sessions with specified names and directory paths.

## How It Works

The script sets up TMUX sessions with specific window and pane configurations. For each session, it creates three windows named "code", "src", and "notya". The "src" window has split panes, while the others have a single pane.

Please only open pull requests that fix bugs or adds improvements without any breaking changes.
These dotfiles are very personal, and I know that everyone has a different taste; hence fork this repository or copy/paste them into your own dotfiles repo.

## Usage

### Using a JSON Template File

1. **Prepare a JSON Template File**: This file should list sessions with their names and desired start paths.

   Example (`sessions.json`):
   ```json
   [
     {"session1": "/path/to/dir1"},
     {"session2": "/path/to/dir2"}
   ]
   ```
   Replace `session1`, `session2`, etc., with your desired session names, and `/path/to/dir1`, `/path/to/dir2`, etc., with their start paths.

2. **Run the Script**: Execute the script with the path to your JSON template file.
   ```
   python main.py -t sessions.json
   ```

### Creating a Single Session Directly

To create an individual session:
```
python main.py -n session_name -p /path/to/directory
```
Replace `session_name` with the desired session name and `/path/to/directory` with the start path.

## Command-line Arguments

- `-t` or `--template`: Path to the JSON template file.
- `-n` or `--name`: Name of the TMUX session.
- `-p` or `--path`: Path for the session.
