install-pipenv:
	pip install --user pipenv

install:
	pipenv install --dev

tests:
	pipenv run nosetests

run:
	pipenv run python -m weatherstation

clean:
	pipenv clean

.PHONY: tests
