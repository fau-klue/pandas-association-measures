.PHONY: performance test lint coverage build

install:
	pipenv install --dev
performance:
	pipenv run python3 performance.py
test:
	pipenv run pytest -v
lint:
	pipenv run pylint --rcfile=.pylintrc association_measures/*.py
coverage:
	pipenv run pytest --cov-report term-missing -v --cov=association_measures/
compile:
	pipenv run python3 setup.py build_ext --inplace
build:
	pipenv run python3 setup.py sdist
clean:
	rm -rf *.egg-info build/ association_measures/*.so association_measures/*.c dist/
