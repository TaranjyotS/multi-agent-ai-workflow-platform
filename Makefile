.PHONY: install test lint security run docker-up docker-down docker-logs clean

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -q

lint:
	ruff check .

security:
	bandit -r app -c pyproject.toml

run:
	uvicorn app.main:app --reload --port 8000

docker-up:
	docker compose up --build

docker-down:
	docker compose down -v

docker-logs:
	docker compose logs -f api postgres redis qdrant

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' -o -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -delete
