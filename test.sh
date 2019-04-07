#!/usr/bin/env bash

python -m pytest

find mobility_pipeline -name '*.py' | xargs pylint
find tests/src -name '*.py' | xargs pylint

python -m mypy mobility_pipeline