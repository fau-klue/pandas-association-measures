install:
	pipenv install --dev
performance:
	pipenv run python3 performance.py
test:
	pipenv run pytest -v
lint:
	pipenv run pylint --rcfile=.pylintrc association_measures/*.py
coverage:
	pipenv run pytest --cov-report term-missing -v --cov=association/
build:
	pipenv run python3 setup.py sdist
clean:
	pipenv clean; rm -rf *.egg-info
