#!/usr/bin/env bash

if [ -d ovenv ]
then
   /bin/rm -fR ovenv
fi
if [ -d venv ]
then
   mv venv ovenv
fi
python3 -m venv venv

source venv/bin/activate

pip3 install tox

