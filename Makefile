default: web

web:
	venv/bin/flask run

dev:
	venv/bin/pip install -r requirements.txt -r requirements-dev.txt

test:
	venv/bin/pylint -rn vault tests
	venv/bin/mypy --install-types --non-interactive vault tests
	venv/bin/pytest tests
