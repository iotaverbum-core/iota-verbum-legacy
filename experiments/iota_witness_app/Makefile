.PHONY: test backend-test backend-lint backend-typecheck

test: backend-test

backend-test:
	cd services/api && pytest -q

backend-lint:
	cd services/api && ruff check app tests

backend-typecheck:
	cd services/api && mypy app
