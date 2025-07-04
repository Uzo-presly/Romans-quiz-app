#!/bin/bash
source ./myvenv/bin/activate

# Set the correct path to the actual JSON file
export GOOGLE_APPLICATION_CREDENTIALS="./.secrets/true-oasis-449208-c6-27acdba00e47.json"

# Run the logger
python3 test_logger.py
