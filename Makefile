VERSION = $(shell grep -m1 '^version' pyproject.toml | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+")

.PHONY: test install build coverage clean

test:
	uv run pytest

install: build
	@echo "Installing pulla $(VERSION) with uv tool"
	uv tool install --force dist/pulla-$(VERSION)-py3-none-any.whl

build:
	@echo "Building distribution package for version $(VERSION)"
	uv build

coverage:
	uv run coverage run -m pytest
	uv run coverage report

clean:
	find . -type f -name '*.pyc' -exec rm {} +
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf dist build
