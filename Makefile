.PHONY: test coverage

test:
	.venv/bin/python -m pytest -q

coverage:
	.venv/bin/python -m pytest --cov=src --cov-report=term-missing
