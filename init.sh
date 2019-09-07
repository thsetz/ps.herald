#!/usr/bin/env bash

set -e
set -x

/bin/rm -fR venv

python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install gunicorn


#cp ../microblog/microblog.py .
#cp ../microblog/config.py .
#cp ../microblog/boot.sh .
#chmod 755 boot.sh


