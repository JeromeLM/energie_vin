#!/usr/bin/env zsh

set -e
echo "### BLACK"
black ./
echo "### FLAKE"
flake8 ./
echo "### PYTEST"
export PYTHONPATH="${PYTHONPATH}:${pwd}/src/"
export EXEC_PROFILE="test"
pytest --cov
echo "Everything is OK, Well done! Go go go push this!!"

