PYTHON=python
PIP=pip

init:
	$(PIP) install pipenv

install:
	pipenv install --dev --python 3

test:
	pipenv run nosetests 

run:
	pipenv run $(PYTHON) weatherstation/gui_weatherstation.py

clean:
	pipenv clean

.PHONY: init install test clean
