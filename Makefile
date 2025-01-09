.PHONY: all lint test install dev clean distclean

PYTHON ?= python

all: ;

lint:
	q2lint
	flake8

test: all
	py.test

test-cov: all
	python -m coverage run -m pytest && coverage xml -o coverage.xml

install: all
	$(PYTHON) -m pip install -v .

dev: all
	pip install -e .

clean: distclean

distclean: ;
