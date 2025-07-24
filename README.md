# cMux - Tmux Session Management Tool

A Python tool for managing tmux sessions, windows, and commands from CSV configuration files.

## Features

- Create tmux sessions and windows from CSV configuration
- Send commands to specific windows
- Check for existing sessions and windows before creating
- **SSH Auto-Reconnection**: Automatically retry SSH commands that fail due to connection timeouts
- Simple pipe-delimited CSV format for configuration

## Installation

### Development Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   make install-dev
   ```

### For Development

Install pre-commit hooks (optional but recommended):
```bash
pip install pre-commit
pre-commit install
```

## Usage

Create a CSV file with pipe-delimited format:
```csv
session_name|window_name|command
test|window1|ls -a
test|window2|ls -l
production|ssh_server|ssh user@production-server.com
development|ssh_dev|ssh -p 2222 developer@dev-server.local
monitoring|ssh_monitor|ssh -o ServerAliveInterval=60 admin@monitor.company.com
```

Run cMux:
```bash
python main.py session.csv
```

## CSV Format

The CSV file should use pipe (|) delimiters with three columns:
- `session_name`: Name of the tmux session
- `window_name`: Name of the window within the session  
- `command`: Command to execute in that window

## SSH Auto-Reconnection

cMux automatically detects SSH commands and provides intelligent retry logic for connection failures:

**Features:**
- **Automatic Detection**: Recognizes `ssh` commands with various options
- **Smart Retry**: Retries failed SSH connections up to 3 times (configurable)
- **Connection Cleanup**: Sends Ctrl+C to clear failed attempts before retry
- **Progress Feedback**: Shows detailed status of connection attempts

**Supported SSH Command Formats:**
```bash
ssh user@host                           # Basic connection
ssh -p 2222 user@host                   # Custom port
ssh -o ServerAliveInterval=60 user@host # With options
ssh -i ~/.ssh/key user@host             # Custom key
```

**Example SSH Auto-Reconnection:**
```
🔗 Detected SSH command to: user@production-server.com
❌ Command failed with return code: 255
🔄 SSH connection might have failed, retrying in 2.0s... (attempt 1/3)
✅ SSH reconnection successful on attempt 2
```

**Why This Helps:**
- **Idle Timeouts**: SSH servers often disconnect idle connections
- **Network Issues**: Temporary network problems are automatically handled
- **Automation**: No manual intervention needed for common connection issues

## Development

### Available Make Commands

- `make help` - Show available commands
- `make install-dev` - Install development dependencies
- `make lint` - Run flake8 linting
- `make format` - Format code with black and isort
- `make type-check` - Run mypy type checking
- `make test` - Run tests
- `make test-cov` - Run tests with coverage
- `make all` - Run all checks (format, lint, type-check, test)
- `make clean` - Clean up generated files

### Code Quality Tools

This project uses several tools to maintain code quality:

- **flake8**: Linting and style checking
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for automated checks

### Running Quality Checks

```bash
# Format code
make format

# Run all quality checks
make all

# Quick lint and type check
make check
```

## Requirements

- Python 3.8+ (3.13 recommended)
- tmux installed and available in PATH

### Python Environment Setup

**Using virtualenv (recommended for this project):**
```bash
# Create virtual environment
python3 -m venv cmux

# Activate it
source cmux/bin/activate

# Install development dependencies
make install-dev
```

**Using pyenv (alternative):**
```bash
pyenv local 3.13.0  # or your preferred version
python -m venv cmux
source cmux/bin/activate
```
