#!/bin/bash

# Add backend directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests with all flags and markdown format
python3 tests/test_endpoints.py "$@"