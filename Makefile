SHELL = /usr/bin/env bash



clean:
	/bin/rm -fR LOG
	/bin/rm -fR dist 
	/bin/rm -fR build 
	/bin/rm -fR .tox 
	/bin/rm -fR venv 

init: clean
	/bin/rm -fR venv
	python3 -m venv venv
	source venv/bin/activate && pip3 install tox pytest coverage beautifulsoup4 
	source venv/bin/activate && pip3 install flake8 flake8-bugbear "flake8-docstrings>=1.3.1" "flake8-import-order>=0.9" "flake8-typing-imports>=1.1" "flake8-rst-docstrings" "pep8-naming"
	source venv/bin/activate && pip3 install -e .

	#source venv/bin/activate && pip3 install tox pytest coverage && python3 setup.py develop 

test:	
	source venv/bin/activate && tox -e tests

