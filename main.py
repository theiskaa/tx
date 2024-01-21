import argparse
import json
import subprocess
import time

def run_command(command, capture_output=False):
    """Run a command in the shell and optionally capture its output."""
    result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
    return result

def session_exists(session_name):
    """Check if a TMUX session with the given name already exists."""
    result = run_command("tmux list-sessions", capture_output=True)
    return session_name in result.stdout

def create_session(session_name, path):
    """Create a TMUX session with the given name and path."""
    if session_exists(session_name):
        print(f"A TMUX session named '{session_name}' already exists.")
        return False

    run_command(f"tmux new-session -d -s {session_name}")
    setup_windows(session_name, path)
    return True

def rename_first_window(session_name, new_name, path):
    """Rename the first window in the session."""
    run_command(f"tmux rename-window -t {session_name}:1 {new_name}")
    navigate(session_name, new_name, path)

def navigate(session_name, window_name, path):
    """Navigate to a specified path and clear the screen in the given window."""
    run_command(f"tmux send-keys -t {session_name}:{window_name} 'cd {path}' C-m")
    run_command(f"tmux send-keys -t {session_name}:{window_name} 'clear' C-m")

def create_window_with_name(session_name, window_name, path):
    """Create a window with a specified name."""
    run_command(f"tmux new-window -t {session_name} -n {window_name}")
    navigate(session_name, window_name, path)

def create_window_with_split_panes(session_name, window_name, path):
    """Create a window with split panes."""
    create_window_with_name(session_name, window_name, path)
    run_command(f"tmux split-window -h -t {session_name}:{window_name}")
    run_command(f"tmux select-pane -t {session_name}:{window_name}.1")
    run_command(f"tmux split-window -v -t {session_name}:{window_name}")

def setup_windows(session_name, path):
    """Setup windows for a session."""
    rename_first_window(session_name, "code", path)
    create_window_with_split_panes(session_name, "src", path)
    create_window_with_name(session_name, "notya", path)
    run_command(f"tmux select-window -t {session_name}:code")

def loading_indicator(session_name, duration=2):
    """Simple loading indicator for the given duration."""
    print(f"Creating TMUX session '{session_name}'", end="")
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(1)
    print()

def main():
    parser = argparse.ArgumentParser(description="Create TMUX sessions based on JSON template or command line arguments.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--template', type=str, help='Path to JSON template file.')
    parser.add_argument('-n', '--name', type=str, help='Session name.')
    parser.add_argument('-p', '--path', type=str, help='Path for the session.')

    args = parser.parse_args()

    if args.template:
        try:
            with open(args.template) as file:
                sessions = json.load(file)
                for session_info in sessions:
                    for session_name, path in session_info.items():
                        print("-------------------------------")
                        loading_indicator(session_name)
                        if create_session(session_name, path):
                            print(f"Successfully created session '{session_name}'.")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}")
            return
    elif args.name and args.path:
        print("-------------------------------")
        loading_indicator(args.name)
        if create_session(args.name, args.path):
            print(f"Successfully created session '{args.name}'.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
