all: install

.PHONY: install test docs distclean dist upload

install:
	python3 -m pip install .

test:
	python3 -m pytest --record-mode=once --cov-report term --cov=habanero test/

test_no_vcr:
	python3 -m pytest --disable-recording --cov-report term --cov=habanero test/

docs:
	cd docs;\
	make html

opendocs:
	open docs/_build/html/index.html

clean:
	rm -rf dist/* build/*

dist:
	python3 -m build

upload_test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python3 -m twine upload dist/*

.PHONY: lint-fix
lint-fix:
	pip3 install -q -r requirements-dev.txt
	isort .
	black .
	flake8

.PHONY: lint-check
lint-check:
	pip3 install -q -r requirements-dev.txt
	isort . --check-only
	black . --check
	flake8 --count
