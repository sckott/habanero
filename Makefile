all: build install

.PHONY: build install test docs distclean dist upload

build:
	python3 setup.py build

install:
	python3 setup.py install

test:
	nosetests -v --with-coverage --cover-package=habanero

test3:
	python3 -m "nose" -v --with-coverage --cover-package=habanero

docs:
	cd docs;\
	make html
	# open _build/html/index.html

distclean:
	rm dist/*

dist:
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal

register:
	python3 setup.py register

upload:
	twine upload dist/*
