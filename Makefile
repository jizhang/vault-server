default: web

web:
	./ve python -m scripts.web

dev:
	./ve pip install -r requirements.txt -r requirements-dev.txt

test:
	./ve pylint -rn vault tests
	./ve mypy vault tests
	./ve pytest tests
