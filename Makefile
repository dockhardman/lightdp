LIGHTDP_VERSION := $(shell poetry version -s)

# Developing
install_all:
	poetry install --with dev

format_code:
	isort . --skip docs && black . --exclude docs

update_packages:
	poetry update
	poetry export --without-hashes -f requirements.txt --output requirements.txt
	poetry export --without-hashes --with dev -f requirements.txt --output requirements-dev.txt

pytest:
	python -m pytest

# Docker
build-docker-py310:
	docker build -t docker-python3.10:0.1.0 -f images/docker-py310.dockerfile .
