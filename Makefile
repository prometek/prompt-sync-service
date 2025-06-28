.PHONY: lint test build run docs docs-serve dev

docker_image = template-python-service

lint:
	uv run	pre-commit run --all-files

test:
	uv run pytest --maxfail=1 --disable-warnings -q --cov=src


build:
	docker build -t $(docker_image) .

run:
	docker run -p 8000:8000 $(docker_image)

docs:
	mkdocs build

docs-serve:
	mkdocs serve

dev:
	devcontainer up --workspace-folder .
	devcontainer exec --workspace-folder . -- /bin/bash
