#!/usr/bin/env bash

set -x
set -e

git log -1 --oneline >> CHANGES.txt
source ./venv/bin/activate && python version_incr.py
VERSION=`cat VERSION.txt`
git commit -m"autocommit from ci $VERSION"  CHANGES.txt VERSION.txt
git push

