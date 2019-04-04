install:
	pipenv install --dev
performance:
	pipenv run python3 performance.py
test:
	pipenv run pytest -v
coverage:
	pipenv run pytest --cov-report term-missing -v --cov=association/
clean:
	pipenv clean
