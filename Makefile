SHELL := /bin/bash

init:
	python3 -m venv venv
	source ./venv/bin/activate && pip install -U setuptools
	source ./venv/bin/activate && pip install sphinx invoke ipython numpydoc devpi zest.releaser[recommended]
	source ./venv/bin/activate && pip install matplotlib
	source ./venv/bin/activate && pip install ps.basic 

doc:
	source ./venv/bin/activate && cd docs/source  && make html
