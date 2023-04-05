#!/usr/bin/env zsh

pipenv lock -r > requirements.txt
set -e
echo "### BLACK"
black ./
echo "### FLAKE"
flake8 ./
echo "### PYTEST"
export PYTHONPATH="${PYTHONPATH}:./src/"
pytest --cov
echo "Everything is OK, Well done! Go go go push this!!"

