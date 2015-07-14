# create virtual environment
PATH := .env/bin:$(PATH)

.env:
	virtualenv .env

# install all needed for development
develop: .env
	pip install -e . -r requirements-testing.txt tox coveralls

coverage: develop
	coverage run --source=pytest_services .env/bin/py.test tests
	coverage report -m

test: develop
	tox

coveralls: coverage
	coveralls

# clean the development envrironment
clean:
	-rm -rf .env

# debian dependencies
dependencies:
	sudo apt-get install `grep -vh '#' DEPENDENCIES*`
