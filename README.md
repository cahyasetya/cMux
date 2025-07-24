# cMux - Tmux Session Management Tool

A Python tool for managing tmux sessions, windows, and commands from CSV configuration files.

## Features

- Create tmux sessions and windows from CSV configuration
- Send commands to specific windows
- Check for existing sessions and windows before creating
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
production|logs|tail -f /var/log/app.log
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
