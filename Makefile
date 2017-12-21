PYTHON=python

init:
	pip install -r requirements.txt

test:
	nosetests

run:
	$(PYTHON) weatherstation/gui_weatherstation.py

.PHONY: init test
