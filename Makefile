install-pipenv:
	pip install --user pipenv

install:
	pipenv install --dev

tests:
	pipenv run nosetests

run:
	pipenv run python weatherstation/gui_weatherstation.py

clean:
	pipenv clean

.PHONY: tests
