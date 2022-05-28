default: web

web:
	flask run

dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pylint -rn vault tests
	mypy vault tests
	pytest tests
