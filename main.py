"""cMux - Tmux session management tool."""
import csv
import subprocess
import sys
from typing import Optional

def list_sessions() -> None:
    print("Listing session\n")
    result = subprocess.run(['tmux', 'list-sessions'])
    print(f"Return code list-session: {result.returncode}\n")

def create_session(name: str) -> None:
    print(f"Creating session : {name}\n")
    result = subprocess.run(['tmux', 'new-session', '-d', '-s', name])
    print(f"Return code create-session: {result.returncode}\n")

def kill_session(name: str) -> None:
    print(f"Killing session: {name}\n")
    result = subprocess.run(['tmux', 'kill-session', '-t', name])
    print(f"Return code kill-session: {result.returncode}\n")

def create_window(session_name: str, window_name: str) -> None:
    print(f"Creating window: {window_name} under session: {session_name}")
    result = subprocess.run(['tmux', 'new-window', '-t', session_name, '-n', window_name])
    print(f"Return code create_window: {result.returncode}\n")

def kill_window(session_name: str, window_name: str) -> None:
    print(f"Killing window: {window_name} under session: {session_name}")
    result = subprocess.run(['tmux', 'kill-window', '-t', f'{session_name}:{window_name}'])
    print(f"Return code kill_window: {result.returncode}\n")

def is_session_exist(name: str) -> bool:
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

def send_keys(session_name: str, window_name: str, keys: str) -> None:
    print(f"sending keys: {keys} to {session_name}:{window_name}")
    try:
        subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:{window_name}', keys, 'Enter'])
    except subprocess.CalledProcessError:
        print("Error sending keys")


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
                    
                session_name, window_name, command = row
                
                if is_session_exist(session_name):
                    if tmux_window_exists(session_name=session_name, window_name=window_name):
                        print(f"Window '{window_name}' exists under session '{session_name}'")
                        send_keys(session_name=session_name, window_name=window_name, keys=command)
                    else:
                        create_window(session_name=session_name, window_name=window_name)
                        send_keys(session_name=session_name, window_name=window_name, keys=command)
                else:
                    create_session(name=session_name)
                    create_window(session_name=session_name, window_name=window_name)
                    send_keys(session_name=session_name, window_name=window_name, keys=command)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
