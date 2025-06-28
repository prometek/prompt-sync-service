# {{ service_name }}

## Description
Short description of the microservice.

## Installation

```sh
uv sync
```

## Documentation
Generate documentation with MkDocs

```sh
make docs
make docs-serve
```


## Local Setup
```sh
make build
make run
```

## Commands
- `make lint`: Run flake8 and black check
- `make test`: Run pytest
- `make build`: Build Docker image
- `make run`: Run service local
- `make docs`: Generate documentation with MkDocs
- `make docs-serve`: Serve documentation with MkDocs
- `make dev`: Run local development server
