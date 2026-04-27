PY := python3
PIP := pip3

.PHONY: install assets run test docker-up docker-down clean

install:
	$(PIP) install -r scripts/requirements.txt

assets:
	cd scripts && $(PY) generate_assets.py

run: assets
	cd scripts && $(PY) orchestrator.py

test: assets
	$(PY) -m pytest tests/ -v

docker-up:
	docker compose -f vm/docker-compose.yml up --build -d

docker-down:
	docker compose -f vm/docker-compose.yml down

clean:
	rm -rf assets/*.enc assets/*.png assets/*.aes
	find . -name __pycache__ -type d -exec rm -rf {} +
