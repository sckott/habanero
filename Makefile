all: install

.PHONY: install test docs distclean dist upload

install:
	uv pip install .

test:
	uv run pytest --record-mode=once --cov-report term --cov=habanero test/

test_no_vcr:
	uv run pytest --disable-recording --cov-report term --cov=habanero test/

docs:
	cd docs;\
	make html

opendocs:
	open docs/_build/html/index.html

clean:
	rm -rf dist/* build/*

dist:
	python -m build

upload_test:
	python -m twine upload --repository testpypi dist/*

upload:
	python -m twine upload --repository pypi dist/*

.PHONY: lint-fix
lint-fix:
	ruff check --select I --fix habanero

.PHONY: lint-check
lint-check:
	ruff check habanero

format:
	ruff format habanero
