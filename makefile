install:
	pipenv install --dev
performance:
	pipenv run python3 performance.py
test:
	pipenv run pytest -v
lint:
	pipenv run  pylint --rcfile=.pylintrc association/*.py
coverage:
	pipenv run pytest --cov-report term-missing -v --cov=association/
clean:
	pipenv clean
