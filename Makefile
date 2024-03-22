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
	python3 -m twine upload --repository testpypi dist/*

upload:
	python3 -m twine upload --repository pypi dist/*

.PHONY: lint-fix
lint-fix:
	source .env/bin/activate; \
	pip3 install -q -r requirements-dev.txt; \
	ruff check --select I --fix habanero

.PHONY: lint-check
lint-check:
	source ./.env/bin/activate; \
	pip3 install -q -r requirements-dev.txt
	ruff check habanero
