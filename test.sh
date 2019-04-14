#!/usr/bin/env bash
saved=$PYTHONPATH
export PYTHONPATH="./mobility_pipeline/:$PYTHONPATH"
python -m pytest

find mobility_pipeline -name '*.py' | xargs pylint
find tests/src -name '*.py' | xargs pylint

python -m mypy mobility_pipeline

liccheck -s strategy.ini -r requirements.txt
export PYTHONPATH="saved"
