lint:
	pylint tests/ src/

test:
	python -m unittest discover -v -f