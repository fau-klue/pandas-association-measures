.PHONY: performance test lint coverage build

install:
	python3 -m venv venv && \
	. venv/bin/activate && \
	pip3 install -U pip setuptools wheel && \
	pip3 install -r requirements-dev.txt

lint:
	. venv/bin/activate && \
	pylint --rcfile=.pylintrc association_measures/*.py

test:
	. venv/bin/activate && \
	pytest -s -v

performance:
	. venv/bin/activate && \
	python3 performance.py

coverage:
	. venv/bin/activate && \
	pytest --cov-report term-missing -v --cov=association_measures/

compile:
	. venv/bin/activate && \
	python3 setup.py build_ext --inplace

build:
	. venv/bin/activate && \
	python3 setup.py sdist

clean:
	rm -rf *.egg-info build/ association_measures/*.so association_measures/*.c dist/
