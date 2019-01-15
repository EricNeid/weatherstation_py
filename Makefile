PYTHON=python

init:
	pip install pipenv

install:
	pipenv install --dev

test:
	pipenv run nosetests

run:
	pipenv run $(PYTHON) weatherstation/gui_weatherstation.py

.PHONY: init install test
