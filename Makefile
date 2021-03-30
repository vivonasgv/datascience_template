lint:
	pylint modules/ src/

test:
	python -m unittest discover -v -f