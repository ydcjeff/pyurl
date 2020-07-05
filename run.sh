#!/bin/bash

# sorting imports
echo 'isort running...'
isort pyurl/pyurl.py tests/test_pyurl.py

# linting
echo 'flake8 running...'
flake8 pyurl/pyurl.py tests/test_pyurl.py

# code formatting
echo 'black running...'
black pyurl/pyurl.py tests/test_pyurl.py

# pytest
echo 'pytest running...'
pytest tests/test_pyurl.py
