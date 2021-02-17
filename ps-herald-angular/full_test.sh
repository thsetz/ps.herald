#!/usr/bin/env bash
set -x
protractor protractor_conf.js 
echo "===================================  NEXT ================================="
ng test


