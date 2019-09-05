init:
	sudo apt-get install python3-kivy 
	pip install pipenv

install:
	pipenv install --dev

test:
	pipenv run nosetests 

run:
	pipenv run python weatherstation/gui_weatherstation.py

clean:
	pipenv clean

.PHONY: install-pipenv install test clean
