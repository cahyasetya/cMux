#!/bin/bash

# This script attempts to run a command multiple times if it fails.
# Usage: ./retry_command.sh <command_to_retry> [max_retries] [retry_delay_seconds]

# Default values
MAX_RETRIES=${2:-3}     # Default to 3 retries if not provided
RETRY_DELAY=${3:-5}     # Default to 5 seconds if not provided

# The command to execute is the first argument
COMMAND_TO_RUN="$1"

if [ -z "$COMMAND_TO_RUN" ]; then
    echo "Usage: $0 <command_to_retry> [max_retries] [retry_delay_seconds]"
    exit 1
fi

echo "--- Starting retry wrapper for: $COMMAND_TO_RUN ---"

ATTEMPT=0
while [ $ATTEMPT -le $MAX_RETRIES ]; do
    echo "Attempt $((ATTEMPT + 1)) of $((MAX_RETRIES + 1)): Running command: $COMMAND_TO_RUN"
    # Execute the command
    eval "$COMMAND_TO_RUN"
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "Command '$COMMAND_TO_RUN' succeeded."
        break
    else
        echo "Command '$COMMAND_TO_RUN' failed with exit code $EXIT_CODE."
        if [ $ATTEMPT -lt $MAX_RETRIES ]; then
            echo "Retrying in $RETRY_DELAY seconds..."
            sleep $RETRY_DELAY
        else
            echo "Max retries reached. Command '$COMMAND_TO_RUN' failed permanently."
        fi
        ATTEMPT=$((ATTEMPT + 1))
    fi
done

echo "--- Retry wrapper finished for: $COMMAND_TO_RUN ---"
# Exit with the last command's exit code
exit $EXIT_CODE
