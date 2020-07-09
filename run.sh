#!/bin/bash

# sorting imports
echo 'isort running...'
isort pyurl/* tests/*

# linting
echo 'flake8 running...'
flake8 pyurl/* tests/*

# code formatting
echo 'black running...'
black pyurl/* tests/*

# pytest
echo 'pytest running...'
pytest tests/* --cov=./
