all: build install

.PHONY: build install test docs distclean dist upload

install:
	python3.10 -m pip install .

test:
	python3.10 -m pytest --record-mode=once --cov-report term --cov=habanero test/

test_no_vcr:
	python3.10 -m pytest --disable-recording --cov-report term --cov=habanero test/

docs:
	cd docs;\
	make html

opendocs:
	open docs/_build/html/index.html

clean:
	rm -rf dist/* build/*

dist:
	python3.10 -m build --sdist --wheel

register:
	python3.10 setup.py register

upload_test:
	python3.10 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload:
	python3.10 -m twine upload dist/*
