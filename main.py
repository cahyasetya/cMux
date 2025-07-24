"""cMux - Tmux session management tool."""
import csv
import subprocess
import sys
import time
from typing import Optional

def list_sessions() -> None:
    """Lists all active Tmux sessions."""
    print("Listing session\n")
    result = subprocess.run(['tmux', 'list-sessions'])
    print(f"Return code list-session: {result.returncode}\n")

def create_session(name: str) -> None:
    """Creates a new detached Tmux session."""
    print(f"Creating session : {name}\n")
    result = subprocess.run(['tmux', 'new-session', '-d', '-s', name])
    print(f"Return code create-session: {result.returncode}\n")

def kill_session(name: str) -> None:
    """Kills a specified Tmux session."""
    print(f"Killing session: {name}\n")
    result = subprocess.run(['tmux', 'kill-session', '-t', name])
    print(f"Return code kill-session: {result.returncode}\n")

def create_window(session_name: str, window_name: str) -> None:
    """Creates a new window within a specified Tmux session."""
    print(f"Creating window: {window_name} under session: {session_name}")
    result = subprocess.run(['tmux', 'new-window', '-t', session_name, '-n', window_name])
    print(f"Return code create_window: {result.returncode}\n")

def kill_window(session_name: str, window_name: str) -> None:
    """Kills a specific window within a Tmux session."""
    print(f"Killing window: {window_name} under session: {session_name}")
    result = subprocess.run(['tmux', 'kill-window', '-t', f'{session_name}:{window_name}'])
    print(f"Return code kill_window: {result.returncode}\n")

def is_session_exist(name: str) -> bool:
    """Checks if a Tmux session with the given name exists."""
    try:
        subprocess.run(['tmux', 'has-session', '-t', name], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def tmux_window_exists(session_name: str, window_name: str) -> bool:
    """Check if a window exists in a tmux session by name."""
    try:
        result = subprocess.run(
            ['tmux', 'list-windows', '-t', session_name, '-F', '#{window_name}'],
            capture_output=True,
            text=True,
            check=True
        )
        window_names = result.stdout.strip().split('\n')
        return window_name in window_names
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"❌ Command failed with exit code: {e.returncode}")
        print(f"❌ Error output: {e.stderr}")
        return False  # Session doesn't exist or no windows

def send_keys_to_tmux(session_name: str, window_name: str, keys: str) -> None:
    """Send keys to a tmux window.

    This function simply sends the keys once and reports the outcome of the
    'tmux send-keys' command itself. It does not implement any retry logic
    for the command being sent (e.g., SSH).

    Args:
        session_name: Name of the tmux session
        window_name: Name of the window
        keys: Command to send
    """
    print(f"Sending keys: {keys} to {session_name}:{window_name}")
    try:
        result = subprocess.run(
            ['tmux', 'send-keys', '-t', f'{session_name}:{window_name}', keys, 'Enter'],
            capture_output=True,
            text=True,
            timeout=5 # Timeout for the 'tmux send-keys' command itself
        )

        if result.returncode == 0:
            print(f"✅ Keys sent successfully to {session_name}:{window_name}")
        else:
            print(f"❌ Failed to send keys to {session_name}:{window_name}. Return code: {result.returncode}")
            if result.stderr:
                print(f"❌ Error: {result.stderr.strip()}")

    except subprocess.TimeoutExpired:
        print(f"⏱️  Sending keys to {session_name}:{window_name} timed out.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error sending keys to {session_name}:{window_name}: {e}")


def main() -> None:
    """Main entry point for cMux."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            csv_reader = csv.reader(f, delimiter="|")
            for row in csv_reader:
                if len(row) != 3:
                    print(f"Skipping malformed row: {row}")
                    continue

                session_name, window_name, command = [item.strip() for item in row] # Strip whitespace from components

                # In this clean version, the command is sent directly as read from CSV.
                # No wrapping with retry scripts or in-line retry logic.
                command_to_send = command

                if is_session_exist(session_name):
                    if tmux_window_exists(session_name=session_name, window_name=window_name):
                        print(f"Window '{window_name}' exists under session '{session_name}'")
                        send_keys_to_tmux(session_name=session_name, window_name=window_name, keys=command_to_send)
                    else:
                        create_window(session_name=session_name, window_name=window_name)
                        send_keys_to_tmux(session_name=session_name, window_name=window_name, keys=command_to_send)
                else:
                    create_session(name=session_name)
                    # Give tmux a moment to create the session before creating the window
                    time.sleep(0.1)
                    create_window(session_name=session_name, window_name=window_name)
                    send_keys_to_tmux(session_name=session_name, window_name=window_name, keys=command_to_send)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
