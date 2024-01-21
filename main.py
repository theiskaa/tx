import subprocess

PATH = "~/dev/projects/tx"
NAME = "tx"

def run_command(command, capture_output=False):
    """Run a command in the shell and optionally capture its output."""
    result = subprocess.run(command, shell=True, capture_output=capture_output, text=True)
    return result

def session_exists(session_name):
    """Check if a TMUX session with the given name already exists."""
    result = run_command(f"tmux list-sessions", capture_output=True)
    return session_name in result.stdout

def rename_first_window(session_name, new_name):
    """Rename the first window in the session."""
    run_command(f"tmux rename-window -t {session_name}:1 {new_name}")
    navigate(session_name, new_name)

def navigate(session_name, window_name):
    """Navigate to a specified path and clear the screen in the given window."""
    run_command(f"tmux send-keys -t {session_name}:{window_name} 'cd {PATH}' C-m")
    run_command(f"tmux send-keys -t {session_name}:{window_name} 'clear' C-m")

def create_window_with_name(session_name, window_name):
    """Create a window with a specified name."""
    run_command(f"tmux new-window -t {session_name} -n {window_name}")
    navigate(session_name, window_name)

def create_window_with_split_panes(session_name, window_name):
    create_window_with_name(session_name, window_name)
    navigate(session_name, window_name)
    run_command(f"tmux split-window -h -t {session_name}:{window_name}")
    run_command(f"tmux select-pane -t {session_name}:{window_name}.1")
    run_command(f"tmux split-window -v -t {session_name}:{window_name}")

def main():
    if session_exists(NAME):
        print(f"A TMUX session named '{NAME}' already exists.")
        return

    run_command(f"tmux new-session -d -s {NAME}")

    rename_first_window(NAME, "code")
    create_window_with_split_panes(NAME, "src")
    create_window_with_name(NAME, "notya")

    run_command(f"tmux select-window -t {NAME}:code")

if __name__ == "__main__":
    main()
