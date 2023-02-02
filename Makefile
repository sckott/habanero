all: install

.PHONY: install test docs distclean dist upload

install:
	python3.11 -m pip install .

test:
	python3.11 -m pytest --record-mode=once --cov-report term --cov=habanero test/

test_no_vcr:
	python3.11 -m pytest --disable-recording --cov-report term --cov=habanero test/

docs:
	cd docs;\
	make html

opendocs:
	open docs/_build/html/index.html

clean:
	rm -rf dist/* build/*

dist:
	python3.11 -m build

upload_test:
	python3.11 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python3.11 -m twine upload dist/*
