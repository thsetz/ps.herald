#!/usr/bin/env bash
set -e
set -x

ng build


/bin/rm -fR dist/save
mkdir dist/save
cp -R dist/ps-herald-angular/*  dist/save
sed -i.bak 's#src="#src="/static/angular_api/#g' dist/save/index.html
cp dist/save/index.html ../src/ps/herald/templates/angular_api/index.html
rm dist/save/index.html
rm dist/save/index.html.bak

cp dist/save/* ../src/ps/herald/static/angular_api/

ls -la  ../src/ps/herald/templates/angular_api/
ls -la  ../src/ps/herald/static/angular_api/


