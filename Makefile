all: install

.PHONY: install test docs

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

lint-fix:
	uv run ruff check --fix habanero test

lint-check:
	uv run ruff check habanero test

format-fix:
	uv run ruff format habanero test

format-check:
	uv run ruff format --check habanero test

ipython:
	uv run --with rich --with ipython python -m IPython

py:
	uv run python
