default: web

web:
	poetry run flask run

dev:
	poetry install

test:
	poetry run ruff --fix vault tests
	poetry run mypy vault tests
	# poetry run pytest tests
